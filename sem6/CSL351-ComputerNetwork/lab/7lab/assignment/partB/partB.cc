#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/ipv4-global-routing-helper.h"
#include "ns3/flow-monitor-module.h"
#include "ns3/mobility-module.h"
#include "ns3/error-model.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("Assignment6PartB");

int main(int argc, char *argv[]) {
    Time::SetResolution(Time::NS);

    // --- Command Line Arguments for Automation ---
    double errorRate = 0.0;
    std::string errorUnit = "Packet";
    uint32_t rngRun = 50; // Starting at 50 for my roll number 12341550

    CommandLine cmd;
    cmd.AddValue("errorRate", "The error rate (0 to 1)", errorRate);
    cmd.AddValue("errorUnit", "The error unit (Packet, Bit, Byte)", errorUnit);
    cmd.AddValue("rngRun", "The RngRun seed value", rngRun);
    cmd.Parse(argc, argv);

    // Set the seed run for randomness
    RngSeedManager::SetRun(rngRun);

    // Create Nodes & Routers
    NodeContainer leafNodes;
    leafNodes.Create(8); 
    NodeContainer routers;
    routers.Create(3);

    PointToPointHelper p2pStandard;
    p2pStandard.SetDeviceAttribute("DataRate", StringValue("5Mbps"));
    p2pStandard.SetChannelAttribute("Delay", StringValue("2ms"));

    PointToPointHelper p2pSpecial;
    p2pSpecial.SetDeviceAttribute("DataRate", StringValue("10Mbps"));
    p2pSpecial.SetChannelAttribute("Delay", StringValue("5ms"));

    NetDeviceContainer d_n0_r0 = p2pSpecial.Install(leafNodes.Get(0), routers.Get(0));
    NetDeviceContainer d_n1_r0 = p2pStandard.Install(leafNodes.Get(1), routers.Get(0));
    NetDeviceContainer d_n2_r0 = p2pSpecial.Install(leafNodes.Get(2), routers.Get(0));
    NetDeviceContainer d_r0_r1 = p2pStandard.Install(routers.Get(0), routers.Get(1));
    NetDeviceContainer d_r0_r2 = p2pStandard.Install(routers.Get(0), routers.Get(2));
    NetDeviceContainer d_n3_r1 = p2pSpecial.Install(leafNodes.Get(3), routers.Get(1));
    NetDeviceContainer d_n4_r1 = p2pStandard.Install(leafNodes.Get(4), routers.Get(1));
    NetDeviceContainer d_n5_r1 = p2pStandard.Install(leafNodes.Get(5), routers.Get(1));
    NetDeviceContainer d_n6_r2 = p2pSpecial.Install(leafNodes.Get(6), routers.Get(2));
    NetDeviceContainer d_n7_r2 = p2pStandard.Install(leafNodes.Get(7), routers.Get(2));

    InternetStackHelper stack;
    stack.Install(leafNodes);
    stack.Install(routers);

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

    Ipv4GlobalRoutingHelper::PopulateRoutingTables();

    // --- Apply RateErrorModel ---
    Ptr<RateErrorModel> em = CreateObject<RateErrorModel>();
    em->SetAttribute("ErrorRate", DoubleValue(errorRate));
    
    if (errorUnit == "Packet") {
        em->SetAttribute("ErrorUnit", StringValue("ERROR_UNIT_PACKET"));
    } else if (errorUnit == "Bit") {
        em->SetAttribute("ErrorUnit", StringValue("ERROR_UNIT_BIT"));
    } else if (errorUnit == "Byte") {
        em->SetAttribute("ErrorUnit", StringValue("ERROR_UNIT_BYTE"));
    }

    // Safely attach Error Model ONLY to the Point-to-Point devices
    NetDeviceContainer allP2PDevices;
    allP2PDevices.Add(d_n0_r0);
    allP2PDevices.Add(d_n1_r0);
    allP2PDevices.Add(d_n2_r0);
    allP2PDevices.Add(d_r0_r1);
    allP2PDevices.Add(d_r0_r2);
    allP2PDevices.Add(d_n3_r1);
    allP2PDevices.Add(d_n4_r1);
    allP2PDevices.Add(d_n5_r1);
    allP2PDevices.Add(d_n6_r2);
    allP2PDevices.Add(d_n7_r2);

    for (uint32_t i = 0; i < allP2PDevices.GetN(); ++i) {
        allP2PDevices.Get(i)->SetAttribute("ReceiveErrorModel", PointerValue(em));
    }

    // --- Setup UdpEcho Traffic Flows (Replacing Part A flows) ---
    uint16_t port = 9;
    
    // Flow 1: Echo n7 -> n4
    UdpEchoServerHelper server1(port);
    ApplicationContainer serverApp1 = server1.Install(leafNodes.Get(4));
    serverApp1.Start(Seconds(1.0));
    serverApp1.Stop(Seconds(10.0));
    UdpEchoClientHelper client1(i_n4_r1.GetAddress(0), port);
    client1.SetAttribute("MaxPackets", UintegerValue(150));
    client1.SetAttribute("Interval", TimeValue(Seconds(0.05)));
    client1.SetAttribute("PacketSize", UintegerValue(1024));
    ApplicationContainer clientApp1 = client1.Install(leafNodes.Get(7));
    clientApp1.Start(Seconds(2.0));
    clientApp1.Stop(Seconds(10.0));

    // Flow 2: Echo n1 -> n5
    UdpEchoServerHelper server2(port+1);
    ApplicationContainer serverApp2 = server2.Install(leafNodes.Get(5));
    serverApp2.Start(Seconds(1.0));
    serverApp2.Stop(Seconds(10.0));
    UdpEchoClientHelper client2(i_n5_r1.GetAddress(0), port+1);
    client2.SetAttribute("MaxPackets", UintegerValue(150));
    client2.SetAttribute("Interval", TimeValue(Seconds(0.05)));
    client2.SetAttribute("PacketSize", UintegerValue(1024));
    ApplicationContainer clientApp2 = client2.Install(leafNodes.Get(1));
    clientApp2.Start(Seconds(2.0));
    clientApp2.Stop(Seconds(10.0));

    // Flow 3: Echo n2 -> n6
    UdpEchoServerHelper server3(port+2);
    ApplicationContainer serverApp3 = server3.Install(leafNodes.Get(6));
    serverApp3.Start(Seconds(1.0));
    serverApp3.Stop(Seconds(10.0));
    UdpEchoClientHelper client3(i_n6_r2.GetAddress(0), port+2);
    client3.SetAttribute("MaxPackets", UintegerValue(150));
    client3.SetAttribute("Interval", TimeValue(Seconds(0.05)));
    client3.SetAttribute("PacketSize", UintegerValue(1024));
    ApplicationContainer clientApp3 = client3.Install(leafNodes.Get(2));
    clientApp3.Start(Seconds(2.0));
    clientApp3.Stop(Seconds(10.0));

    // Flow 4: Echo n0 -> n3
    UdpEchoServerHelper server4(port+3);
    ApplicationContainer serverApp4 = server4.Install(leafNodes.Get(3));
    serverApp4.Start(Seconds(1.0));
    serverApp4.Stop(Seconds(10.0));
    UdpEchoClientHelper client4(i_n3_r1.GetAddress(0), port+3);
    client4.SetAttribute("MaxPackets", UintegerValue(150));
    client4.SetAttribute("Interval", TimeValue(Seconds(0.05)));
    client4.SetAttribute("PacketSize", UintegerValue(1024));
    ApplicationContainer clientApp4 = client4.Install(leafNodes.Get(0));
    clientApp4.Start(Seconds(2.0));
    clientApp4.Stop(Seconds(10.0));

    // FlowMonitor
    Ptr<FlowMonitor> flowmon;
    FlowMonitorHelper flowmonHelper;
    flowmon = flowmonHelper.InstallAll();

    Simulator::Stop(Seconds(11.0));
    Simulator::Run();

    // --- Calculate and Print PDR ---
    flowmon->CheckForLostPackets();
    std::map<FlowId, FlowMonitor::FlowStats> stats = flowmon->GetFlowStats();
    
    uint64_t t_total = 0;
    uint64_t r_total = 0;

    for (std::map<FlowId, FlowMonitor::FlowStats>::const_iterator i = stats.begin(); i != stats.end(); ++i) {
        t_total += i->second.txPackets;
        r_total += i->second.rxPackets;
    }

    double pdr = 0.0;
    if (t_total > 0) {
        pdr = (double)r_total / (double)t_total;
    }

    // Print strictly the PDR value for easy automation scraping
    std::cout << pdr << std::endl;

    Simulator::Destroy();
    return 0;
}
