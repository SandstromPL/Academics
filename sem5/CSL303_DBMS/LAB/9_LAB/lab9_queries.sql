-- SQL Queries for Lab Sheet 9: Optimization with DBMS

-- Part 1: Find all pairs of terminus stations (A,B) such that one can go from A to B with at most two changes of train.
-- Output format: (StationA, StationB, Train1, Change1, Train2, Change2, Train3)
-- If direct, Change1, Train2, Change2, Train3 are NULL.
-- If one change, Change2, Train3 are NULL.

-- Query for 0 changes (direct train)
SELECT
    T1.station AS StationA,
    T2.station AS StationB,
    S1.train AS Train1,
    NULL AS Change1,
    NULL AS Train2,
    NULL AS Change2,
    NULL AS Train3
FROM
    schedule S1
JOIN
    schedule S2 ON S1.train = S2.train
JOIN
    terminus T1 ON S1.station = T1.station
JOIN
    terminus T2 ON S2.station = T2.station
WHERE
    S1.station != S2.station
    AND S1.dep IS NOT NULL
    AND S2.arr IS NOT NULL
    AND (
        (S2.arrdate > S1.depdate)
        OR
        (S2.arrdate = S1.depdate AND S2.arr > S1.dep)
    )

UNION ALL

-- Query for 1 change
SELECT
    T1.station AS StationA,
    T2.station AS StationB,
    S1.train AS Train1,
    S2.station AS Change1,
    S3.train AS Train2,
    NULL AS Change2,
    NULL AS Train3
FROM
    schedule S1 -- Train1 departs from StationA
JOIN
    schedule S2 ON S1.train = S2.train -- Train1 arrives at Change1
JOIN
    schedule S3 ON S2.station = S3.station -- Train2 departs from Change1
JOIN
    schedule S4 ON S3.train = S4.train -- Train2 arrives at StationB
JOIN
    terminus T1 ON S1.station = T1.station
JOIN
    terminus T2 ON S4.station = T2.station
WHERE
    S1.station != S2.station
    AND S2.station != S4.station
    AND S1.station != S4.station
    AND S1.train != S3.train
    AND S1.dep IS NOT NULL
    AND S2.arr IS NOT NULL
    AND S3.dep IS NOT NULL
    AND S4.arr IS NOT NULL
    AND (
        (S2.arrdate < S3.depdate)
        OR
        (S2.arrdate = S3.depdate AND S2.arr < S3.dep)
    )
    AND (
        (S4.arrdate > S3.depdate)
        OR
        (S4.arrdate = S3.depdate AND S4.arr > S3.dep)
    )

UNION ALL

-- Query for 2 changes
SELECT
    T1.station AS StationA,
    T2.station AS StationB,
    S1.train AS Train1,
    S2.station AS Change1,
    S3.train AS Train2,
    S4.station AS Change2,
    S5.train AS Train3
FROM
    schedule S1 -- Train1 departs from StationA
JOIN
    schedule S2 ON S1.train = S2.train -- Train1 arrives at Change1
JOIN
    schedule S3 ON S2.station = S3.station -- Train2 departs from Change1
JOIN
    schedule S4 ON S3.train = S4.train -- Train2 arrives at Change2
JOIN
    schedule S5 ON S4.station = S5.station -- Train3 departs from Change2
JOIN
    schedule S6 ON S5.train = S6.train -- Train3 arrives at StationB
JOIN
    terminus T1 ON S1.station = T1.station
JOIN
    terminus T2 ON S6.station = T2.station
WHERE
    S1.station != S2.station
    AND S2.station != S4.station
    AND S4.station != S6.station
    AND S1.station != S4.station
    AND S1.station != S6.station
    AND S2.station != S6.station
    AND S1.train != S3.train
    AND S3.train != S5.train
    AND S1.train != S5.train
    AND S1.dep IS NOT NULL
    AND S2.arr IS NOT NULL
    AND S3.dep IS NOT NULL
    AND S4.arr IS NOT NULL
    AND S5.dep IS NOT NULL
    AND S6.arr IS NOT NULL
    AND (
        (S2.arrdate < S3.depdate)
        OR
        (S2.arrdate = S3.depdate AND S2.arr < S3.dep)
    )
    AND (
        (S4.arrdate < S5.depdate)
        OR
        (S4.arrdate = S5.depdate AND S4.arr < S5.dep)
    )
    AND (
        (S6.arrdate > S5.depdate)
        OR
        (S6.arrdate = S5.depdate AND S6.arr > S5.dep)
    );


-- Part 2: Repeat the above exercise with three changes.
-- This query includes 0, 1, 2, and 3 changes.

-- Query for 0 changes (direct train)
SELECT
    T1.station AS StationA,
    T2.station AS StationB,
    S1.train AS Train1,
    NULL AS Change1,
    NULL AS Train2,
    NULL AS Change2,
    NULL AS Train3
FROM
    schedule S1
JOIN
    schedule S2 ON S1.train = S2.train
JOIN
    terminus T1 ON S1.station = T1.station
JOIN
    terminus T2 ON S2.station = T2.station
WHERE
    S1.station != S2.station
    AND S1.dep IS NOT NULL
    AND S2.arr IS NOT NULL
    AND (
        (S2.arrdate > S1.depdate)
        OR
        (S2.arrdate = S1.depdate AND S2.arr > S1.dep)
    )

UNION ALL

-- Query for 1 change
SELECT
    T1.station AS StationA,
    T2.station AS StationB,
    S1.train AS Train1,
    S2.station AS Change1,
    S3.train AS Train2,
    NULL AS Change2,
    NULL AS Train3
