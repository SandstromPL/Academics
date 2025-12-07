#include "bplustree.h"
#include <iostream>
#include <cstring>
#include <algorithm>

// --- Helper Functions for Buffer Management ---

static int32_t readInt32(const char* buf, int offset) {
    int32_t val;
    std::memcpy(&val, buf + offset, sizeof(int32_t));
    return val;
}

static void writeInt32(char* buf, int offset, int32_t val) {
    std::memcpy(buf + offset, &val, sizeof(int32_t));
}

static int64_t readInt64(const char* buf, int offset) {
    int64_t val;
    std::memcpy(&val, buf + offset, sizeof(int64_t));
    return val;
}

static void writeInt64(char* buf, int offset, int64_t val) {
    std::memcpy(buf + offset, &val, sizeof(int64_t));
}

static void readTuple(const char* buf, int offset, Tuple& tuple) {
    std::memcpy(tuple.data, buf + offset, TUPLE_SIZE);
}

static void writeTuple(char* buf, int offset, const Tuple& tuple) {
    std::memcpy(buf + offset, tuple.data, TUPLE_SIZE);
}

// --- Node Accessors ---

// Common Header
// 0: IsLeaf (4 bytes) - 0 or 1
// 4: NumKeys (4 bytes)
// 8: Parent (4 bytes)

static bool isLeaf(const char* buf) {
    return readInt32(buf, 0) == 1;
}

static void setIsLeaf(char* buf, bool leaf) {
    writeInt32(buf, 0, leaf ? 1 : 0);
}

static int32_t getNumKeys(const char* buf) {
    return readInt32(buf, 4);
}

static void setNumKeys(char* buf, int32_t num) {
    writeInt32(buf, 4, num);
}

static int32_t getParent(const char* buf) {
    return readInt32(buf, 8);
}

static void setParent(char* buf, int32_t parent) {
    writeInt32(buf, 8, parent);
}

// Internal Node Layout
// Header: 12 bytes
// P0: 12
// K[i]: 16 + i*12
// P[i+1]: 16 + i*12 + 8

static int32_t getInternalPtr(const char* buf, int index) {
    // P0 is at 12
    // P1 is at 16 + 0*12 + 8 = 24
    // P2 is at 16 + 1*12 + 8 = 36
    if (index == 0) return readInt32(buf, 12);
    return readInt32(buf, 16 + (index - 1) * 12 + 8);
}

static void setInternalPtr(char* buf, int index, int32_t ptr) {
    if (index == 0) writeInt32(buf, 12, ptr);
    else writeInt32(buf, 16 + (index - 1) * 12 + 8, ptr);
}

static int64_t getInternalKey(const char* buf, int index) {
    return readInt64(buf, 16 + index * 12);
}

static void setInternalKey(char* buf, int index, int64_t key) {
    writeInt64(buf, 16 + index * 12, key);
}

// Leaf Node Layout
// Header: 12 bytes
// NextLeaf: 12 (4 bytes)
// K[i]: 16 + i*108
// V[i]: 16 + i*108 + 8

static int32_t getNextLeaf(const char* buf) {
    return readInt32(buf, 12);
}

static void setNextLeaf(char* buf, int32_t next) {
    writeInt32(buf, 12, next);
}

static int64_t getLeafKey(const char* buf, int index) {
    return readInt64(buf, 16 + index * 108);
}

static void setLeafKey(char* buf, int index, int64_t key) {
    writeInt64(buf, 16 + index * 108, key);
}

static void getLeafTuple(const char* buf, int index, Tuple& tuple) {
    readTuple(buf, 16 + index * 108 + 8, tuple);
}

static void setLeafTuple(char* buf, int index, const Tuple& tuple) {
    writeTuple(buf, 16 + index * 108 + 8, tuple);
}


// --- BPlusTree Implementation ---

