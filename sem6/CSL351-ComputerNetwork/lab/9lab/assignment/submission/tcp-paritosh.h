#ifndef TCP_PARITOSH_H
#define TCP_PARITOSH_H

#include "ns3/tcp-congestion-ops.h"
#include "ns3/tcp-socket-state.h"

namespace ns3 {

class TcpParitosh : public TcpNewReno
{
public:
  static TypeId GetTypeId (void);
  TcpParitosh ();
  TcpParitosh (const TcpParitosh& sock);
  virtual ~TcpParitosh ();

  virtual Ptr<TcpCongestionOps> Fork () override;
  virtual std::string GetName () const override;

  // Override to capture RTT measurements for HyStart
  virtual void PktsAcked (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked, const Time& rtt) override;
  
  // Override to inject HyStart's early exit logic
  virtual void IncreaseWindow (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked) override;

private:
  Time m_delayMin;           //!<  Min delay
  Time m_currRtt;            //!<  Current Rtt
  bool m_found;              //!<  The exit point is found?
  Time m_hystartDelayThresh; //!< Delay threshold to trigger early exit
};

} // namespace ns3
#endif /* TCP_PARITOSH_H */