SELECT w.day_of_week AS day_of_week, AVG(arrival_delay) AS delay
FROM flights f, weekdays w
WHERE f.day_of_week_id = w.did
GROUP BY day_of_week_id
ORDER BY avg(arrival_delay) DESC
LIMIT 1;