SELECT DISTINCT f.carrier_id AS carrier
FROM 
	(SELECT *
	FROM flights
	WHERE origin_city = 'Seattle WA'
	AND dest_city = 'San Francisco CA') AS f
ORDER BY f.carrier_id ASC

/*
4
Query succeeded | 5s
carrier_id
AS
OO
UA
VX
*/