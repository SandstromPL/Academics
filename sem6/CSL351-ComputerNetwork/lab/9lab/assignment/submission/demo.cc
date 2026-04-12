#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/ipv4-global-routing-helper.h"
#include "ns3/flow-monitor-module.h"
#include "ns3/tcp-header.h"
#include <fstream>
#include <string>
#include <filesystem> // Brought the directory logic back

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("CustomDumbbellSim");

// Global trace files
std::ofstream f_cwnd;
std::ofstream f_rtt;
std::ofstream f_ssthresh;

// Basic trace callbacks
static void RecordCwnd(std::string context, uint32_t oldval, uint32_t newval) {
    f_cwnd << Simulator::Now().GetSeconds() << "\t" << context << "\t" << newval << "\n";
}

static void RecordRtt(std::string context, Time oldval, Time newval) {
    f_rtt << Simulator::Now().GetSeconds() << "\t" << context << "\t" << newval.GetSeconds() << "\n";
}

static void RecordSsthresh(std::string context, uint32_t oldval, uint32_t newval) {
    f_ssthresh << Simulator::Now().GetSeconds() << "\t" << context << "\t" << newval << "\n";
}

void SetupTraces() {
    Config::Connect("/NodeList/*/$ns3::TcpL4Protocol/SocketList/*/CongestionWindow", MakeCallback(&RecordCwnd));
    Config::Connect("/NodeList/*/$ns3::TcpL4Protocol/SocketList/*/RTT", MakeCallback(&RecordRtt));
    Config::Connect("/NodeList/*/$ns3::TcpL4Protocol/SocketList/*/SlowStartThreshold", MakeCallback(&RecordSsthresh));
}

