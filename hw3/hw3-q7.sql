SELECT DISTINCT carrier_id AS carrier
FROM flights
WHERE origin_city = 'Seattle WA'
AND dest_city = 'San Francisco CA'
ORDER BY carrier_id ASC

/*
4
Query succeeded | 8s
AS
OO
UA
VX
*/