FROM
    schedule S1 -- Train1 departs from StationA
JOIN
    schedule S2 ON S1.train = S2.train -- Train1 arrives at Change1
JOIN
    schedule S3 ON S2.station = S3.station -- Train2 departs from Change1
JOIN
    schedule S4 ON S3.train = S4.train -- Train2 arrives at StationB
JOIN
    terminus T1 ON S1.station = T1.station
JOIN
    terminus T2 ON S4.station = T2.station
WHERE
    S1.station != S2.station
    AND S2.station != S4.station
    AND S1.station != S4.station
    AND S1.train != S3.train
    AND S1.dep IS NOT NULL
    AND S2.arr IS NOT NULL
    AND S3.dep IS NOT NULL
    AND S4.arr IS NOT NULL
    AND (
        (S2.arrdate < S3.depdate)
        OR
        (S2.arrdate = S3.depdate AND S2.arr < S3.dep)
    )
    AND (
        (S4.arrdate > S3.depdate)
        OR
        (S4.arrdate = S3.depdate AND S4.arr > S3.dep)
    )

UNION ALL

-- Query for 2 changes
SELECT
    T1.station AS StationA,
    T2.station AS StationB,
    S1.train AS Train1,
    S2.station AS Change1,
    S3.train AS Train2,
    S4.station AS Change2,
    S5.train AS Train3
FROM
    schedule S1 -- Train1 departs from StationA
JOIN
    schedule S2 ON S1.train = S2.train -- Train1 arrives at Change1
JOIN
    schedule S3 ON S2.station = S3.station -- Train2 departs from Change1
JOIN
    schedule S4 ON S3.train = S4.train -- Train2 arrives at Change2
JOIN
    schedule S5 ON S4.station = S5.station -- Train3 departs from Change2
JOIN
    schedule S6 ON S5.train = S6.train -- Train3 arrives at StationB
JOIN
    terminus T1 ON S1.station = T1.station
JOIN
    terminus T2 ON S6.station = T2.station
WHERE
    S1.station != S2.station
    AND S2.station != S4.station
    AND S4.station != S6.station
    AND S1.station != S4.station
    AND S1.station != S6.station
    AND S2.station != S6.station
    AND S1.train != S3.train
    AND S3.train != S5.train
    AND S1.train != S5.train
    AND S1.dep IS NOT NULL
    AND S2.arr IS NOT NULL
    AND S3.dep IS NOT NULL
    AND S4.arr IS NOT NULL
    AND S5.dep IS NOT NULL
    AND S6.arr IS NOT NULL
    AND (
        (S2.arrdate < S3.depdate)
        OR
        (S2.arrdate = S3.depdate AND S2.arr < S3.dep)
    )
    AND (
        (S4.arrdate < S5.depdate)
        OR
        (S4.arrdate = S5.depdate AND S4.arr < S5.dep)
    )
    AND (
        (S6.arrdate > S5.depdate)
        OR
        (S6.arrdate = S5.depdate AND S6.arr > S5.dep)
    )

UNION ALL

-- Query for 3 changes
SELECT
    T1.station AS StationA,
    T2.station AS StationB,
    S1.train AS Train1,
    S2.station AS Change1,
    S3.train AS Train2,
    S4.station AS Change2,
    S5.train AS Train3,
    S6.station AS Change3,
    S7.train AS Train4
FROM
    schedule S1 -- Train1 departs from StationA
JOIN
    schedule S2 ON S1.train = S2.train -- Train1 arrives at Change1
JOIN
    schedule S3 ON S2.station = S3.station -- Train2 departs from Change1
JOIN
    schedule S4 ON S3.train = S4.train -- Train2 arrives at Change2
JOIN
    schedule S5 ON S4.station = S5.station -- Train3 departs from Change2
JOIN
    schedule S6 ON S5.train = S6.train -- Train3 arrives at Change3
JOIN
    schedule S7 ON S6.station = S7.station -- Train4 departs from Change3
JOIN
    schedule S8 ON S7.train = S8.train -- Train4 arrives at StationB
JOIN
    terminus T1 ON S1.station = T1.station
JOIN
    terminus T2 ON S8.station = T2.station
WHERE
    S1.station != S2.station
    AND S2.station != S4.station
    AND S4.station != S6.station
    AND S6.station != S8.station
    AND S1.station != S4.station
    AND S1.station != S6.station
    AND S1.station != S8.station
    AND S2.station != S6.station
    AND S2.station != S8.station
    AND S4.station != S8.station
    AND S1.train != S3.train
    AND S3.train != S5.train
    AND S5.train != S7.train
    AND S1.train != S5.train
    AND S1.train != S7.train
    AND S3.train != S7.train
    AND S1.dep IS NOT NULL
    AND S2.arr IS NOT NULL
    AND S3.dep IS NOT NULL
    AND S4.arr IS NOT NULL
    AND S5.dep IS NOT NULL
    AND S6.arr IS NOT NULL
    AND S7.dep IS NOT NULL
    AND S8.arr IS NOT NULL
    AND (
        (S2.arrdate < S3.depdate)
        OR
        (S2.arrdate = S3.depdate AND S2.arr < S3.dep)
    )
    AND (
        (S4.arrdate < S5.depdate)
        OR
        (S4.arrdate = S5.depdate AND S4.arr < S5.dep)
    )
    AND (
        (S6.arrdate < S7.depdate)
        OR
        (S6.arrdate = S7.depdate AND S6.arr < S7.dep)
    )
    AND (
        (S8.arrdate > S7.depdate)
        OR
        (S8.arrdate = S7.depdate AND S8.arr > S7.dep)
    );
