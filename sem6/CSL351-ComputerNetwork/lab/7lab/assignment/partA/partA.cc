#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/ipv4-global-routing-helper.h"
#include "ns3/netanim-module.h"
#include "ns3/flow-monitor-module.h"
#include "ns3/mobility-module.h"
#include <fstream>

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("Assignment6PartA");

int main(int argc, char *argv[]) {
    Time::SetResolution(Time::NS);

    // Create 8 leaf nodes (n0 to n7) and 3 routers (router0, router1, router2)
    NodeContainer leafNodes;
    leafNodes.Create(8); 
    NodeContainer routers;
    routers.Create(3);

    // Standard Point-to-Point link parameters
    PointToPointHelper p2pStandard;
    p2pStandard.SetDeviceAttribute("DataRate", StringValue("5Mbps"));
    p2pStandard.SetChannelAttribute("Delay", StringValue("2ms"));

    // Special Point-to-Point link parameters for n0->n3 and n2->n6 flows
    PointToPointHelper p2pSpecial;
    p2pSpecial.SetDeviceAttribute("DataRate", StringValue("10Mbps"));
    p2pSpecial.SetChannelAttribute("Delay", StringValue("5ms"));

    // Install P2P links
    // n0, n1, n2 to router0
    NetDeviceContainer d_n0_r0 = p2pSpecial.Install(leafNodes.Get(0), routers.Get(0));
    NetDeviceContainer d_n1_r0 = p2pStandard.Install(leafNodes.Get(1), routers.Get(0));
    NetDeviceContainer d_n2_r0 = p2pSpecial.Install(leafNodes.Get(2), routers.Get(0));

    // router0 to router1 and router2
    NetDeviceContainer d_r0_r1 = p2pStandard.Install(routers.Get(0), routers.Get(1));
    NetDeviceContainer d_r0_r2 = p2pStandard.Install(routers.Get(0), routers.Get(2));

    // n3, n4, n5 to router1
    NetDeviceContainer d_n3_r1 = p2pSpecial.Install(leafNodes.Get(3), routers.Get(1));
    NetDeviceContainer d_n4_r1 = p2pStandard.Install(leafNodes.Get(4), routers.Get(1));
    NetDeviceContainer d_n5_r1 = p2pStandard.Install(leafNodes.Get(5), routers.Get(1));

    // n6, n7 to router2
    NetDeviceContainer d_n6_r2 = p2pSpecial.Install(leafNodes.Get(6), routers.Get(2));
    NetDeviceContainer d_n7_r2 = p2pStandard.Install(leafNodes.Get(7), routers.Get(2));

    // Install Internet stack
    InternetStackHelper stack;
    stack.Install(leafNodes);
    stack.Install(routers);

    // Assign IP Addresses (Each P2P link needs its own subnet)
    Ipv4AddressHelper address;
    
    address.SetBase("10.1.1.0", "255.255.255.0");
    Ipv4InterfaceContainer i_n0_r0 = address.Assign(d_n0_r0);
    
    address.SetBase("10.1.2.0", "255.255.255.0");
    Ipv4InterfaceContainer i_n1_r0 = address.Assign(d_n1_r0);
    
    address.SetBase("10.1.3.0", "255.255.255.0");
    Ipv4InterfaceContainer i_n2_r0 = address.Assign(d_n2_r0);

    address.SetBase("10.1.4.0", "255.255.255.0");
    Ipv4InterfaceContainer i_r0_r1 = address.Assign(d_r0_r1);

    address.SetBase("10.1.5.0", "255.255.255.0");
    Ipv4InterfaceContainer i_r0_r2 = address.Assign(d_r0_r2);

    address.SetBase("10.1.6.0", "255.255.255.0");
    Ipv4InterfaceContainer i_n3_r1 = address.Assign(d_n3_r1);

    address.SetBase("10.1.7.0", "255.255.255.0");
    Ipv4InterfaceContainer i_n4_r1 = address.Assign(d_n4_r1);

    address.SetBase("10.1.8.0", "255.255.255.0");
    Ipv4InterfaceContainer i_n5_r1 = address.Assign(d_n5_r1);

    address.SetBase("10.1.9.0", "255.255.255.0");
    Ipv4InterfaceContainer i_n6_r2 = address.Assign(d_n6_r2);

    address.SetBase("10.1.10.0", "255.255.255.0");
    Ipv4InterfaceContainer i_n7_r2 = address.Assign(d_n7_r2);

    // Populate Routing Tables
    Ipv4GlobalRoutingHelper::PopulateRoutingTables();

    // Generate routing-tables.txt
    Ptr<OutputStreamWrapper> routingStream = Create<OutputStreamWrapper>("routing-tables.txt", std::ios::out);
    *routingStream->GetStream() << "Router 0 Routing Table\n";
    routers.Get(0)->GetObject<Ipv4>()->GetRoutingProtocol()->PrintRoutingTable(routingStream);
    *routingStream->GetStream() << "\nRouter 1 Routing Table\n";
    routers.Get(1)->GetObject<Ipv4>()->GetRoutingProtocol()->PrintRoutingTable(routingStream);
    *routingStream->GetStream() << "\nRouter 2 Routing Table\n";
    routers.Get(2)->GetObject<Ipv4>()->GetRoutingProtocol()->PrintRoutingTable(routingStream);

    // ---> THE PCAP  <---
    p2pStandard.EnablePcapAll("partA_trace");
    
    // --- Setup Traffic Flows ---
    uint16_t port = 8080;

    // Flow 1: TCP n7 -> n4
    Address tcpSinkAddr1(InetSocketAddress(i_n4_r1.GetAddress(0), port));
    PacketSinkHelper tcpSink1("ns3::TcpSocketFactory", tcpSinkAddr1);
    ApplicationContainer sinkApp1 = tcpSink1.Install(leafNodes.Get(4));
    sinkApp1.Start(Seconds(1.0));
    sinkApp1.Stop(Seconds(10.0));

    OnOffHelper tcpClient1("ns3::TcpSocketFactory", tcpSinkAddr1);
    tcpClient1.SetAttribute("DataRate", DataRateValue(DataRate("1Mbps")));
    tcpClient1.SetAttribute("PacketSize", UintegerValue(1024));
    ApplicationContainer clientApp1 = tcpClient1.Install(leafNodes.Get(7));
    clientApp1.Start(Seconds(2.0));
    clientApp1.Stop(Seconds(10.0));

    // Flow 2: UDP n1 -> n5
    Address udpSinkAddr2(InetSocketAddress(i_n5_r1.GetAddress(0), port+1));
    PacketSinkHelper udpSink2("ns3::UdpSocketFactory", udpSinkAddr2);
    ApplicationContainer sinkApp2 = udpSink2.Install(leafNodes.Get(5));
    sinkApp2.Start(Seconds(1.0));
    sinkApp2.Stop(Seconds(10.0));

    OnOffHelper udpClient2("ns3::UdpSocketFactory", udpSinkAddr2);
    udpClient2.SetAttribute("DataRate", DataRateValue(DataRate("500Kbps")));
    udpClient2.SetAttribute("PacketSize", UintegerValue(1024));
    ApplicationContainer clientApp2 = udpClient2.Install(leafNodes.Get(1));
    clientApp2.Start(Seconds(2.0));
    clientApp2.Stop(Seconds(10.0));

    // Flow 3: TCP n2 -> n6
    Address tcpSinkAddr3(InetSocketAddress(i_n6_r2.GetAddress(0), port+2));
    PacketSinkHelper tcpSink3("ns3::TcpSocketFactory", tcpSinkAddr3);
    ApplicationContainer sinkApp3 = tcpSink3.Install(leafNodes.Get(6));
    sinkApp3.Start(Seconds(1.0));
    sinkApp3.Stop(Seconds(10.0));

    OnOffHelper tcpClient3("ns3::TcpSocketFactory", tcpSinkAddr3);
    tcpClient3.SetAttribute("DataRate", DataRateValue(DataRate("2Mbps")));
    tcpClient3.SetAttribute("PacketSize", UintegerValue(1024));
    ApplicationContainer clientApp3 = tcpClient3.Install(leafNodes.Get(2));
    clientApp3.Start(Seconds(2.0));
    clientApp3.Stop(Seconds(10.0));

    // Flow 4: TCP n0 -> n3
    Address tcpSinkAddr4(InetSocketAddress(i_n3_r1.GetAddress(0), port+3));
    PacketSinkHelper tcpSink4("ns3::TcpSocketFactory", tcpSinkAddr4);
    ApplicationContainer sinkApp4 = tcpSink4.Install(leafNodes.Get(3));
    sinkApp4.Start(Seconds(1.0));
    sinkApp4.Stop(Seconds(10.0));

    OnOffHelper tcpClient4("ns3::TcpSocketFactory", tcpSinkAddr4);
    tcpClient4.SetAttribute("DataRate", DataRateValue(DataRate("2Mbps")));
    tcpClient4.SetAttribute("PacketSize", UintegerValue(1024));
    ApplicationContainer clientApp4 = tcpClient4.Install(leafNodes.Get(0));
    clientApp4.Start(Seconds(2.0));
    clientApp4.Stop(Seconds(10.0));

    // FlowMonitor
    Ptr<FlowMonitor> flowmon;
    FlowMonitorHelper flowmonHelper;
    flowmon = flowmonHelper.InstallAll();
    
    // Install a constant mobility model to silence NetAnim warnings
    MobilityHelper mobility;
    mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");
    mobility.Install(leafNodes);
    mobility.Install(routers);

    // NetAnim
    AnimationInterface anim("partA_anim.xml");
    
    // Set Node positions for NetAnim
    // Routers
    anim.SetConstantPosition(routers.Get(0), 40.0, 50.0); // Router 0 (Center-Left)
    anim.SetConstantPosition(routers.Get(1), 60.0, 30.0); // Router 1 (Top-Right)
    anim.SetConstantPosition(routers.Get(2), 60.0, 70.0); // Router 2 (Bottom-Right)

    // Left Leaf Nodes (connected to Router 0)
    anim.SetConstantPosition(leafNodes.Get(0), 20.0, 30.0); // n0
    anim.SetConstantPosition(leafNodes.Get(1), 20.0, 50.0); // n1
    anim.SetConstantPosition(leafNodes.Get(2), 20.0, 70.0); // n2

    // Top-Right Leaf Nodes (connected to Router 1)
    anim.SetConstantPosition(leafNodes.Get(3), 80.0, 10.0); // n3
    anim.SetConstantPosition(leafNodes.Get(4), 80.0, 30.0); // n4
    anim.SetConstantPosition(leafNodes.Get(5), 80.0, 50.0); // n5

    // Bottom-Right Leaf Nodes (connected to Router 2)
    anim.SetConstantPosition(leafNodes.Get(6), 80.0, 70.0); // n6
    anim.SetConstantPosition(leafNodes.Get(7), 80.0, 90.0); // n7
    
    Simulator::Stop(Seconds(11.0));
    Simulator::Run();

    // Print FlowMonitor Stats
    flowmon->CheckForLostPackets();
    Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier>(flowmonHelper.GetClassifier());
    std::map<FlowId, FlowMonitor::FlowStats> stats = flowmon->GetFlowStats();

    for (std::map<FlowId, FlowMonitor::FlowStats>::const_iterator i = stats.begin(); i != stats.end(); ++i) {
        Ipv4FlowClassifier::FiveTuple t = classifier->FindFlow(i->first);
        std::cout << "Flow " << i->first << " (" << t.sourceAddress << " -> " << t.destinationAddress << ")\n";
        std::cout << "  Tx Packets: " << i->second.txPackets << "\n";
        std::cout << "  Rx Packets: " << i->second.rxPackets << "\n";
        std::cout << "  Lost Packets: " << i->second.lostPackets << "\n";
        std::cout << "  Throughput: " << i->second.rxBytes * 8.0 / (i->second.timeLastRxPacket.GetSeconds() - i->second.timeFirstTxPacket.GetSeconds()) / 1024 / 1024  << " Mbps\n";
        // Note for your Goodput calculation: FlowMonitor measures at the IP layer. 
        // Goodput requires subtracting the TCP/UDP and IP header sizes from rxBytes.
    }

    Simulator::Destroy();
    return 0;
}
