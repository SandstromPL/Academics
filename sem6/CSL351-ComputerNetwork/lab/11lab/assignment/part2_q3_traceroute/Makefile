CC=gcc
CFLAGS=-Wall -Wextra -O2
SRC_DIR=src
BIN_DIR=bin

all: $(BIN_DIR)/traceroute

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(BIN_DIR)/traceroute: $(SRC_DIR)/traceroute.c | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -rf $(BIN_DIR)

.PHONY: all clean
