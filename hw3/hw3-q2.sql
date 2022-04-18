SELECT f.oc AS city
FROM
	(SELECT origin_city AS oc, max(actual_time) mt
	FROM flights
	WHERE canceled = 0
	GROUP BY origin_city) AS f
WHERE f.mt < 180
ORDER BY f.oc ASC

/*
109
Query succeeded | 3s
Aberdeen SD
Abilene TX
Alpena MI
Ashland WV
Augusta GA
Barrow AK
Beaumont/Port Arthur TX
Bemidji MN
Bethel AK
Binghamton NY
Brainerd MN
Bristol/Johnson City/Kingsport TN
Butte MT
Carlsbad CA
Casper WY
Cedar City UT
Chico CA
College Station/Bryan TX
Columbia MO
Columbus GA
Columbus MS
Cordova AK
*/