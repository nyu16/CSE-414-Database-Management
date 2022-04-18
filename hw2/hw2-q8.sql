SELECT carrier_id AS name,
SUM(capacity) AS delay
FROM flights
GROUP BY carrier_id;