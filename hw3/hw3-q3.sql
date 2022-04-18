SELECT f.origin_city AS origin_city, ISNULL(((SELECT count(f1.actual_time)
	FROM flights AS f1
	WHERE f1.canceled = 0 AND f1.actual_time < 180
	GROUP BY f1.origin_city
	HAVING f1.origin_city = f.origin_city) * 100.00/ count(f.actual_time)), 0) AS percentage
FROM flights AS f
WHERE f.canceled = 0
GROUP BY f.origin_city
ORDER BY perc, f.origin_city ASC

/*
327
Query succeeded | 7s

Guam TT 0.0000000000000
Pago Pago TT 0.0000000000000
Aguadilla PR 28.8973384030418
Anchorage AK 31.8120805369127
San Juan PR 33.6605316973415
Charlotte Amalie VI 39.5588235294117 Ponce PR 40.9836065573770
Fairbanks AK 50.1165501165501
Kahului HI 53.5144713526284
Honolulu HI 54.7390288236821
San Francisco CA 55.8288645371881
Los Angeles CA 56.0808908229873
Seattle WA 57.6093877922314
Long Beach CA 62.1764395139989
New York NY 62.3718341367280
Kona HI 63.1607929515418
Las Vegas NV 64.9202563720375
Christiansted VI 65.1006711409395
Newark NJ 65.8499710969807
Plattsburgh NY 66.6666666666666
Worcester MA 67.2131147540983
Philadelphia PA 67.7815659534446
San Diego CA 68.2431059014838
Portland OR 68.8134580927732
Lihue HI 69.0970274817722 */