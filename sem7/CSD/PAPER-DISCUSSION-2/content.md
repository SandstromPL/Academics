# Paper Discussion 2: From Bigtable to the Lakehouse

**Name:** Paritosh Lahre
**ID:** 12341550
**Course:** CSL559 (Computer System Design)

Seven papers on how large-scale data systems are built: how to store huge data, how to query it fast, and how to run all of it in the cloud on open file formats.

**Slides:** title, big picture, 2 slides per paper (problem + idea + key terms, then how it works + results + takeaway), common ideas, thank you. 18 slides total.

---

## The big picture (timeline)

| Year | Paper | One-line summary |
|------|-------|------------------|
| 2006 | Bigtable (Google) | Store huge structured data on thousands of machines |
| 2020 | Dremel (Google) | Fast SQL on huge data, storage split from compute |
| 2020 | Snowflake | Elastic data warehouse built on cloud storage |
| 2021 | Lakehouse (Databricks) | One open system for both BI (SQL) and ML |
| 2024 | BigLake (Google) | BigQuery's lakehouse that works across many clouds |
| 2024 | AQE (Databricks) | Fix the query plan while the query is running |
| 2024 | ClickHouse | Very fast open-source engine for real-time analytics |

**The story:** first store big data, then query it fast, then split storage from compute, then put everything on open files in the cloud.

---

## 1. Bigtable

**Paper:** Bigtable: A Distributed Storage System for Structured Data. OSDI 2006, Google.

**Problem**
- Google had petabytes of data: web pages, Google Earth images, Google Analytics data and more.
- Normal relational databases could not spread this data over thousands of cheap machines.
- Different apps needed different things: some needed big batch jobs, some needed very fast single reads.

**Main idea**
- A huge, sparse, sorted map. Each value is found by (row key, column key, timestamp).
- It does not give full SQL. It gives a simple data model, and the app decides how to lay out its data.

**Key terms**
- **Tablet:** a range of rows; the unit of load balancing
- **Memtable:** recent writes kept in memory
- **SSTable:** a sorted, read-only file stored on GFS

**How it works**
- Rows are kept in sorted order. A table is split into row ranges called **tablets** (about 100-200 MB each).
- One **master** gives tablets to many **tablet servers** and balances the load.
- Data files are stored on **GFS** (Google File System). **Chubby** (a lock service) makes sure there is only one master and keeps the root location.
- Columns are grouped into **column families**. Each cell can keep many versions by timestamp.
- **Write path:** a write goes to a commit log and to an in-memory table (**memtable**). When the memtable is full, it is saved to disk as an **SSTable** file.
- **Compactions** merge SSTables in the background.
- **Read speed-ups:** Bloom filters (skip files that do not have the row), caching, locality groups, compression.

**Results**
- Used by more than 60 Google products, including web indexing, Google Earth and Google Analytics.
- Clusters run on thousands of servers and store petabytes of data.
- Inspired open-source systems such as HBase and Cassandra.

**Key takeaway:** A simple data model plus smart storage (logs, memtables, SSTables) is enough to scale storage to thousands of machines.

---

## 2. Dremel

**Paper:** Dremel: A Decade of Interactive SQL Analysis at Web Scale. VLDB 2020, Google. (Looks back at the original 2010 Dremel paper.)

**Problem**
- Analysts wanted answers in seconds over trillions of rows.
- MapReduce jobs took minutes or hours, which is too slow for exploring data.

**Main idea**
- Run SQL on data where it already lives (**in situ** analysis), using **column storage** and a big shared pool of machines.

**Key terms**
- **In situ:** query files in place, with no loading step
- **Disaggregation:** storage and compute scale on their own
- **Serverless:** users never set up or manage machines

**How it works**
- **SQL:** Dremel's query language grew into standard SQL, shared with other Google products like Spanner.
- **Storage split from compute:** data sits in the shared file system (GFS, later Colossus). Compute servers can scale on their own.
- **Column format for nested data:** each column is stored on its own, with *repetition* and *definition levels* so nested records can be rebuilt. Only needed columns are read.
- **Serving tree:** a root server splits the query, middle servers combine results, leaf servers scan data.
- **In-memory shuffle:** a separate memory layer for big joins and group-bys.
- **Serverless:** users just send queries. They never set up or manage machines.

**Results**
- Became the engine behind **Google BigQuery** (launched 2010).
- Interactive queries over petabytes of data.
- Its ideas (columnar, serverless, storage split from compute, in situ analysis) are now standard across the industry.

