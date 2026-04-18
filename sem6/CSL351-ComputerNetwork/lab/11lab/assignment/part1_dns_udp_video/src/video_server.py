#!/usr/bin/env python3
import argparse
import select
import socket
import struct
import time

import cv2

CHUNK_HDR = struct.Struct("!IHHH")
MAX_DGRAM = 1200
MAX_CHUNK_PAYLOAD = MAX_DGRAM - CHUNK_HDR.size
KEEPALIVE_TIMEOUT_S = 0.2


def main() -> None:
    p = argparse.ArgumentParser(description="UDP video streaming server")
    p.add_argument("port", type=int)
    p.add_argument("jpeg_quality", type=int)
    args = p.parse_args()

    if args.port <= 0 or args.port > 65535:
        raise SystemExit("invalid port")
    if args.jpeg_quality < 1 or args.jpeg_quality > 100:
        raise SystemExit("jpeg_quality must be in [1,100]")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise SystemExit("failed to open webcam")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", args.port))
    sock.setblocking(False)

    print(f"Video UDP server listening on 0.0.0.0:{args.port}")

    active_client = None
    last_keepalive = 0.0
    frame_id = 0

    try:
        while True:
            ready, _, _ = select.select([sock], [], [], 0.005)
            if ready:
                payload, addr = sock.recvfrom(256)
                msg = payload.decode("utf-8", errors="ignore").strip()
                if msg.startswith("START"):
                    active_client = addr
                    last_keepalive = time.monotonic()
                    print(f"START from {addr[0]}:{addr[1]}")
                elif msg.startswith("KEEPALIVE") and active_client == addr:
                    last_keepalive = time.monotonic()

            if active_client is None:
                continue

            if time.monotonic() - last_keepalive > KEEPALIVE_TIMEOUT_S:
                print("Keep-alive timeout > 200ms. Stopping stream.")
                active_client = None
                continue

            ok, frame = cap.read()
            if not ok:
                continue

            ok, encoded = cv2.imencode(
                ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), args.jpeg_quality]
            )
            if not ok:
                continue

            data = encoded.tobytes()
            total_chunks = (len(data) + MAX_CHUNK_PAYLOAD - 1) // MAX_CHUNK_PAYLOAD
            if total_chunks == 0:
                continue

            for chunk_id in range(total_chunks):
                start = chunk_id * MAX_CHUNK_PAYLOAD
                chunk = data[start : start + MAX_CHUNK_PAYLOAD]
                hdr = CHUNK_HDR.pack(frame_id, chunk_id, total_chunks, len(chunk))
                sock.sendto(hdr + chunk, active_client)

            frame_id = (frame_id + 1) & 0xFFFFFFFF
    finally:
        cap.release()
        sock.close()


if __name__ == "__main__":
    main()
