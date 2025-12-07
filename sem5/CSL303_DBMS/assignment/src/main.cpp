#include "bplustree.h"
#include <iostream>
#include <vector>
#include <string>
#include <cassert>
#include <cstring>
#include <chrono>
#include <random>
#include <iomanip>
#include <sstream>

void printTuple(const Tuple& t) {
    // Assuming string data for demo
    std::cout << "Data: " << std::string((char*)t.data, 20) << "..." << std::endl;
}

class Timer {
    std::chrono::high_resolution_clock::time_point start;
public:
    Timer() { reset(); }
    void reset() { start = std::chrono::high_resolution_clock::now(); }
    double elapsed() {
        auto end = std::chrono::high_resolution_clock::now();
        return std::chrono::duration<double>(end - start).count();
    }
};

struct BenchmarkResult {
    int N;
    double insertTime;
    double searchTime;
    double rangeTime;
};

BenchmarkResult runBenchmark(int N) {
    std::cout << "\n=========================================" << std::endl;
    std::cout << "Running Benchmark for N = " << N << std::endl;
    std::cout << "=========================================" << std::endl;

    std::string filename = "benchmark_" + std::to_string(N) + ".dat";
    remove(filename.c_str());
    
    BPlusTree tree(filename);
    Timer timer;

    // 1. Insertion
    std::cout << "Inserting " << N << " records..." << std::flush;
    timer.reset();
    for(int i=0; i<N; ++i) {
        Tuple t;
        // Minimal data generation overhead
        *(int*)t.data = i; 
        tree.writeData(i, t);
        
        if (i > 0 && i % (N/10) == 0) std::cout << "." << std::flush;
    }
    double insertTime = timer.elapsed();
    std::cout << " Done!" << std::endl;
    std::cout << "Insertion Time: " << std::fixed << std::setprecision(4) << insertTime << " s (" 
              << (N/insertTime) << " ops/s)" << std::endl;

    // 2. Point Search (Random)
    int searchOps = 10000;
    if (searchOps > N) searchOps = N;
    
    std::cout << "Performing " << searchOps << " random point searches..." << std::flush;
    
    std::vector<int> keysToSearch(searchOps);
    std::mt19937 rng(42);
    std::uniform_int_distribution<int> dist(0, N-1);
    for(int& k : keysToSearch) k = dist(rng);
    
    timer.reset();
    int foundCount = 0;
    for(int k : keysToSearch) {
        Tuple t;
        if(tree.readData(k, t)) foundCount++;
    }
    double searchTime = timer.elapsed();
    std::cout << " Done!" << std::endl;
    std::cout << "Point Search Time (" << searchOps << " ops): " << searchTime << " s (" 
              << (searchOps/searchTime) << " ops/s)" << std::endl;
    
    // 3. Range Search
    int rangeOps = 100;
    int rangeSize = 100;
    std::cout << "Performing " << rangeOps << " range searches (size ~" << rangeSize << ")..." << std::flush;
    
    timer.reset();
    for(int i=0; i<rangeOps; ++i) {
        int start = dist(rng);
        if (start > N - rangeSize) start = N - rangeSize;
        std::vector<Tuple> results;
        tree.readRangeData(start, start + rangeSize, rangeSize + 10, results);
    }
    double rangeTime = timer.elapsed();
    std::cout << " Done!" << std::endl;
    std::cout << "Range Search Time (" << rangeOps << " ops): " << rangeTime << " s (" 
              << (rangeOps/rangeTime) << " ops/s)" << std::endl;

    // Cleanup
    remove(filename.c_str());
    return {N, insertTime, searchTime, rangeTime};
}

void runScriptMode() {
    BPlusTree tree("index.dat");
    std::string line;
    
    while (std::getline(std::cin, line)) {
        std::stringstream ss(line);
        std::string command;
        ss >> command;

        if (command == "INSERT") {
            int64_t key;
            std::string dataStr;
            ss >> key >> dataStr;
            
            Tuple t;
            std::memset(t.data, 0, TUPLE_SIZE);
            std::strncpy((char*)t.data, dataStr.c_str(), TUPLE_SIZE - 1);
            
            if (tree.writeData(key, t)) {
                std::cout << "Inserted " << key << std::endl;
            } else {
                std::cout << "Failed to insert " << key << std::endl;
            }
        } 
        else if (command == "DELETE") {
            int64_t key;
            ss >> key;
            if (tree.deleteData(key)) {
                std::cout << "Deleted " << key << std::endl;
            } else {
                std::cout << "Failed to delete " << key << std::endl;
            }
        } 
        else if (command == "SEARCH") {
            int64_t key;
            ss >> key;
            Tuple t;
            if (tree.readData(key, t)) {
                std::cout << "Found " << key << ": " << (char*)t.data << std::endl;
            } else {
                std::cout << "Not Found " << key << std::endl;
            }
        }
        else if (command == "RANGE") {
            int64_t start, end;
            ss >> start >> end;
            std::vector<Tuple> results;
            tree.readRangeData(start, end, 1000, results);
            
            std::cout << "Range [" << start << ", " << end << "]: Found " << results.size() << " items" << std::endl;
            for(const auto& t : results) {
                std::cout << "  " << (char*)t.data << std::endl;
            }
        }
        else if (command == "EXIT") {
            break;
        }
    }
}