**Key takeaway:** Column storage plus a large shared pool of compute makes SQL on huge data feel interactive.

---

## 3. Snowflake

**Paper:** Building An Elastic Query Engine on Disaggregated Storage. NSDI 2020, Snowflake + Cornell University.

**Problem**
- Old data warehouses are **shared-nothing**: each node owns part of the data.
- Adding or removing nodes means moving lots of data around.
- Customers run mixed workloads, so hardware is either too much (wasted) or too little (slow).

**Main idea**
- Keep tables in cloud storage (Amazon S3). Run queries on separate groups of machines called **virtual warehouses** that can grow or shrink at any time.

**Key terms**
- **Virtual warehouse:** a group of VMs that runs queries
- **Ephemeral storage:** temp data kept on compute nodes
- **Work stealing:** an idle node takes tasks from a busy one

**How it works**
- **Three layers:** cloud services (metadata, query planning, scheduling), compute (virtual warehouses made of VMs), storage (S3).
- **Ephemeral storage:** Snowflake built its own distributed storage on the compute nodes for temporary (intermediate) data, like data exchanged during joins.
- The same ephemeral storage also **caches table files** from S3, so repeated reads are fast.
- **Consistent hashing** decides which node caches which file. When nodes are added, the cache is updated lazily, without a big reshuffle.
- **Work stealing:** a free node can take tasks from a busy node, which helps with skew.
- The paper studies about **70 million queries** over **14 days** (February 2018).

**Results / findings**
- Query mix: about 28% read-only, 13% write-only, 59% read-write.
- Temporary data size changes a lot between queries (up to terabytes) and does not follow input size.
- Cache hit rate on table data is about 60-80%, even with small local storage.
- About 20% of clusters use elastic scaling.
- Open problems: split compute from ephemeral storage too, handle deeper storage tiers, and deal with per-second cloud pricing.

**Key takeaway:** Splitting storage from compute gives elasticity, but you still need a fast layer in the middle (ephemeral storage and caching) to keep queries fast.

---

## 4. Lakehouse

**Paper:** Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics. CIDR 2021, Databricks.

**Problem**
- Most companies use a **two-tier** setup: a **data lake** (cheap files in open formats) plus a **data warehouse** (fast SQL).
- Data is copied from the lake into the warehouse with ETL jobs. This causes:
  - stale data (the warehouse is behind),
  - extra cost (two copies),
  - more failure points,
  - poor support for machine learning (ML tools cannot easily read warehouse data).

**Main idea**
- One system: open files (like Apache Parquet) on cheap cloud storage, plus a **metadata layer** that adds warehouse features on top.

**Key terms**
- **Data lake:** raw files in cloud object storage
- **ACID:** safe, all-or-nothing updates
- **Delta Lake:** a transaction log on top of Parquet files

**How it works**
- **Metadata layer** (Delta Lake, Apache Iceberg, Apache Hudi): keeps a transaction log, so you get ACID transactions, table versions (time travel) and schema checks.
- **Speed without a closed format:** caching, extra data such as min/max stats for each file, and good data layout (for example Z-order) to skip files.
- **Same data for SQL and ML:** ML tools read the same tables directly through DataFrame APIs.

**Results**
- On the TPC-DS benchmark, Databricks' Delta Engine was competitive with popular cloud data warehouses, at lower cost.

**Key takeaway:** You can get warehouse features (transactions, speed, governance) directly on open files, so one copy of data serves both BI and ML.

---

## 5. BigLake

**Paper:** BigLake: BigQuery's Evolution toward a Multi-Cloud Lakehouse. SIGMOD 2024, Google.

**Problem**
- Customer data is stored in open formats (Parquet, Iceberg) on Google Cloud Storage, AWS S3 and Azure.
- Customers want BigQuery's security and speed on this data, and also want engines like Spark to use the same data safely.

**Main idea**
- Bring BigQuery's security rules and fast query engine to open-format data, in any cloud.

**Key terms**
- **Fine-grained security:** access control per row and column
- **Apache Iceberg:** an open table format
- **Object table:** a table view over images or documents

