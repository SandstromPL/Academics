#include "tcp-paritosh.h"
#include "ns3/log.h"
#include "ns3/simulator.h"

namespace ns3 {

NS_LOG_COMPONENT_DEFINE ("TcpParitosh");
NS_OBJECT_ENSURE_REGISTERED (TcpParitosh);

TypeId
TcpParitosh::GetTypeId (void)
{
  static TypeId tid = TypeId ("ns3::TcpParitosh")
    .SetParent<TcpNewReno> ()
    .SetGroupName ("Internet")
    .AddConstructor<TcpParitosh> ();
  return tid;
}

TcpParitosh::TcpParitosh ()
  : TcpNewReno (),
    m_delayMin (Time::Max ()),
    m_currRtt (Seconds (0.0)),
    m_found (false),
    m_hystartDelayThresh (MilliSeconds (4)) // Standard HyStart threshold
{
}

TcpParitosh::TcpParitosh (const TcpParitosh& sock)
  : TcpNewReno (sock),
    m_delayMin (sock.m_delayMin),
    m_currRtt (sock.m_currRtt),
    m_found (sock.m_found),
    m_hystartDelayThresh (sock.m_hystartDelayThresh)
{
}

TcpParitosh::~TcpParitosh () {}

Ptr<TcpCongestionOps>
TcpParitosh::Fork ()
{
  return CreateObject<TcpParitosh> (*this);
}

void
TcpParitosh::PktsAcked (Ptr<TcpSocketState> tcb, uint32_t packetsAcked, const Time& rtt)
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

  // Simplified HyStart Delay-based exit logic
  if (tcb->m_cWnd < tcb->m_ssThresh)
    {
      if (m_currRtt > m_delayMin + m_hystartDelayThresh)
        {
          m_found = true; // Delay spike detected! We should exit slow start.
        }
    }
}

void
TcpParitosh::IncreaseWindow (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked)
{
  if (tcb->m_cWnd < tcb->m_ssThresh)
    {
      // We are in Slow Start
      if (m_found)
        {
          // HyStart triggered! Exit Slow Start early by dropping ssthresh down to current cwnd
          NS_LOG_INFO ("HyStart triggered an early exit from Slow Start");
          tcb->m_ssThresh = tcb->m_cWnd;
          m_found = false; // Reset flag
        }
      
      // Execute standard Slow Start increment
      tcb->m_cWnd += tcb->m_segmentSize;
    }
  else
    {
      // We are in Congestion Avoidance
      TcpNewReno::IncreaseWindow (tcb, segmentsAcked);
    }
}

std::string
TcpParitosh::GetName () const
{
  return "TcpParitosh";
}

} // namespace ns3