BPlusTree::BPlusTree(const std::string& fname) : filename(fname) {
    // Open file for read/write. Create if not exists.
    file.open(filename, std::ios::in | std::ios::out | std::ios::binary);
    if (!file.is_open()) {
        // Try creating it
        file.open(filename, std::ios::out | std::ios::binary);
        file.close();
        file.open(filename, std::ios::in | std::ios::out | std::ios::binary);
    }

    // Check if empty
    file.seekg(0, std::ios::end);
    if (file.tellg() == 0) {
        // Initialize Metadata
        meta.rootPageId = INVALID_PAGE_ID;
        meta.totalPages = 1; // Page 0 is metadata
        
        char buf[PAGE_SIZE];
        std::memset(buf, 0, PAGE_SIZE);
        writeInt32(buf, 0, meta.rootPageId);
        writeInt32(buf, 4, meta.totalPages);
        writePage(0, buf);
    } else {
        // Read Metadata
        char buf[PAGE_SIZE];
        readPage(0, buf);
        meta.rootPageId = readInt32(buf, 0);
        meta.totalPages = readInt32(buf, 4);
    }
}

BPlusTree::~BPlusTree() {
    if (file.is_open()) {
        // Ensure metadata is saved
        char buf[PAGE_SIZE];
        std::memset(buf, 0, PAGE_SIZE);
        writeInt32(buf, 0, meta.rootPageId);
        writeInt32(buf, 4, meta.totalPages);
        writePage(0, buf);
        
        file.close();
    }
}

void BPlusTree::readPage(PageID pageId, char* buffer) {
    file.seekg(pageId * PAGE_SIZE, std::ios::beg);
    file.read(buffer, PAGE_SIZE);
    if (file.gcount() != PAGE_SIZE) {
        // Handle error or partial read (should not happen if logic correct)
        std::memset(buffer, 0, PAGE_SIZE);
    }
}

void BPlusTree::writePage(PageID pageId, const char* buffer) {
    file.seekp(pageId * PAGE_SIZE, std::ios::beg);
    file.write(buffer, PAGE_SIZE);
    file.flush();
}

PageID BPlusTree::allocatePage() {
    PageID newId = meta.totalPages++;
    // Update metadata on disk
    char buf[PAGE_SIZE];
    readPage(0, buf);
    writeInt32(buf, 4, meta.totalPages);
    writePage(0, buf);
    
    // Zero out new page
    std::memset(buf, 0, PAGE_SIZE);
    writePage(newId, buf);
    return newId;
}

PageID BPlusTree::findLeaf(KeyType key) {
    if (meta.rootPageId == INVALID_PAGE_ID) {
        return INVALID_PAGE_ID;
    }

    PageID currentId = meta.rootPageId;
    char buf[PAGE_SIZE];
    
    while (true) {
        readPage(currentId, buf);
        if (isLeaf(buf)) {
            return currentId;
        }

        // Internal Node Search
        int32_t numKeys = getNumKeys(buf);
        int i = 0;
        // Find first key >= search key
        while (i < numKeys && getInternalKey(buf, i) <= key) {
            i++;
        }
        
        currentId = getInternalPtr(buf, i);
    }
}

bool BPlusTree::readData(KeyType key, Tuple& outData) {
    PageID leafId = findLeaf(key);
    if (leafId == INVALID_PAGE_ID) return false;

    char buf[PAGE_SIZE];
    readPage(leafId, buf);
    
    int32_t numKeys = getNumKeys(buf);
    for (int i = 0; i < numKeys; ++i) {
        if (getLeafKey(buf, i) == key) {
            getLeafTuple(buf, i, outData);
            return true;
        }
    }
    return false;
}

bool BPlusTree::readRangeData(KeyType lowerKey, KeyType upperKey, int n, std::vector<Tuple>& result) {
    PageID leafId = findLeaf(lowerKey);
    if (leafId == INVALID_PAGE_ID) return false;

    char buf[PAGE_SIZE];
    readPage(leafId, buf);
    
    int count = 0;
    while (count < n) {
        int32_t numKeys = getNumKeys(buf);
        
        for (int i = 0; i < numKeys && count < n; ++i) {
            KeyType k = getLeafKey(buf, i);
            if (k >= lowerKey && k <= upperKey) {
                Tuple t;
                getLeafTuple(buf, i, t);
                result.push_back(t);
                count++;
            } else if (k > upperKey) {
                return result.size() > 0;
            }
        }
        
        int32_t nextLeaf = getNextLeaf(buf);
        if (nextLeaf == 0 || nextLeaf == INVALID_PAGE_ID) break; // 0 is usually metadata, so invalid for next leaf
        
        readPage(nextLeaf, buf);
    }
    return result.size() > 0;
}