**How it works**
- **BigLake tables:** row-level and column-level security on files in object storage. Users do not need direct access to the files.
- **Storage Read / Write APIs:** Spark, Presto and other engines read and write through these APIs, and the same security rules apply.
- **Metadata caching:** file and stats info is cached so queries can skip files and plan faster.
- **BigLake Managed Tables:** fully managed tables that use the Apache Iceberg format.
- **Object tables:** treat unstructured files (images, documents) as tables and run ML inference from SQL.
- **BigQuery Omni:** runs the Dremel engine inside AWS and Azure, so data does not need to be moved. Cross-cloud joins are possible.

**Results**
- Read API optimizations gave about 5x faster Spark queries.
- Works across three clouds: Google Cloud, AWS and Azure.
- Cross-cloud joins without copying data.

**Key takeaway:** A lakehouse can be multi-cloud: one place to set security rules and query data, wherever it is stored.

---

## 6. Adaptive Query Execution (AQE)

**Paper:** Adaptive and Robust Query Execution for Lakehouses at Scale. VLDB 2024, Databricks.

**Problem**
- In a lakehouse, table statistics are often missing or out of date (raw data, fast ingestion, external tables, nested schemas).
- Size guesses for filters, joins and user-defined functions (UDFs) are often wrong.
- A fixed query plan made at the start can then cause heavy data movement, disk spill and memory pressure.

**Main idea**
- Do not trust the first plan. When a stage of the query finishes, use the **real data sizes** to re-plan the rest of the query.

**Key terms**
- **Shuffle:** moving data between machines by key
- **Broadcast join:** send the small table to every machine
- **Skew:** one partition much bigger than the rest

**How it works**
- The plan is cut into **query stages** at natural break points (shuffle and broadcast).
- When a stage finishes, AQE collects exact stats and runs the optimizer again on the remaining plan.
- Main rules:
  - **Coalesce shuffle partitions:** merge many tiny partitions into fewer, right-sized ones.
  - **Join re-selection:** switch join type, for example sort-merge join to broadcast hash join when one side turns out small.
  - **Skew join handling:** split very large (skewed) partitions into smaller pieces.
  - **Shuffle elimination fallback:** go back safely when an earlier choice turns out bad.
- Users can see how the plan changed in the query UI, which helps debugging.

**Results**
- Up to **25x** speedup on a single query (TPC-DS without stats).
- Up to **1.72x** total speedup (TPC-H, scale factor 3000).
- Median overhead under 1%.
- Running in production at Databricks for several years, on billions of queries and exabytes of data per day.

**Key takeaway:** When you cannot trust statistics, measure at run time and fix the plan as you go.

---

## 7. ClickHouse

**Paper:** ClickHouse - Lightning Fast Analytics for Everyone. VLDB 2024, ClickHouse Inc.

**Problem**
- Teams need real-time analytics on huge, fast-growing data like logs, events and clicks.
- Answers must come back very fast (milliseconds to seconds) while new data keeps coming in.

**Main idea**
- A column-oriented database built for raw speed: a smart storage format plus vectorized, parallel execution.

**Key terms**
- **Part:** a sorted, read-only chunk made by one insert
- **Granule:** 8192 rows, one entry in the sparse index
- **SIMD:** one CPU instruction works on many values

**How it works**
- **MergeTree storage:** each insert creates a small sorted **part**. Parts are merged in the background (similar to an LSM tree).
- **Sparse primary index:** one index entry per granule of 8192 rows, so the index stays small. **Skipping indexes** (min/max, sets, Bloom filters) help skip data.
- **Merge-time transforms:** during merges, rows can be replaced (latest version), pre-aggregated, or deleted when old (TTL).
- **Idempotent inserts and replication** for safe writes.
- **Vectorized execution with SIMD**, running in parallel on all cores and across many nodes.
- **Integration:** can read many file formats and query outside systems such as S3 and MySQL directly.

**Results**
- Open source since 2016 and widely used.
- Among the fastest systems on ClickBench and other analytics benchmarks.

**Key takeaway:** Careful engineering at every level (storage layout, indexes, SIMD execution) gives very fast analytics on a single, simple system.

---

## Common ideas across the papers

1. **Split storage and compute:** scale each one on its own. (Dremel, Snowflake, BigLake)
2. **Store data by column:** read only the columns you need and compress well. (Dremel, ClickHouse, Parquet in Lakehouse)
3. **Open formats, one copy of data:** many engines share the same files. (Lakehouse, BigLake, AQE)
4. **Adapt at run time:** use real numbers, not guesses. (AQE re-planning, Snowflake work stealing and elasticity)

**Discussion question:** Is the separate data warehouse going away, or will both models live side by side?

*(AI used for making the presentation)*
