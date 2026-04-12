#ifndef TCP_12342320_H
#define TCP_12342320_H

//#include "tcp-newreno.h"
#include "tcp-congestion-ops.h"
#include "ns3/tcp-recovery-ops.h"
#include "ns3/sequence-number.h"
#include "ns3/traced-value.h"

namespace ns3 {

class Tcp12342320 : public TcpNewReno
{
public:
  static TypeId GetTypeId (void);

  Tcp12342320 ();
  Tcp12342320 (const Tcp12342320& sock);
  virtual ~Tcp12342320 ();

  virtual Ptr<TcpCongestionOps> Fork () override;

  // Overriding essential methods to inject HyStart
  virtual void PktsAcked (Ptr<TcpSocketState> tcb, uint32_t packetsAcked, const Time& rtt) override;
  virtual void IncreaseWindow (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked) override;

  virtual std::string GetName () const override;

protected:
  // HyStart specific variables
  Time m_delayMin;         // Minimum RTT 
  Time m_currRtt;          // Current RTT
  bool m_found;            // Flag to check if exit point is found
  Time m_hystartDelayThresh; // Threshold for delay spike
};

} // namespace ns3

#endif /* TCP_12342320_H */
