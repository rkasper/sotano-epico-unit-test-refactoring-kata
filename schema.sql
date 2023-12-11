CREATE TABLE IF NOT EXISTS artists (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    genre TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS albums (
    id INTEGER PRIMARY KEY,
    artist_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    release_year INTEGER NOT NULL,
    FOREIGN KEY (artist_id) REFERENCES artists (id)
);
