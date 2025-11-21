SELECT DISTINCT
  A.station AS StationA,
  B.station AS StationB,
  s1.train   AS Train1,
  NULL       AS Change1,
  NULL       AS Train2,
  NULL       AS Change2,
  NULL       AS Train3
FROM terminus A
JOIN schedule s1
  ON s1.station = A.station
JOIN schedule s2
  ON s2.train = s1.train
 AND ( s1.depdate < s2.arrdate
    OR (s1.depdate = s2.arrdate AND s1.dep < s2.arr) )
JOIN terminus B
  ON B.station = s2.station
WHERE A.station <> B.station

UNION ALL

SELECT DISTINCT
  A.station AS StationA,
  B.station AS StationB,
  t1.train  AS Train1,
  X.station AS Change1,
  t2.train  AS Train2,
  NULL      AS Change2,
  NULL      AS Train3
FROM terminus A
JOIN schedule t1
  ON t1.station = A.station

JOIN schedule X
  ON X.train = t1.train
 AND ( t1.depdate < X.arrdate
    OR (t1.depdate = X.arrdate AND t1.dep < X.arr) )

JOIN schedule X2
  ON X2.station = X.station

JOIN schedule t2
  ON t2.train = X2.train
 AND ( X2.depdate < t2.arrdate
    OR (X2.depdate = t2.arrdate AND X2.dep < t2.arr) )

JOIN terminus B
  ON B.station = t2.station

WHERE A.station <> B.station
  AND X.station NOT IN (A.station, B.station)
  AND t1.train <> t2.train
  AND ( X.arrdate < X2.depdate OR (X.arrdate = X2.depdate AND X.arr <= X2.dep) )

UNION ALL

SELECT DISTINCT
  A.station      AS StationA,
  B.station      AS StationB,
  t1.train       AS Train1,
  X.station      AS Change1,
  t2.train       AS Train2,
  t2.station     AS Change2,
  t3.train       AS Train3
FROM terminus A
JOIN schedule t1
  ON t1.station = A.station

JOIN schedule X
  ON X.train = t1.train
 AND ( t1.depdate < X.arrdate
    OR (t1.depdate = X.arrdate AND t1.dep < X.arr) )

JOIN schedule X2
  ON X2.station = X.station

JOIN schedule t2
  ON t2.train = X2.train
 AND ( X2.depdate < t2.arrdate
    OR (X2.depdate = t2.arrdate AND X2.dep < t2.arr) )

JOIN schedule Y2
  ON Y2.station = t2.station

JOIN schedule t3
  ON t3.train = Y2.train
 AND ( Y2.depdate < t3.arrdate
    OR (Y2.depdate = t3.arrdate AND Y2.dep < t3.arr) )

JOIN terminus B
  ON B.station = t3.station

WHERE A.station <> B.station
  AND X.station NOT IN (A.station, B.station)
  AND t2.station NOT IN (A.station, B.station, X.station)
  AND t1.train <> t2.train
  AND t2.train <> t3.train
  AND t1.train <> t3.train
  AND ( X.arrdate < X2.depdate OR (X.arrdate = X2.depdate AND X.arr <= X2.dep) )
  AND ( t2.arrdate < Y2.depdate OR (t2.arrdate = Y2.depdate AND t2.arr <= Y2.dep) );

