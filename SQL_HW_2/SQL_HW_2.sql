CREATE TABLE IF NOT EXISTS genres (
	id SERIAL PRIMARY KEY,
	title VARCHAR(30) NOT NULL
	);
	
CREATE TABLE IF NOT EXISTS artists (
	id SERIAL PRIMARY KEY,
	name VARCHAR(40) NOT NULL
	);
	
CREATE TABLE IF NOT EXISTS artist_genre (
	artist_id INTEGER REFERENCES artists(id),
	genre_id INTEGER REFERENCES genres(id),
	CONSTRAINT art_gen PRIMARY KEY (artist_id, genre_id)
	);
	
CREATE TABLE IF NOT EXISTS albums (
	id SERIAL PRIMARY KEY,
	title VARCHAR(40) NOT NULL,
	release_year SMALLINT NOT NULL
	);

CREATE TABLE IF NOT EXISTS artist_album (
	artist_id INTEGER REFERENCES artists(id),
	album_id INTEGER REFERENCES albums(id),
	CONSTRAINT art_alb PRIMARY KEY (artist_id, album_id)
	);

CREATE TABLE IF NOT EXISTS tracks (
	id SERIAL PRIMARY KEY,
	album_id INTEGER REFERENCES albums(id),
	title VARCHAR(60) NOT NULL,
	duration TIME NOT NULL
	);

CREATE TABLE IF NOT EXISTS collections (
	id SERIAL PRIMARY KEY,
	title VARCHAR(40) NOT NULL, 
	release_year SMALLINT NOT NULL
	);

CREATE TABLE IF NOT EXISTS collection_track (
	collection_id INTEGER REFERENCES collections(id), 
	track_id INTEGER REFERENCES tracks(id),
	CONSTRAINT col_trk PRIMARY KEY (collection_id, track_id)
	);
	