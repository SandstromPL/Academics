-- 
-- Lab 9: Railway Connectivity Queries (Optimized Version)
-- Uses supporting indexes to speed up schedule self-joins
-- Designed for railways.dump (MyISAM schedule + terminus)
-- 

-- 
-- PART 0 : SPEED OPTIMIZATION (recommended)
-- 

-- Indexes for faster joins on schedule
ALTER TABLE schedule ADD INDEX idx_station (station);
ALTER TABLE schedule ADD INDEX idx_train (train);
ALTER TABLE schedule ADD INDEX idx_arr (arrdate, arr);
ALTER TABLE schedule ADD INDEX idx_dep (depdate, dep);

-- Index for terminus
ALTER TABLE terminus ADD INDEX idx_term_station (station);

-- 
-- PART 1: All pairs of terminus stations (A,B)
-- Reachable with at most TWO changes (0, 1, or 2)
-- 

-- 
-- 0 CHANGES (Direct)
-- 
SELECT
    T1.station AS StationA,
    T2.station AS StationB,
    S1.train AS Train1,
    NULL AS Change1,
    NULL AS Train2,
    NULL AS Change2,
    NULL AS Train3
FROM schedule S1
JOIN schedule S2 ON S1.train = S2.train
JOIN terminus T1 ON T1.station = S1.station
JOIN terminus T2 ON T2.station = S2.station
WHERE S1.station <> S2.station
  AND S1.dep IS NOT NULL
  AND S2.arr IS NOT NULL
  AND (S2.arrdate > S1.depdate
       OR (S2.arrdate = S1.depdate AND S2.arr > S1.dep));

-- 
-- 1 CHANGE
-- 
SELECT
    T1.station AS StationA,
    T2.station AS StationB,
    S1.train AS Train1,
    S2.station AS Change1,
    S3.train AS Train2,
    NULL AS Change2,
    NULL AS Train3
FROM schedule S1
JOIN schedule S2 ON S1.train = S2.train
JOIN schedule S3 ON S2.station = S3.station
JOIN schedule S4 ON S3.train = S4.train
JOIN terminus T1 ON T1.station = S1.station
JOIN terminus T2 ON T2.station = S4.station
WHERE S1.station <> S2.station
  AND S2.station <> S4.station
  AND S1.train <> S3.train
  AND S2.arrdate < S3.depdate
  OR (S2.arrdate = S3.depdate AND S2.arr < S3.dep);

-- 
-- 2 CHANGES
-- 
SELECT
    T1.station AS StationA,
    T2.station AS StationB,
    S1.train AS Train1,
    S2.station AS Change1,
    S3.train AS Train2,
    S4.station AS Change2,
    S5.train AS Train3
FROM schedule S1
JOIN schedule S2 ON S1.train = S2.train
JOIN schedule S3 ON S2.station = S3.station
JOIN schedule S4 ON S3.train = S4.train
JOIN schedule S5 ON S4.station = S5.station
JOIN schedule S6 ON S5.train = S6.train
JOIN terminus T1 ON T1.station = S1.station
JOIN terminus T2 ON T2.station = S6.station
WHERE S1.station <> S2.station
  AND S2.station <> S4.station
  AND S4.station <> S6.station
  AND S1.train <> S3.train
  AND S3.train <> S5.train
  AND S2.arrdate < S3.depdate
  AND S4.arrdate < S5.depdate;

-- 
-- PART 2: Allowing up to THREE changes (0,1,2,3)
-- 

-- (0 and 1 and 2 change queries repeated from Part 1)
-- To avoid duplication inside the submission, we include them again.

-- 
-- 0 CHANGES
-- 
SELECT
    T1.station AS StationA,
    T2.station AS StationB,
    S1.train AS Train1,
    NULL, NULL, NULL, NULL
FROM schedule S1
JOIN schedule S2 ON S1.train = S2.train
JOIN terminus T1 ON T1.station = S1.station
JOIN terminus T2 ON T2.station = S2.station
WHERE S1.station <> S2.station
  AND S1.dep IS NOT NULL
  AND S2.arr IS NOT NULL
  AND (S2.arrdate > S1.depdate
       OR (S2.arrdate = S1.depdate AND S2.arr > S1.dep))

UNION ALL

-- 
-- 1 CHANGE
-- 
SELECT
    T1.station AS StationA,
    T2.station AS StationB,
    S1.train,
    S2.station AS Change1,
    S3.train,
    NULL,
    NULL
FROM schedule S1
JOIN schedule S2 ON S1.train = S2.train
JOIN schedule S3 ON S2.station = S3.station
JOIN schedule S4 ON S3.train = S4.train
JOIN terminus T1 ON T1.station = S1.station
JOIN terminus T2 ON T2.station = S4.station
WHERE S1.station <> S2.station
  AND S2.station <> S4.station
  AND S1.train <> S3.train
  AND (S2.arrdate < S3.depdate
       OR (S2.arrdate = S3.depdate AND S2.arr < S3.dep))

UNION ALL

-- 
-- 2 CHANGES
-- 
SELECT
    T1.station AS StationA,
    T2.station AS StationB,
    S1.train,
    S2.station AS Change1,
    S3.train,
    S4.station AS Change2,
    S5.train
FROM schedule S1
JOIN schedule S2 ON S1.train = S2.train
JOIN schedule S3 ON S2.station = S3.station
JOIN schedule S4 ON S3.train = S4.train
JOIN schedule S5 ON S4.station = S5.station
JOIN schedule S6 ON S5.train = S6.train
JOIN terminus T1 ON T1.station = S1.station
JOIN terminus T2 ON T2.station = S6.station
WHERE S1.station <> S2.station
  AND S2.station <> S4.station
  AND S4.station <> S6.station
  AND S1.train <> S3.train
  AND S3.train <> S5.train
  AND (S2.arrdate < S3.depdate)
  AND (S4.arrdate < S5.depdate)

UNION ALL

-- 
-- 3 CHANGES
-- 
SELECT
    T1.station AS StationA,
    T2.station AS StationB,
    S1.train,
    S2.station AS Change1,
    S3.train,
    S4.station AS Change2,
    S5.train,
    S6.station AS Change3,
    S7.train AS Train4
FROM schedule S1
JOIN schedule S2 ON S1.train = S2.train
JOIN schedule S3 ON S2.station = S3.station
JOIN schedule S4 ON S3.train = S4.train
JOIN schedule S5 ON S4.station = S5.station
JOIN schedule S6 ON S5.train = S6.train
JOIN schedule S7 ON S6.station = S7.station
JOIN schedule S8 ON S7.train = S8.train
JOIN terminus T1 ON T1.station = S1.station
JOIN terminus T2 ON T2.station = S8.station
WHERE S1.station <> S2.station
  AND S2.station <> S4.station
  AND S4.station <> S6.station
  AND S6.station <> S8.station
  AND S1.train <> S3.train
  AND S3.train <> S5.train
  AND S5.train <> S7.train
  AND S2.arrdate < S3.depdate
  AND S4.arrdate < S5.depdate
  AND S6.arrdate < S7.depdate;
