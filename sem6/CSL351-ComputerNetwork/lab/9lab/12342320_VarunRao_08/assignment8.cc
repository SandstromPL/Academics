#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/point-to-point-layout-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h"
#include <fstream>
#include <string>

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("Assignment8Script");

// Global streams for trace files
std::ofstream cwndFile;
std::ofstream ssthreshFile;
std::ofstream rttFile;
uint32_t senderNodeId = 0; // Will be set dynamically

static void CwndTracer (uint32_t oldval, uint32_t newval)
{
  cwndFile << Simulator::Now ().GetSeconds () << " " << newval << std::endl;
}

static void SsThreshTracer (uint32_t oldval, uint32_t newval)
{
  ssthreshFile << Simulator::Now ().GetSeconds () << " " << newval << std::endl;
}

static void RttTracer (Time oldval, Time newval)
{
  rttFile << Simulator::Now ().GetSeconds () << " " << newval.GetSeconds () << std::endl;
}

static void TraceSetup ()
{
  // Correct ns-3.44 path directly to the Socket inside the Protocol
  std::string prefix = "/NodeList/" + std::to_string(senderNodeId) + "/$ns3::TcpL4Protocol/SocketList/0/";
  Config::ConnectWithoutContext (prefix + "CongestionWindow", MakeCallback (&CwndTracer));
  Config::ConnectWithoutContext (prefix + "SlowStartThreshold", MakeCallback (&SsThreshTracer));
  Config::ConnectWithoutContext (prefix + "RTT", MakeCallback (&RttTracer));
}

int main (int argc, char *argv[])
{
  uint32_t nFlows = 4;
  bool isMixed = false; // False = All NewReno, True = Half NewReno, Half Tcp12342320

  CommandLine cmd;
  cmd.AddValue ("nFlows", "Number of flows (4, 8, 16, 20)", nFlows);
  cmd.AddValue ("isMixed", "Set to 1 to use half NewReno, half custom", isMixed);
  cmd.Parse (argc, argv);

  Config::SetDefault ("ns3::TcpSocket::SegmentSize", UintegerValue (1448));

  // Create Dumbbell Topology
  PointToPointHelper innerHelper;
  innerHelper.SetDeviceAttribute ("DataRate", StringValue ("10Mbps"));
  innerHelper.SetChannelAttribute ("Delay", StringValue ("20ms"));

  PointToPointHelper outerHelper;
  outerHelper.SetDeviceAttribute ("DataRate", StringValue ("100Mbps"));
  outerHelper.SetChannelAttribute ("Delay", StringValue ("1ms"));

  PointToPointDumbbellHelper dumbbell (nFlows, outerHelper, nFlows, outerHelper, innerHelper);

  InternetStackHelper stack;
  dumbbell.InstallStack (stack);

  dumbbell.AssignIpv4Addresses (
      Ipv4AddressHelper ("10.1.1.0", "255.255.255.0"),
      Ipv4AddressHelper ("10.2.1.0", "255.255.255.0"),
      Ipv4AddressHelper ("10.3.1.0", "255.255.255.0")
  );

  Ipv4GlobalRoutingHelper::PopulateRoutingTables ();

  // Dynamically get the exact Node ID of the first sender for our graphs
  senderNodeId = dumbbell.GetLeft(0)->GetId();
  uint16_t port = 50000;

  // Install Receivers
  for (uint32_t i = 0; i < nFlows; ++i)
    {
      Address sinkLocalAddress (InetSocketAddress (Ipv4Address::GetAny (), port));
      PacketSinkHelper sinkHelper ("ns3::TcpSocketFactory", sinkLocalAddress);
      ApplicationContainer sinkApp = sinkHelper.Install (dumbbell.GetRight (i));
      sinkApp.Start (Seconds (0.0));
      sinkApp.Stop (Seconds (20.0));
    }


// Install Senders with Bulletproof CCA Assignment
  for (uint32_t i = 0; i < nFlows; ++i)
    {
      std::string protocolName;
      if (isMixed && (i % 2 == 1)) 
        {
          protocolName = "ns3::Tcp12342320";
        } 
      else 
        {
          protocolName = "ns3::TcpNewReno";
        }
      
      // Force the specific node to use the specific TCP variant
      Config::Set ("/NodeList/" + std::to_string(dumbbell.GetLeft(i)->GetId()) + "/$ns3::TcpL4Protocol/SocketType", StringValue (protocolName));

      AddressValue remoteAddress (InetSocketAddress (dumbbell.GetRightIpv4Address (i), port));
      
      // Use OnOffApplication instead of BulkSend for more aggressive, reliable saturation
      OnOffHelper onoff ("ns3::TcpSocketFactory", Address ());
      onoff.SetAttribute ("Remote", remoteAddress);
      onoff.SetAttribute ("OnTime", StringValue ("ns3::ConstantRandomVariable[Constant=1]"));
      onoff.SetAttribute ("OffTime", StringValue ("ns3::ConstantRandomVariable[Constant=0]"));
      onoff.SetAttribute ("DataRate", StringValue ("50Mbps")); // Push hard to cause bottleneck
      onoff.SetAttribute ("PacketSize", UintegerValue (1448));

      ApplicationContainer sourceApp = onoff.Install (dumbbell.GetLeft (i));
      sourceApp.Start (Seconds (1.0));
      sourceApp.Stop (Seconds (20.0));
    }

  // Setup Tracing Files
  cwndFile.open ("cwnd.dat", std::ios::out);
  ssthreshFile.open ("ssthresh.dat", std::ios::out);
  rttFile.open ("rtt.dat", std::ios::out);
  
  // Schedule hooks after socket is guaranteed to be created
  Simulator::Schedule (Seconds (1.1), &TraceSetup);

  FlowMonitorHelper flowmon;
  Ptr<FlowMonitor> monitor = flowmon.InstallAll ();

  std::cout << "Starting Simulation for " << nFlows << " flows. Mixed Mode: " << (isMixed ? "Yes" : "No") << "..." << std::endl;
  
  Simulator::Stop (Seconds (20.0));
  Simulator::Run ();

  // Calculate Metrics
  monitor->CheckForLostPackets ();
  Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier> (flowmon.GetClassifier ());
  std::map<FlowId, FlowMonitor::FlowStats> stats = monitor->GetFlowStats ();

  double sumX = 0;
  double sumSqX = 0;
  int activeFlows = 0;

  std::cout << "\n--- Results ---" << std::endl;
  for (std::map<FlowId, FlowMonitor::FlowStats>::const_iterator i = stats.begin (); i != stats.end (); ++i)
    {
      if (i->first > nFlows) break; // Ignore ACK return flows
      double tput = i->second.rxBytes * 8.0 / 1000000.0 / 19.0; // 19s active time
      std::cout << "Flow " << i->first << " Throughput: " << tput << " Mbps" << std::endl;
      
      sumX += tput;
      sumSqX += (tput * tput);
      activeFlows++;
    }

  double jainsFairness = (sumX * sumX) / (activeFlows * sumSqX);
  std::cout << "\n>>> Jain's Fairness Index: " << jainsFairness << " <<<\n" << std::endl;

  cwndFile.close ();
  ssthreshFile.close ();
  rttFile.close ();
  Simulator::Destroy ();

  return 0;
}
