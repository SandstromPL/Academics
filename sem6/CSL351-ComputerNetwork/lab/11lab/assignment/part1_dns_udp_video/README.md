# Part 1: DNS-Assisted UDP Video Streaming (Python)

## Components
- `src/dns_server.py`: Custom TCP DNS resolver server with file-backed records.
- `src/video_server.py`: UDP webcam streamer using JPG encoding and chunked datagrams.
- `src/client.py`: Client that resolves domain over TCP first, then receives/display video over UDP.
- `dns_records.txt`: Domain-to-IP mappings (>= 5 entries).
- `requirements.txt`: Python dependencies for streaming client/server.

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run Order (localhost demo)
Terminal 1:
```bash
python3 src/dns_server.py 5300 dns_records.txt
```

Terminal 2:
```bash
python3 src/video_server.py 9000 70
```

Terminal 3:
```bash
python3 src/client.py 127.0.0.1 5300 video.server.com 9000 100
```

## Expected behavior
1. Client prints:
   - `Domain: video.server.com`
   - `IP Address: 127.0.0.1`
2. Video starts only after successful DNS resolution.
3. Client sends keep-alive every 100 ms.
4. Server stops streaming if no keep-alive is received for >200 ms.

## Protocol Summary
- DNS request (TCP): `txid(2) + qname_len(2) + qname`.
- DNS response (TCP): `txid(2) + status(1) + ip_len(2) + ip`.
- Video chunk (UDP): `frame_id(4) + chunk_id(2) + total_chunks(2) + payload_size(2) + payload`.
- Control messages (UDP): `START`, `KEEPALIVE`.

## Notes
- Press `q` or `Esc` in the client display window to stop.
- UDP loss is handled by dropping incomplete frames and continuing playback.
