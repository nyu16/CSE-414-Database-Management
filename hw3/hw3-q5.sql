SELECT DISTINCT f.dest_city AS city
FROM (SELECT dest_city
  FROM flights
  WHERE origin_city != 'Seattle WA') AS f
WHERE f.dest_city NOT IN (SELECT f2.dest_city
  FROM flights AS f1, flights AS f2
  WHERE f1.dest_city = f2.origin_city
    AND f1.dest_city = f.dest_city
    AND f1.origin_city = 'Seattle WA')
ORDER BY f.dest_city ASC

/* I was not able to get an answer
A connection was successfully established with the server, but then an error occurred during the login process.
(provider: TCP Provider, error: 0 - An existing connection was forcibly closed by the remote host.)*/