bool BPlusTree::writeData(KeyType key, const Tuple& data) {
    // Check if exists
    Tuple temp;
    if (readData(key, temp)) return false; // Already exists

    if (meta.rootPageId == INVALID_PAGE_ID) {
        // Create root (Leaf)
        PageID rootId = allocatePage();
        meta.rootPageId = rootId;
        
        // Update metadata
        char metaBuf[PAGE_SIZE];
        readPage(0, metaBuf);
        writeInt32(metaBuf, 0, meta.rootPageId);
        writePage(0, metaBuf);
        
        // Init root
        char rootBuf[PAGE_SIZE];
        std::memset(rootBuf, 0, PAGE_SIZE);
        setIsLeaf(rootBuf, true);
        setNumKeys(rootBuf, 0);
        setParent(rootBuf, INVALID_PAGE_ID);
        setNextLeaf(rootBuf, INVALID_PAGE_ID);
        writePage(rootId, rootBuf);
    }

    PageID leafId = findLeaf(key);
    insertIntoLeaf(leafId, key, data);
    return true;
}

void BPlusTree::insertIntoLeaf(PageID leafId, KeyType key, const Tuple& tuple) {
    char buf[PAGE_SIZE];
    readPage(leafId, buf);
    int32_t numKeys = getNumKeys(buf);

    if (numKeys < MAX_KEYS_LEAF) {
        // Insert sorted
        int i = 0;
        while (i < numKeys && getLeafKey(buf, i) < key) i++;
        
        // Shift
        for (int j = numKeys; j > i; --j) {
            setLeafKey(buf, j, getLeafKey(buf, j-1));
            Tuple t;
            getLeafTuple(buf, j-1, t);
            setLeafTuple(buf, j, t);
        }
        
        setLeafKey(buf, i, key);
        setLeafTuple(buf, i, tuple);
        setNumKeys(buf, numKeys + 1);
        writePage(leafId, buf);
    } else {
        // Split Leaf
        PageID newLeafId = allocatePage();
        char newBuf[PAGE_SIZE];
        std::memset(newBuf, 0, PAGE_SIZE);
        setIsLeaf(newBuf, true);
        setParent(newBuf, getParent(buf));
        setNextLeaf(newBuf, getNextLeaf(buf));
        setNextLeaf(buf, newLeafId);
        
        // Gather all keys (N+1)
        // We have MAX_KEYS_LEAF keys in buf, plus 1 new one.
        // Total MAX_KEYS_LEAF + 1.
        // Split point: (N+1)/2
        
        // To simplify, let's use a temporary memory buffer for sorting
        struct Entry { KeyType k; Tuple t; };
        std::vector<Entry> entries;
        for(int k=0; k<numKeys; ++k) {
            Entry e;
            e.k = getLeafKey(buf, k);
            getLeafTuple(buf, k, e.t);
            entries.push_back(e);
        }
        Entry newEntry = {key, tuple};
        // Insert sorted
        auto it = std::lower_bound(entries.begin(), entries.end(), newEntry, [](const Entry& a, const Entry& b){
            return a.k < b.k;
        });
        entries.insert(it, newEntry);
        
        int total = entries.size();
        int split = total / 2;
        
        // Write first half to buf
        setNumKeys(buf, split);
        for(int k=0; k<split; ++k) {
            setLeafKey(buf, k, entries[k].k);
            setLeafTuple(buf, k, entries[k].t);
        }
        
        // Write second half to newBuf
        setNumKeys(newBuf, total - split);
        for(int k=split; k<total; ++k) {
            setLeafKey(newBuf, k - split, entries[k].k);
            setLeafTuple(newBuf, k - split, entries[k].t);
        }
        
        writePage(leafId, buf);
        writePage(newLeafId, newBuf);
        
        insertIntoParent(leafId, entries[split].k, newLeafId);
    }
}

