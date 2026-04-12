#include "tcp-12342320.h"
#include "ns3/log.h"
#include "ns3/simulator.h"

namespace ns3 {

NS_LOG_COMPONENT_DEFINE ("Tcp12342320");
NS_OBJECT_ENSURE_REGISTERED (Tcp12342320);

TypeId
Tcp12342320::GetTypeId (void)
{
  static TypeId tid = TypeId ("ns3::Tcp12342320")
    .SetParent<TcpNewReno> ()
    .SetGroupName ("Internet")
    .AddConstructor<Tcp12342320> ()
  ;
  return tid;
}

Tcp12342320::Tcp12342320 ()
  : TcpNewReno (),
    m_delayMin (Time::Max ()),
    m_currRtt (Seconds (0.0)),
    m_found (false),
    m_hystartDelayThresh (MilliSeconds (4)) // Standard HyStart threshold
{
}

Tcp12342320::Tcp12342320 (const Tcp12342320& sock)
  : TcpNewReno (sock),
    m_delayMin (sock.m_delayMin),
    m_currRtt (sock.m_currRtt),
    m_found (sock.m_found),
    m_hystartDelayThresh (sock.m_hystartDelayThresh)
{
}

Tcp12342320::~Tcp12342320 ()
{
}

Ptr<TcpCongestionOps>
Tcp12342320::Fork ()
{
  return CreateObject<Tcp12342320> (*this);
}

void
Tcp12342320::PktsAcked (Ptr<TcpSocketState> tcb, uint32_t packetsAcked, const Time& rtt)
{
  if (rtt.IsZero ())
    {
      return;
    }

  m_currRtt = rtt;

  // Update minimum RTT
  if (m_currRtt < m_delayMin)
    {
      m_delayMin = m_currRtt;
    }

  // HyStart Delay-based exit logic
  // If we are in Slow Start, check if current RTT exceeds minimum RTT by the threshold
  if (tcb->m_cWnd < tcb->m_ssThresh)
    {
      if (m_currRtt > m_delayMin + m_hystartDelayThresh)
        {
          m_found = true; // Delay spike detected! We should exit slow start.
        }
    }
}

void
Tcp12342320::IncreaseWindow (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked)
{
  if (tcb->m_cWnd < tcb->m_ssThresh)
    {
      // We are in Slow Start
      if (m_found)
        {
          // HyStart triggered! Exit Slow Start early by dropping ssthresh down to current cwnd
          NS_LOG_INFO ("HyStart triggered an early exit from Slow Start at time " << Simulator::Now ().GetSeconds ());
          tcb->m_ssThresh = tcb->m_cWnd;
          m_found = false; // Reset flag
        }
      
      // Execute standard Slow Start increment
      tcb->m_cWnd += tcb->m_segmentSize;
    }
  else
    {
      // We are in Congestion Avoidance
      // Execute standard NewReno Congestion Avoidance
      TcpNewReno::IncreaseWindow (tcb, segmentsAcked);
    }
}

std::string
Tcp12342320::GetName () const
{
  return "Tcp12342320";
}

} // namespace ns3
