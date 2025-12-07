# Team Members
- Agastya Nath(12340140)
- Paritosh Lahre(12341550)
- Y Rahul Dev Reddy(12342390)

# B+ Tree Index Implementation

This project implements a disk-based B+ Tree index in C++. It supports insertion, deletion, point search, and range search.

## Compilation

To compile the project, simply run:

```bash
make
```

This will generate an executable named `bplustree_driver`.

## Execution

To run the driver program with basic tests:

```bash
./bplustree_driver
```

To run a larger scale test:

```bash
./bplustree_driver large
```

## API Documentation

### `writeData`

**Synopsis**
```cpp
bool writeData(KeyType key, const Tuple& data);
```

**Description**
Inserts a key-value pair into the index.
- `key`: The integer key to insert.
- `data`: The 100-byte tuple data.

**Return Value**
Returns `true` (1) if insertion is successful. Returns `false` (0) if the key already exists or write failed.

### `deleteData`

**Synopsis**
```cpp
bool deleteData(KeyType key);
```

**Description**
Deletes a key and its associated data from the index.
- `key`: The key to delete.

**Return Value**
Returns `true` (1) if deletion is successful. Returns `false` (0) if the key was not found.

### `readData`

**Synopsis**
```cpp
bool readData(KeyType key, Tuple& outData);
```

**Description**
Searches for a key in the index.
- `key`: The key to search for.
- `outData`: Reference to a Tuple where the data will be stored if found.

**Return Value**
Returns `true` (1) if the key exists, and populates `outData`. Returns `false` (0) otherwise.

### `readRangeData`

**Synopsis**
```cpp
bool readRangeData(KeyType lowerKey, KeyType upperKey, int n, std::vector<Tuple>& result);
```

**Description**
Searches for all keys in the range `[lowerKey, upperKey]`.
- `lowerKey`: The start of the range (inclusive).
- `upperKey`: The end of the range (inclusive).
- `n`: Maximum number of results to return (not strictly enforced by implementation logic but used as a hint/limit in API design).
- `result`: Vector to store the resulting tuples.

**Return Value**
Returns `true` (1) if at least one key in the range is found. Returns `false` (0) otherwise.

## Implementation Details

- **Page Size**: 4096 bytes.
- **Key Type**: `int64_t`.
- **Data Type**: Fixed 100-byte array.
- **Storage**: File-based using `std::fstream`.
- **Structure**:
    - **Internal Nodes**: Store keys and page pointers. Order ~340.
    - **Leaf Nodes**: Store keys and actual data tuples. Order ~37. Linked list structure for range queries.
    - **Metadata**: Page 0 stores root page ID and total page count.

## Design Choices

- **No Buffer Manager**: Direct file I/O is used with `seekg`/`write`. The OS page cache acts as the buffer manager.
- **Space Management**: New pages are appended to the end of the file. Deleted pages are not currently reclaimed (simple implementation).
- **Deletion**: Uses lazy deletion (removal from leaf) without complex rebalancing/merging for simplicity, ensuring correctness of data presence.

## Benchmarks

Benchmarks were run on a standard desktop environment. The implementation shows consistent performance even as the dataset size grows, thanks to the logarithmic complexity of B+ Tree operations.

| Scale (N) | Insert Time (s) | Read Time (10k ops) (s) | Range Time (100 ops) (s) |
|-----------|-----------------|-------------------------|--------------------------|
| 10,000    | 0.0950          | 0.0438                  | 0.0012                   |>
| 100,000   | 1.0699          | 0.0515                  | 0.0015                   |
| 1,000,000 | 10.8992         | 0.0565                  | 0.0015                   |

*Note: Performance may vary based on disk speed (SSD vs HDD) and CPU.*

To run the benchmarks yourself:
```bash
./bplustree_driver benchmark
```
To run a specific size (e.g., 50000):
```bash
./bplustree_driver 50000
```

## Test Case Details

The driver program supports different modes of operation, each with specific test data generation strategies:

1.  **Default Run (`./bplustree_driver`)**:
    *   **Data**: Inserts keys `0` to `99` sequentially.
    *   **Operations**: Verifies all insertions, performs range search `[10, 19]`, and tests deletion of key `50`.

2.  **Large Scale (`./bplustree_driver large`)**:
    *   **Data**: Inserts 5,000 records with **even keys** (`0, 2, 4, ... 9998`).
    *   **Operations**: Verifies existence of key `100` and non-existence of key `101` (odd).

3.  **Benchmark / Custom Size (`./bplustree_driver <N>` or `benchmark`)**:
    *   **Insertion**: Inserts `N` records with sequential keys `0` to `N-1`. This tests the tree's performance under heavy sequential write load (append-only).
    *   **Point Search**: Performs 10,000 random searches for keys uniformly distributed in `[0, N-1]`.
    *   **Range Search**: Performs 100 random range queries. Each query starts at a random key `k` and requests 100 items (`[k, k+100]`).

## Script Mode (External Test Cases)

You can feed a script file to the driver to execute a sequence of commands. This is useful for grading or custom testing.

**Command Format:**

The script file should contain one command per line. The supported commands are:

1.  **`INSERT <key> <data>`**
    *   Inserts a record with the given integer key and string data.
    *   *Note:* The `<data>` string must **not** contain spaces (it is read as a single word).
    *   Example: `INSERT 100 user_profile_data`

2.  **`DELETE <key>`**
    *   Deletes the record associated with the given integer key.
    *   Example: `DELETE 100`

3.  **`SEARCH <key>`**
    *   Searches for the record with the given integer key and prints the data if found.
    *   Example: `SEARCH 100`

4.  **`RANGE <start_key> <end_key>`**
    *   Searches for all records with keys in the range `[start_key, end_key]` (inclusive).
    *   Example: `RANGE 50 150`

5.  **`EXIT`**
    *   Terminates the script execution.

**Example Usage:**

Create a file `test_input.txt`:
```text
INSERT 10 apple
INSERT 20 banana
SEARCH 10
RANGE 0 30
EXIT
```

Run the driver:
```bash
./bplustree_driver script < test_input.txt
```