void BPlusTree::insertIntoParent(PageID leftChildId, KeyType key, PageID rightChildId) {
    char leftBuf[PAGE_SIZE];
    readPage(leftChildId, leftBuf);
    PageID parentId = getParent(leftBuf);
    
    if (parentId == INVALID_PAGE_ID) {
        // Create new root
        PageID newRootId = allocatePage();
        char rootBuf[PAGE_SIZE];
        std::memset(rootBuf, 0, PAGE_SIZE);
        setIsLeaf(rootBuf, false);
        setNumKeys(rootBuf, 1);
        setParent(rootBuf, INVALID_PAGE_ID);
        
        setInternalPtr(rootBuf, 0, leftChildId);
        setInternalKey(rootBuf, 0, key);
        setInternalPtr(rootBuf, 1, rightChildId);
        
        writePage(newRootId, rootBuf);
        
        // Update children parents
        setParent(leftBuf, newRootId);
        writePage(leftChildId, leftBuf);
        
        char rightBuf[PAGE_SIZE];
        readPage(rightChildId, rightBuf);
        setParent(rightBuf, newRootId);
        writePage(rightChildId, rightBuf);
        
        // Update metadata
        meta.rootPageId = newRootId;
        char metaBuf[PAGE_SIZE];
        readPage(0, metaBuf);
        writeInt32(metaBuf, 0, meta.rootPageId);
        writePage(0, metaBuf);
        return;
    }
    
    char parentBuf[PAGE_SIZE];
    readPage(parentId, parentBuf);
    int32_t numKeys = getNumKeys(parentBuf);
    
    if (numKeys < MAX_KEYS_INTERNAL) {
        // Insert sorted
        int i = 0;
        while (i < numKeys && getInternalKey(parentBuf, i) < key) i++;
        
        // Shift keys and pointers
        // P0 K0 P1 K1 ...
        // We need to shift K[i]... and P[i+1]...
        for (int j = numKeys; j > i; --j) {
            setInternalKey(parentBuf, j, getInternalKey(parentBuf, j-1));
            setInternalPtr(parentBuf, j+1, getInternalPtr(parentBuf, j));
        }
        setInternalPtr(parentBuf, i+1, rightChildId);
        setInternalKey(parentBuf, i, key);
        setNumKeys(parentBuf, numKeys + 1);
        writePage(parentId, parentBuf);
    } else {
        // Split Internal Node
        PageID newInternalId = allocatePage();
        char newBuf[PAGE_SIZE];
        std::memset(newBuf, 0, PAGE_SIZE);
        setIsLeaf(newBuf, false);
        setParent(newBuf, getParent(parentBuf));
        
        // Gather keys and pointers
        // Existing: P0 K0 P1 ... K(N-1) P(N)
        // New item: Key, RightChild (LeftChild is already in P array or is P(N))
        // We are inserting (Key, RightChild) after LeftChild.
        
        struct Item { KeyType k; PageID p; };
        std::vector<Item> items; // Stores K[i], P[i+1]
        // P0 is separate
        
        // Find position
        int i = 0;
        while (i < numKeys && getInternalKey(parentBuf, i) < key) i++;
        
        // Construct full list of keys and pointers
        // P0, K0, P1, K1, ...
        std::vector<KeyType> allKeys;
        std::vector<PageID> allPtrs;
        
        allPtrs.push_back(getInternalPtr(parentBuf, 0));
        for(int k=0; k<numKeys; ++k) {
            allKeys.push_back(getInternalKey(parentBuf, k));
            allPtrs.push_back(getInternalPtr(parentBuf, k+1));
        }
        
        // Insert new key and ptr
        allKeys.insert(allKeys.begin() + i, key);
        allPtrs.insert(allPtrs.begin() + i + 1, rightChildId);
        
        // Split
        // Total keys = N+1.
        // Mid key goes up.
        // Left node: P0 ... K[mid-1] P[mid]
        // Right node: P[mid+1] ...
        
        int totalKeys = allKeys.size();
        int mid = totalKeys / 2;
        KeyType upKey = allKeys[mid];
        
        // Write Left (parentBuf)
        setNumKeys(parentBuf, mid);
        setInternalPtr(parentBuf, 0, allPtrs[0]);
        for(int k=0; k<mid; ++k) {
            setInternalKey(parentBuf, k, allKeys[k]);
            setInternalPtr(parentBuf, k+1, allPtrs[k+1]);
        }
        
        // Write Right (newBuf)
        int rightKeys = totalKeys - mid - 1;
        setNumKeys(newBuf, rightKeys);
        setInternalPtr(newBuf, 0, allPtrs[mid+1]);
        for(int k=0; k<rightKeys; ++k) {
            setInternalKey(newBuf, k, allKeys[mid + 1 + k]);
            setInternalPtr(newBuf, k+1, allPtrs[mid + 1 + k + 1]);
            
            // Update parent pointers for children moved to new node
            PageID childId = allPtrs[mid + 1 + k + 1]; // P[k+1] in new node
            // Also P0 of new node
            if (k==0) {
                 PageID childP0 = allPtrs[mid+1];
                 char childBuf[PAGE_SIZE];
                 readPage(childP0, childBuf);
                 setParent(childBuf, newInternalId);
                 writePage(childP0, childBuf);
            }
            
            char childBuf[PAGE_SIZE];
            readPage(childId, childBuf);
            setParent(childBuf, newInternalId);
            writePage(childId, childBuf);
        }

        if (rightKeys == 0) {
             PageID childP0 = allPtrs[mid+1];
             char childBuf[PAGE_SIZE];
             readPage(childP0, childBuf);
             setParent(childBuf, newInternalId);
             writePage(childP0, childBuf);
        }

        writePage(parentId, parentBuf);
        writePage(newInternalId, newBuf);
        
        insertIntoParent(parentId, upKey, newInternalId);
    }
}

