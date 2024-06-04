CREATE TABLE IF NOT EXISTS genre (
	genre_id SERIAL PRIMARY KEY,
	title VARCHAR(30) NOT NULL
	);
	
CREATE TABLE IF NOT EXISTS artist (
	artist_id SERIAL PRIMARY KEY,
	artist_name VARCHAR(40) NOT NULL
	);
	
CREATE TABLE IF NOT EXISTS artist_genre (
	artist_id INTEGER REFERENCES artist(artist_id),
	genre_id INTEGER REFERENCES genre(genre_id),
	CONSTRAINT ag1 PRIMARY KEY (artist_id, genre_id)
	);
	
CREATE TABLE IF NOT EXISTS album (
	album_id SERIAL PRIMARY KEY,
	title VARCHAR(40) NOT NULL,
	release_year SMALLINT NOT NULL, 
	CHECK (release_year BETWEEN 1900 AND 2100)
	);

CREATE TABLE IF NOT EXISTS artist_album (
	artist_id INTEGER REFERENCES artist(artist_id),
	album_id INTEGER REFERENCES album(album_id),
	CONSTRAINT aa1 PRIMARY KEY (artist_id, album_id)
	);

CREATE TABLE IF NOT EXISTS tracks (
	track_id SERIAL PRIMARY KEY,
	album_id INTEGER REFERENCES album(album_id),
	title VARCHAR(60) NOT NULL,
	duration_sec INTEGER NOT NULL,
	CHECK (duration_sec > 0)
	);

CREATE TABLE IF NOT EXISTS collection (
	collection_id SERIAL PRIMARY KEY,
	title VARCHAR(40) NOT NULL, 
	release_year SMALLINT NOT NULL,
	CHECK (release_year BETWEEN 1900 AND 2100)
	);

CREATE TABLE IF NOT EXISTS collection_track (
	collection_id INTEGER REFERENCES collection(collection_id), 
	track_id INTEGER REFERENCES tracks(track_id),
	CONSTRAINT ct1 PRIMARY KEY (collection_id, track_id)
	);