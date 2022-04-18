SELECT carrier_id AS carrier, MAX(price) AS max_price
FROM flights 
WHERE (origin_city = "Seattle WA" AND dest_city = "New York NY")
OR (origin_city = "New York NY" AND dest_city = "Seattle WA")
GROUP BY carrier_id;