bool BPlusTree::deleteData(KeyType key) {
    PageID leafId = findLeaf(key);
    if (leafId == INVALID_PAGE_ID) return false;
    
    char buf[PAGE_SIZE];
    readPage(leafId, buf);
    int32_t numKeys = getNumKeys(buf);
    
    int i = 0;
    while (i < numKeys && getLeafKey(buf, i) != key) i++;
    
    if (i == numKeys) return false; // Not found
    
    // Shift to delete
    for (int j = i; j < numKeys - 1; ++j) {
        setLeafKey(buf, j, getLeafKey(buf, j+1));
        Tuple t;
        getLeafTuple(buf, j+1, t);
        setLeafTuple(buf, j, t);
    }
    setNumKeys(buf, numKeys - 1);
    writePage(leafId, buf);
    
    return true;
}

void BPlusTree::print() {
    // BFS or DFS print
    if (meta.rootPageId == INVALID_PAGE_ID) {
        std::cout << "Empty Tree" << std::endl;
        return;
    }
    printTree(meta.rootPageId, 0);
}

void BPlusTree::printTree(PageID pageId, int level) {
    char buf[PAGE_SIZE];
    readPage(pageId, buf);
    
    std::string indent(level * 2, ' ');
    std::cout << indent << "Page " << pageId << " (Leaf: " << isLeaf(buf) << ", Keys: " << getNumKeys(buf) << "): ";
    
    int n = getNumKeys(buf);
    if (isLeaf(buf)) {
        for(int i=0; i<n; ++i) {
            std::cout << getLeafKey(buf, i) << " ";
        }
        std::cout << " -> Next: " << getNextLeaf(buf);
    } else {
        for(int i=0; i<n; ++i) {
            std::cout << getInternalKey(buf, i) << " ";
        }
    }
    std::cout << std::endl;
    
    if (!isLeaf(buf)) {
        // Recurse
        // P0
        printTree(getInternalPtr(buf, 0), level + 1);
        for(int i=0; i<n; ++i) {
            printTree(getInternalPtr(buf, i+1), level + 1);
        }
    }
}
