#!/usr/bin/env python3
import argparse
import socket
import struct
import time
from dataclasses import dataclass, field
from typing import Dict

import cv2
import numpy as np

REQ_HDR = struct.Struct("!HH")
RESP_HDR = struct.Struct("!HBH")
CHUNK_HDR = struct.Struct("!IHHH")
KEEPALIVE_INTERVAL_S = 0.1


def recv_exact(conn: socket.socket, size: int) -> bytes:
    data = bytearray()
    while len(data) < size:
        chunk = conn.recv(size - len(data))
        if not chunk:
            raise ConnectionError("peer closed")
        data.extend(chunk)
    return bytes(data)


def resolve_domain(dns_ip: str, dns_port: int, domain: str, txid: int) -> str:
    qname = domain.encode("utf-8")
    req = REQ_HDR.pack(txid, len(qname)) + qname

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((dns_ip, dns_port))
        s.sendall(req)

        resp_hdr = recv_exact(s, RESP_HDR.size)
        r_txid, status, ip_len = RESP_HDR.unpack(resp_hdr)
        if r_txid != txid or status != 0 or ip_len == 0:
            raise RuntimeError("domain resolution failed")

        ip_raw = recv_exact(s, ip_len)
        return ip_raw.decode("utf-8")


@dataclass
class FrameBuffer:
    frame_id: int = -1
    total_chunks: int = 0
    parts: Dict[int, bytes] = field(default_factory=dict)

    def reset(self, new_frame_id: int, total: int) -> None:
        self.frame_id = new_frame_id
        self.total_chunks = total
        self.parts.clear()


def main() -> None:
    p = argparse.ArgumentParser(description="DNS-assisted UDP video client")
    p.add_argument("dns_ip")
    p.add_argument("dns_port", type=int)
    p.add_argument("domain")
    p.add_argument("video_port", type=int)
    p.add_argument("txid", type=int)
    args = p.parse_args()

    resolved_ip = resolve_domain(args.dns_ip, args.dns_port, args.domain, args.txid & 0xFFFF)
    print(f"Domain: {args.domain}")
    print(f"IP Address: {resolved_ip}")

    server = (resolved_ip, args.video_port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.03)

    sock.sendto(b"START", server)

    fb = FrameBuffer()
    last_keepalive = 0.0

    try:
        while True:
            now = time.monotonic()
            if now - last_keepalive >= KEEPALIVE_INTERVAL_S:
                sock.sendto(b"KEEPALIVE", server)
                last_keepalive = now

            try:
                packet, _ = sock.recvfrom(1500)
            except socket.timeout:
                key = cv2.waitKey(1) & 0xFF
                if key in (27, ord("q")):
                    break
                continue

            if len(packet) < CHUNK_HDR.size:
                continue

            frame_id, chunk_id, total_chunks, payload_size = CHUNK_HDR.unpack_from(packet, 0)
            if total_chunks <= 0 or chunk_id >= total_chunks:
                continue
            if CHUNK_HDR.size + payload_size > len(packet):
                continue

            payload = packet[CHUNK_HDR.size : CHUNK_HDR.size + payload_size]

            if fb.frame_id != frame_id:
                fb.reset(frame_id, total_chunks)

            if fb.total_chunks != total_chunks:
                fb.reset(frame_id, total_chunks)

            fb.parts.setdefault(chunk_id, payload)

            if len(fb.parts) == fb.total_chunks:
                jpg = b"".join(fb.parts[i] for i in range(fb.total_chunks) if i in fb.parts)
                if len(jpg) == 0:
                    fb.parts.clear()
                    continue

                image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                if image is not None:
                    cv2.imshow("UDP Stream", image)

                key = cv2.waitKey(1) & 0xFF
                if key in (27, ord("q")):
                    break

                fb.parts.clear()
    finally:
        sock.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
