CC = gcc
CFLAGS = -g

# Programs to build
PROGS = null Q4 Q5 Q6 Q7

all: step1 step2 step3 step4 step5 step6 step7

# --- Step 1: Compile and run null.c normally ---
step1: null
	@echo "======== Step 1: Running null ============================="
	./null || true

# --- Step 2: Run null under gdb ---
step2: null
	@echo "======== Step 2: Running null under gdb ==================="
	@echo "run" | gdb null

# --- Step 3: Run null under valgrind ---
step3: null
	@echo "======== Step 3: Running null under valgrind =============="
	valgrind --leak-check=yes ./null || true

# --- Step 4: malloc() without free ---
step4: Q4
	@echo "======== Step 4: Running Q4 (malloc without free) ========="
	./Q4 || true
	@echo "=== gdb output ==="
	@echo "run" | gdb Q4
	@echo "=== valgrind output ==="
	valgrind --leak-check=yes ./Q4 || true

# --- Step 5: Array overflow ---
step5: Q5
	@echo "======== Step 5: Running Q5 (array overflow) =============="
	./Q5 || true
	valgrind --leak-check=yes ./Q5 || true

# --- Step 6: Use after free ---
step6: Q6
	@echo "======== Step 6: Running Q6 (use after free) =============="
	./Q6 || true
	valgrind --leak-check=yes ./Q6 || true

# --- Step 7: Invalid free ---
step7: Q7
	@echo "======== Step 7: Running Q7 (invalid free) ================"
	./Q7 || true
	valgrind --leak-check=yes ./Q7 || true

# --- Build rules ---
null: null.c
	$(CC) $(CFLAGS) -o null null.c

Q4: Q4.c
	$(CC) $(CFLAGS) -o Q4 Q4.c

Q5: Q5.c
	$(CC) $(CFLAGS) -o Q5 Q5.c

Q6: Q6.c
	$(CC) $(CFLAGS) -o Q6 Q6.c

Q7: Q7.c
	$(CC) $(CFLAGS) -o Q7 Q7.c

# Clean build artifacts
clean:
	rm -f $(PROGS)

