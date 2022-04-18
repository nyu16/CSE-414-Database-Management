SELECT SUM(capacity) AS capacity
FROM flights
WHERE month_id=7 AND
day_of_month=10 AND
(origin_city = "Seattle WA" AND dest_city = "San Francisco CA") OR
(origin_city = "San Francisco CA" AND dest_city = "Seattle WA");