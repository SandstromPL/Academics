#ifndef BPLUSTREE_H
#define BPLUSTREE_H

#include <iostream>
#include <fstream>
#include <vector>
#include <cstring>
#include <string>
#include <cstdint>
#include <algorithm>

// Configuration
const int PAGE_SIZE = 4096;
const int TUPLE_SIZE = 100;
const int INVALID_PAGE_ID = -1;

// Types
using KeyType = int64_t;
using PageID = int32_t;

// Structures for Page Layout
// We will cast the raw buffer to these structs, or use them to serialize/deserialize.
// To ensure standard layout, we will manage offsets manually or use packed structs.
// For simplicity and portability, we'll manage offsets manually in the implementation,
// but define constants here.

// Page 0: Metadata
struct MetaData {
    PageID rootPageId;
    PageID totalPages; // Used for simple allocation
};

// Node Types
enum NodeType {
    INTERNAL = 0,
    LEAF = 1
};

// Constants for capacities
// Internal Node: Header(12) + P0(4) + N * (Key(8) + P(4)) <= 4096
// 16 + 12*N <= 4096 => 12*N <= 4080 => N = 340
const int MAX_KEYS_INTERNAL = 340;

// Leaf Node: Header(16) + N * (Key(8) + Data(100)) <= 4096
// 16 + 108*N <= 4096 => 108*N <= 4080 => N = 37
const int MAX_KEYS_LEAF = 37;

struct Tuple {
    uint8_t data[TUPLE_SIZE];
};

class BPlusTree {
private:
    std::fstream file;
    std::string filename;
    MetaData meta;

    // Helper to read/write pages
    void readPage(PageID pageId, char* buffer);
    void writePage(PageID pageId, const char* buffer);
    PageID allocatePage();

    // Helper functions for tree operations
    PageID findLeaf(KeyType key);
    
    // Insert helpers
    void insertIntoLeaf(PageID leafId, KeyType key, const Tuple& tuple);
    void insertIntoParent(PageID leftChildId, KeyType key, PageID rightChildId);
    
    // Delete helpers
    void deleteEntry(PageID nodeId, KeyType key);
    // Complex delete helpers (redistribute, merge) would go here

    // Debug
    void printTree(PageID pageId, int level);

public:
    BPlusTree(const std::string& fname);
    ~BPlusTree();

    // API
    bool writeData(KeyType key, const Tuple& data);
    bool deleteData(KeyType key);
    bool readData(KeyType key, Tuple& outData);
    bool readRangeData(KeyType lowerKey, KeyType upperKey, int n, std::vector<Tuple>& result);
    
    // Debug
    void print();
};

#endif // BPLUSTREE_H
