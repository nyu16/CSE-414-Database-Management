SELECT carrier_id AS name, SUM(canceled)*100./COUNT(canceled) AS percentage
FROM flights
WHERE origin_city = "Seattle WA"
GROUP BY carrier_id
HAVING SUM(canceled)*100./COUNT(canceled) > 0.5;