void testBasic() {
    std::string filename = "index.dat";
    // Remove existing file
    remove(filename.c_str());
    
    BPlusTree tree(filename);
    
    std::cout << "--- Testing Insert ---" << std::endl;
    for (int i = 0; i < 100; ++i) {
        Tuple t;
        std::string s = "Value " + std::to_string(i);
        std::memset(t.data, 0, TUPLE_SIZE);
        std::strcpy((char*)t.data, s.c_str());
        
        bool res = tree.writeData(i, t);
        if (!res) std::cout << "Failed to insert " << i << std::endl;
    }
    std::cout << "Inserted 0-99" << std::endl;
    
    std::cout << "--- Testing Read ---" << std::endl;
    for (int i = 0; i < 100; ++i) {
        Tuple t;
        bool res = tree.readData(i, t);
        if (!res) {
            std::cout << "Failed to read " << i << std::endl;
        } else {
            std::string s((char*)t.data);
            if (s != "Value " + std::to_string(i)) {
                std::cout << "Data mismatch for " << i << std::endl;
            }
        }
    }
    std::cout << "Read verification complete." << std::endl;
    
    std::cout << "--- Testing Range Read ---" << std::endl;
    std::vector<Tuple> rangeRes;
    tree.readRangeData(10, 19, 100, rangeRes);
    std::cout << "Range 10-19 size: " << rangeRes.size() << " (Expected 10)" << std::endl;
    // for(const auto& t : rangeRes) {
    //     printTuple(t);
    // }
    
    std::cout << "--- Testing Delete ---" << std::endl;
    tree.deleteData(50);
    Tuple t;
    if (tree.readData(50, t)) {
        std::cout << "Error: 50 should be deleted" << std::endl;
    } else {
        std::cout << "50 deleted successfully." << std::endl;
    }
    
    // Re-insert
    Tuple t50;
    std::string s50 = "Value 50 New";
    std::memset(t50.data, 0, TUPLE_SIZE);
    std::strcpy((char*)t50.data, s50.c_str());
    tree.writeData(50, t50);
    if (tree.readData(50, t)) {
        std::cout << "50 re-inserted successfully." << std::endl;
    }
}

void testLargeScale() {
    std::cout << "--- Large Scale Test ---" << std::endl;
    std::string filename = "index_large.dat";
    remove(filename.c_str());
    BPlusTree tree(filename);
    
    int N = 5000;
    for(int i=0; i<N; ++i) {
        Tuple t;
        std::memset(t.data, 0, TUPLE_SIZE);
        sprintf((char*)t.data, "V%d", i);
        tree.writeData(i * 2, t); // 0, 2, 4...
    }
    std::cout << "Inserted " << N << " items." << std::endl;
    
    // Check random
    Tuple t;
    if(tree.readData(100, t)) std::cout << "Found 100" << std::endl;
    else std::cout << "Error: 100 not found" << std::endl;
    
    if(tree.readData(101, t)) std::cout << "Error: Found 101" << std::endl;
    else std::cout << "Correct: 101 not found" << std::endl;
}

int main(int argc, char** argv) {
    if (argc > 1) {
        std::string arg = argv[1];
        if (arg == "large") {
            testLargeScale();
        } else if (arg == "benchmark") {
            // Run a suite of benchmarks
            std::vector<BenchmarkResult> results;
            results.push_back(runBenchmark(10000));    // 10k
            results.push_back(runBenchmark(100000));   // 100k
            results.push_back(runBenchmark(1000000));  // 1M
            // runBenchmark(10000000); // 10M - Uncomment if you have time/disk space (approx 1GB)
            
            std::cout << "\n\n================================================================================\n";
            std::cout << "                              BENCHMARK SUMMARY                                 \n";
            std::cout << "================================================================================\n";
            std::cout << std::left << std::setw(15) << "Scale" 
                      << std::setw(20) << "Insert (s)" 
                      << std::setw(20) << "Read (s)" 
                      << std::setw(20) << "Range (s)" << std::endl;
            std::cout << "--------------------------------------------------------------------------------\n";
            for(const auto& res : results) {
                std::cout << std::left << std::setw(15) << res.N 
                          << std::setw(20) << std::fixed << std::setprecision(4) << res.insertTime 
                          << std::setw(20) << res.searchTime 
                          << std::setw(20) << res.rangeTime << std::endl;
            }
            std::cout << "================================================================================\n";
        } else if (arg == "script") {
            runScriptMode();
        } else {
            // Try to parse as number
            try {
                int n = std::stoi(arg);
                runBenchmark(n);
            } catch (...) {
                testBasic();
            }
        }
    } else {
        testBasic();
    }
    return 0;
}
