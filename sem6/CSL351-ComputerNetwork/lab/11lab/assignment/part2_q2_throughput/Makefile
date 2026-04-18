CC=gcc
CFLAGS=-Wall -Wextra -O2
SRC_DIR=src
BIN_DIR=bin

all: $(BIN_DIR)/echo_server $(BIN_DIR)/echo_perf_client

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(BIN_DIR)/echo_server: $(SRC_DIR)/echo_server.c | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $<

$(BIN_DIR)/echo_perf_client: $(SRC_DIR)/echo_perf_client.c | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -rf $(BIN_DIR)

.PHONY: all clean
