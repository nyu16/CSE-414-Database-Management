SELECT DISTINCT flight_num AS flight_num
FROM flights 
WHERE origin_city = "Seattle WA" AND 
dest_city = "Boston MA" AND
carrier_id = "AS" AND
day_of_week_id = 1;