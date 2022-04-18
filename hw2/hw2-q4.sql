SELECT distinct carrier_id AS name
FROM flights 
GROUP BY carrier_id, day_of_month 
HAVING count(day_of_month) > 1000;