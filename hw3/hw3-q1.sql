SELECT DISTINCT 
	f.origin_city AS origin_city,
	f.dest_city AS dest_city,
	mf.max_time AS time
FROM 
	flights AS f
	INNER JOIN
	(SELECT origin_city AS oc, max(actual_time) AS max_time
	FROM flights
	GROUP BY origin_city) AS mf
ON f.origin_city = mf.oc AND f.actual_time = mf.max_time
ORDER BY f.origin_city, f.dest_city ASC

/*
334
Query succeeded | 8s

origin_city dest_city time
Aberdeen SD Minneapolis MN 106
Abilene TX Dallas/Fort Worth TX 111
Adak Island AK Anchorage AK 471
Aguadilla PR New York NY 368
Akron OH Atlanta GA 408
Albany GA Atlanta GA 243
Albany NY Atlanta GA 390
Albuquerque NM Houston TX 492
Alexandria LA Atlanta GA 391
Allentown/Bethlehem/Easton PA Atlanta GA 456
Alpena MI Detroit MI 80
Amarillo TX Houston TX 390
Anchorage AK Barrow AK 490
Appleton WI Atlanta GA 405
Arcata/Eureka CA San Francisco CA 476
Asheville NC Chicago IL 279
Ashland WV Cincinnati OH 84
Aspen CO Los Angeles CA 304
Atlanta GA Honolulu HI 649
Atlantic City NJ Fort Lauderdale FL 212
Augusta GA Atlanta GA 176
*/