#!/usr/bin/env python3
import argparse
import socket
import struct
from typing import Dict

REQ_HDR = struct.Struct("!HH")
RESP_HDR = struct.Struct("!HBH")


def recv_exact(conn: socket.socket, size: int) -> bytes:
    data = bytearray()
    while len(data) < size:
        chunk = conn.recv(size - len(data))
        if not chunk:
            raise ConnectionError("peer closed connection")
        data.extend(chunk)
    return bytes(data)


def send_all(conn: socket.socket, payload: bytes) -> None:
    view = memoryview(payload)
    while view:
        sent = conn.send(view)
        if sent <= 0:
            raise ConnectionError("failed to send")
        view = view[sent:]


def load_records(path: str) -> Dict[str, str]:
    records: Dict[str, str] = {}
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) >= 2:
                records[parts[0]] = parts[1]
    return records


def serve(port: int, records_file: str) -> None:
    records = load_records(records_file)
    if len(records) < 5:
        raise RuntimeError("records file must contain at least 5 domain->IP entries")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("0.0.0.0", port))
        srv.listen(10)
        print(f"DNS TCP server listening on 0.0.0.0:{port} with {len(records)} records")

        while True:
            conn, addr = srv.accept()
            with conn:
                try:
                    hdr = recv_exact(conn, REQ_HDR.size)
                    txid, qname_len = REQ_HDR.unpack(hdr)
                    if qname_len == 0 or qname_len > 255:
                        continue

                    qname_raw = recv_exact(conn, qname_len)
                    qname = qname_raw.decode("utf-8", errors="replace")
                    ip = records.get(qname)
                    if ip is None:
                        resp = RESP_HDR.pack(txid, 1, 0)
                        send_all(conn, resp)
                        print(f"MISS txid={txid} domain={qname} from {addr[0]}:{addr[1]}")
                    else:
                        ip_b = ip.encode("utf-8")
                        resp = RESP_HDR.pack(txid, 0, len(ip_b)) + ip_b
                        send_all(conn, resp)
                        print(f"HIT txid={txid} domain={qname} -> {ip}")
                except Exception as exc:
                    print(f"request error from {addr}: {exc}")


def main() -> None:
    p = argparse.ArgumentParser(description="Custom TCP DNS server")
    p.add_argument("port", type=int)
    p.add_argument("records_file")
    args = p.parse_args()

    if args.port <= 0 or args.port > 65535:
        raise SystemExit("invalid port")

    serve(args.port, args.records_file)


if __name__ == "__main__":
    main()
