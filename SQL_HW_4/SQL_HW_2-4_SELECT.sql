-- Задание 2

SELECT title, duration_sec
FROM tracks
ORDER BY duration_sec DESC
LIMIT 1;

SELECT title
FROM tracks 
WHERE duration_sec >= (3.5 * 60);

SELECT title 
FROM collection
WHERE release_year BETWEEN 2018 AND 2020;

SELECT artist_name 
FROM artist
WHERE artist_name NOT LIKE '% %';

SELECT title
FROM tracks
WHERE title LIKE '%my%' OR title LIKE '%мой%';

-- Задание 3

SELECT g.title, COUNT(artist_id) AS artists_total
FROM artist_genre AS ag
JOIN genre AS g ON ag.genre_id = g.genre_id
GROUP BY g.title 
ORDER BY artists_total DESC;

SELECT a.title, COUNT(track_id) AS tracks_total
FROM tracks AS t
JOIN album AS a ON t.album_id = a.album_id 
WHERE a.release_year BETWEEN 2019 AND 2020
GROUP BY a.title 
ORDER BY tracks_total DESC;

SELECT a.title, AVG(duration_sec) AS duration_sec_avg
FROM tracks AS t
JOIN album AS a ON t.album_id = a.album_id 
GROUP BY a.title 
ORDER BY duration_sec_avg DESC;

SELECT ar.artist_name  
FROM artist_album AS aa 
JOIN artist AS ar ON aa.artist_id = ar.artist_id 
JOIN album AS a ON aa.album_id = a.album_id 
WHERE a.release_year <> 2020;

SELECT DISTINCT c.title 
FROM collection AS c 
JOIN collection_track AS ct ON ct.collection_id = c.collection_id 
JOIN tracks AS t ON ct.track_id = t.track_id 
JOIN album AS a ON t.album_id = a.album_id 
JOIN artist_album AS aa ON aa.album_id = a.album_id 
JOIN artist AS ar ON aa.artist_id = ar.artist_id 
WHERE ar.artist_name = 'Bob Marley';

-- Задание 4

SELECT title
FROM album
JOIN artist_album USING(album_id)
WHERE artist_id IN 
	(SELECT artist_id
	 FROM artist_genre
	 GROUP BY artist_id
	 HAVING COUNT(genre_id) > 1);

SELECT title 
FROM tracks
WHERE track_id NOT IN 
	(SELECT track_id
	 FROM collection_track);
	
SELECT artist_name
FROM artist
JOIN artist_album USING(artist_id)
JOIN album USING(album_id)
JOIN tracks USING(album_id)
WHERE duration_sec = (SELECT MIN(duration_sec)
					  FROM tracks);

SELECT a.title 
FROM album as a
JOIN tracks USING(album_id)
GROUP BY album_id
HAVING COUNT(track_id) = (SELECT COUNT(track_id) AS tracks_total
						  FROM tracks
						  GROUP BY album_id 
						  ORDER BY tracks_total ASC
						  LIMIT 1);





	  