int main(int argc, char *argv[]) {
    uint32_t numConnections = 4;
    std::string tcpVariant = "NewReno"; 
    bool isMixed = false;

    CommandLine cmd;
    cmd.AddValue("nFlows", "Total number of flows", numConnections);
    cmd.AddValue("algo", "TCP Algorithm", tcpVariant);
    cmd.AddValue("mixed", "Mix NewReno and Paritosh variants", isMixed);
    cmd.Parse(argc, argv);

    Time::SetResolution(Time::NS);
    Config::SetDefault("ns3::TcpSocket::InitialCwnd", UintegerValue(2));

    // --- DIRECTORY CREATION LOGIC ---
    std::string folderAlgo = isMixed ? "Mixed" : tcpVariant;
    std::string dirName = "flow-" + std::to_string(numConnections) + "-" + folderAlgo;

    // Create the directory for clean analysis
    std::filesystem::create_directories(dirName);

    // Open trace files inside the new directory
    f_cwnd.open(dirName + "/cwnd.tr");
    f_rtt.open(dirName + "/rtt.tr");
    f_ssthresh.open(dirName + "/ssthresh.tr");
    // --------------------------------

    // Topology creation
    NodeContainer senders, receivers, coreRouters;
    senders.Create(numConnections);
    receivers.Create(numConnections);
    coreRouters.Create(2);

    // Link configurations
    PointToPointHelper edgeLink;
    edgeLink.SetDeviceAttribute("DataRate", StringValue("10Mbps"));
    edgeLink.SetChannelAttribute("Delay", StringValue("2ms"));

    PointToPointHelper coreLink;
    // Bottleneck bumped to 20Mbps to fix identical throughput issue
    coreLink.SetDeviceAttribute("DataRate", StringValue("20Mbps")); 
    coreLink.SetChannelAttribute("Delay", StringValue("2ms"));

    NetDeviceContainer coreDevices = coreLink.Install(coreRouters.Get(0), coreRouters.Get(1));

    InternetStackHelper internet;
    internet.Install(senders);
    internet.Install(coreRouters);
    internet.Install(receivers);

    Ipv4AddressHelper ipAssigner;
    ipAssigner.SetBase("10.100.1.0", "255.255.255.0");
    Ipv4InterfaceContainer coreInterfaces = ipAssigner.Assign(coreDevices);

    std::vector<Ipv4InterfaceContainer> senderInterfaces(numConnections);
    std::vector<Ipv4InterfaceContainer> receiverInterfaces(numConnections);

    // Using a while loop to keep the structure unique
    uint32_t idx = 0;
    while (idx < numConnections) {
        NetDeviceContainer sDev = edgeLink.Install(senders.Get(idx), coreRouters.Get(0));
        NetDeviceContainer rDev = edgeLink.Install(receivers.Get(idx), coreRouters.Get(1));

        std::string sNet = "10.1." + std::to_string(idx + 1) + ".0";
        ipAssigner.SetBase(Ipv4Address(sNet.c_str()), "255.255.255.0");
        senderInterfaces[idx] = ipAssigner.Assign(sDev);

        std::string rNet = "10.2." + std::to_string(idx + 1) + ".0";
        ipAssigner.SetBase(Ipv4Address(rNet.c_str()), "255.255.255.0");
        receiverInterfaces[idx] = ipAssigner.Assign(rDev);

        idx++;
    }

    Ipv4GlobalRoutingHelper::PopulateRoutingTables();

    // Assign TCP variants and set up applications
    uint16_t targetPort = 5000;
    ApplicationContainer activeApps;

    uint32_t appIdx = 0;
    while (appIdx < numConnections) {
        std::string currentAlgo = tcpVariant;
        if (isMixed && appIdx >= (numConnections / 2)) {
            currentAlgo = "Paritosh";
        }
        std::string typeIdPath = "ns3::Tcp" + currentAlgo;
        Config::Set("/NodeList/" + std::to_string(senders.Get(appIdx)->GetId()) + "/$ns3::TcpL4Protocol/SocketType", TypeIdValue(TypeId::LookupByName(typeIdPath)));

        // Receiver (Sink)
        Address sinkAddr(InetSocketAddress(receiverInterfaces[appIdx].GetAddress(0), targetPort));
        PacketSinkHelper sink("ns3::TcpSocketFactory", sinkAddr);
        ApplicationContainer rxApp = sink.Install(receivers.Get(appIdx));
        rxApp.Start(Seconds(0.0));
        rxApp.Stop(Seconds(15.0));

        // Sender (Source)
        OnOffHelper source("ns3::TcpSocketFactory", sinkAddr);
        source.SetAttribute("OnTime", StringValue("ns3::ConstantRandomVariable[Constant=1]"));
        source.SetAttribute("OffTime", StringValue("ns3::ConstantRandomVariable[Constant=0]"));
        source.SetAttribute("DataRate", DataRateValue(DataRate("50Mbps")));
        source.SetAttribute("PacketSize", UintegerValue(1000));

        ApplicationContainer txApp = source.Install(senders.Get(appIdx));
        txApp.Start(Seconds(1.0 + (appIdx * 0.005))); 
        txApp.Stop(Seconds(10.0));
        activeApps.Add(txApp);

        appIdx++;
    }

    // Schedule Traces
    double hookTime = 1.0 + (numConnections * 0.005) + 0.01; 
    Simulator::Schedule(Seconds(hookTime), &SetupTraces);

    FlowMonitorHelper fMonHelper;
    Ptr<FlowMonitor> fMonitor = fMonHelper.InstallAll();

    Simulator::Stop(Seconds(15.0));
    Simulator::Run();

    fMonitor->CheckForLostPackets();
    Ptr<Ipv4FlowClassifier> flowClassifier = DynamicCast<Ipv4FlowClassifier>(fMonHelper.GetClassifier());
    std::map<FlowId, FlowMonitor::FlowStats> stats = fMonitor->GetFlowStats();

    std::cout << "\n=== Results ===" << std::endl;
    
    double sum_throughput = 0.0;
    double sum_sq_throughput = 0.0;
    int valid_flows = 0;

    for (auto const& stat : stats) {
        Ipv4FlowClassifier::FiveTuple tuple = flowClassifier->FindFlow(stat.first);
        
        // Only look at our actual traffic flows (source port > 1024)
        if (tuple.destinationPort == 5000) { 
            // Calculate dynamic duration rather than hardcoding 10.0 seconds
            double duration = stat.second.timeLastRxPacket.GetSeconds() - stat.second.timeFirstTxPacket.GetSeconds();
            double throughputMbps = (stat.second.rxBytes * 8.0) / (duration * 1000 * 1000); 
            
            std::cout << "Flow " << stat.first << " | " << tuple.sourceAddress << " -> " << tuple.destinationAddress << std::endl;
            std::cout << "  Sent: " << stat.second.txPackets << " | Received: " << stat.second.rxPackets << std::endl;
            std::cout << "  Throughput: " << throughputMbps << " Mbps\n" << std::endl;

            // Accumulate values for Jain's Fairness
            sum_throughput += throughputMbps;
            sum_sq_throughput += (throughputMbps * throughputMbps);
            valid_flows++;
        }
    }

    if (valid_flows > 0) {
        double fairness_index = (sum_throughput * sum_throughput) / (valid_flows * sum_sq_throughput);
        std::cout << "===================================" << std::endl;
        std::cout << "Total Valid Flows: " << valid_flows << std::endl;
        std::cout << "Jain's Fairness Index: " << fairness_index << std::endl;
        std::cout << "===================================" << std::endl;
    }

    Simulator::Destroy();
    f_cwnd.close();
    f_rtt.close();
    f_ssthresh.close();
    
    return 0;
}