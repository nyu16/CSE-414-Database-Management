SELECT DISTINCT f2.dest_city AS city
FROM flights AS f1, flights AS f2
WHERE f1.dest_city = f2.origin_city
	AND f1.origin_city = 'Seattle WA'
	AND f2.dest_city != 'Seattle WA'
	AND f2.dest_city NOT IN (SELECT f.dest_city
		FROM flights AS f
		WHERE f.origin_city = 'Seattle WA')
ORDER BY f2.dest_city ASC

/*
256
Could not run on azure so I ran on terminal
Aberdeen SD
Abilene TX
Adak Island AK
Aguadilla PR
Akron OH
Albany GA
Albany NY
Alexandria LA
Allentown/Bethlehem/Easton PA
Alpena MI
Amarillo TX
Appleton WI
Arcata/Eureka CA
Asheville NC
Ashland WV
Aspen CO
Atlantic City NJ
Augusta GA
Bakersfield CA
Bangor ME
Barrow AK
*/