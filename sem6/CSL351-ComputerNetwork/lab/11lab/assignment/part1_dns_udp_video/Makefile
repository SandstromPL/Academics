PYTHON=python3

all:
	@echo "Part 1 uses Python. No native build required."
	@echo "Run: make setup"

setup:
	$(PYTHON) -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

run-dns:
	$(PYTHON) src/dns_server.py 5300 dns_records.txt

run-video:
	$(PYTHON) src/video_server.py 9000 70

run-client:
	$(PYTHON) src/client.py 127.0.0.1 5300 video.server.com 9000 100

clean:
	rm -rf .venv __pycache__ src/__pycache__

.PHONY: all setup run-dns run-video run-client clean
