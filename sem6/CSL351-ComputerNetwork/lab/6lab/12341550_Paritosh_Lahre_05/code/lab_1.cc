/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/netanim-module.h" 

// Default Network Topology
//
//       10.1.1.0
// n0 -------------- n1
//    point-to-point
//
 
using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("FirstScriptExample"); //  Adding Logging to your Code

int
main (int argc, char *argv[])
{
  bool tracing = true;
  std::string band = "5Kbps";
  std::string lat = "15ms";
  uint32_t maxPkts = 100;
  double interval = 1.0;
  uint32_t pktSize = 1024;
  
  // Allow the user to override any of the defaults and the above
  // Bind()s at run-time, via command-line arguments
  CommandLine cmd;
  cmd.AddValue ("band", "Bandwidth", band);
  cmd.AddValue ("lat", "Latency", lat);
  cmd.AddValue ("maxPkts", "Max packets", maxPkts);
  cmd.AddValue ("interval", "Interval in seconds", interval);
  cmd.AddValue ("pktSize", "Packet size", pktSize);
  cmd.Parse (argc, argv);
  
  Time::SetResolution (Time::NS);
  //LogComponentEnable ("UdpClient", LOG_LEVEL_ERROR);
  //LogComponentEnable ("UdpServer", LOG_LEVEL_ERROR);
  LogComponentEnable ("FirstScriptExample", LOG_LEVEL_INFO);  //enabling log for this file...

// Explicitly create the nodes required by the topology (shown above).
  NS_LOG_INFO ("Create nodes.");
  NodeContainer nodes;
  nodes.Create (2);


// Explicitly create the point-to-point link required by the topology (shown above)
  NS_LOG_INFO ("Create channels.");
  PointToPointHelper pointToPoint;
  pointToPoint.SetDeviceAttribute ("DataRate", StringValue (band));
  pointToPoint.SetChannelAttribute ("Delay", StringValue (lat));

  NetDeviceContainer devices;
  devices = pointToPoint.Install (nodes);

// Install the internet stack on the nodes
  InternetStackHelper stack;
  stack.Install (nodes);


// We've got the "hardware" in place.  Now we need to add IP addresses.
  NS_LOG_INFO ("Assign IP Addresses.");
  Ipv4AddressHelper address;
  address.SetBase ("10.1.1.0", "255.255.255.0");

  Ipv4InterfaceContainer interfaces = address.Assign (devices);


// --- START OF MODIFIED SECTION ---
  NS_LOG_INFO ("Create Applications.");

  // 1. Create a standard UDP Server on Node 2 (Index 1)
  // We use UdpServerHelper instead of UdpEchoServerHelper as required 
  uint16_t port = 9; 
  UdpServerHelper myServer (port); 
  ApplicationContainer serverApps = myServer.Install (nodes.Get (1));
  serverApps.Start (Seconds (1.0));
  serverApps.Stop (Seconds (30.0)); // Total simulation time: 1 minute 

  // 2. Create a standard UDP Client on Node 1 (Index 0)
  // Pointing to the IP address assigned to Node 2 
  UdpClientHelper myClient (interfaces.GetAddress (1), 9);
  myClient.SetAttribute ("MaxPackets", UintegerValue (maxPkts));   
  myClient.SetAttribute ("Interval", TimeValue (Seconds (interval)));
  myClient.SetAttribute ("PacketSize", UintegerValue (pktSize));

  ApplicationContainer clientApps = myClient.Install (nodes.Get (0));
  clientApps.Start (Seconds (2.0));
  clientApps.Stop (Seconds (30.0));
  
  // --- Question 4: Additional Echo Application Flow ---
NS_LOG_INFO ("Create Additional Echo Application.");

// 1. Configure a different Port to avoid conflict
uint16_t newPort = 10; 

// 2. Set up the second Server (Echo Server) on Node 2
UdpEchoServerHelper echoServer (newPort); 
ApplicationContainer echoServerApps = echoServer.Install (nodes.Get (1));
echoServerApps.Start (Seconds (1.5)); // Start slightly after the first server
echoServerApps.Stop (Seconds (30.0));

// 3. Set up the second Client (Echo Client) on Node 1
UdpEchoClientHelper echoClient (interfaces.GetAddress (1), newPort);
echoClient.SetAttribute ("MaxPackets", UintegerValue (50));
echoClient.SetAttribute ("Interval", TimeValue (Seconds (1.0)));
echoClient.SetAttribute ("PacketSize", UintegerValue (512));

ApplicationContainer echoClientApps = echoClient.Install (nodes.Get (0));
echoClientApps.Start (Seconds (2.5));
echoClientApps.Stop (Seconds (30.0));
  // --- END OF MODIFIED SECTION ---

//Enable ascii trace and pcap trace 

  if (tracing)
    {
      AsciiTraceHelper ascii;
      pointToPoint.EnableAsciiAll (ascii.CreateFileStream ("p2p.tr"));
      //pointToPoint.EnablePcapAll ("p2p", false);
      // Increase the max packets allowed in a single PCAP trace file
      pointToPoint.EnablePcapAll ("p2ppcap", true);
    }

//AnimationInterface anim ("animation.xml")
  AnimationInterface anim("f1.xml");
  Simulator::Run ();
  // --- ADD THIS AFTER RUN TO PRINT RESULTS ---
// Get the total packets and bytes received by the server
Ptr<UdpServer> serverApp = DynamicCast<UdpServer> (serverApps.Get (0));
uint32_t totalPacketsReceived = serverApp->GetReceived ();
// To calculate throughput, we need total bytes. 
// Note: You can also find this in Wireshark.
NS_LOG_UNCOND ("--------------------------------------------------");
NS_LOG_UNCOND ("Packets Received: " << totalPacketsReceived);
NS_LOG_UNCOND ("--------------------------------------------------");
  Simulator::Destroy ();
  return 0;
}
