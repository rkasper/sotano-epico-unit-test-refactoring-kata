from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)


def get_db_connection():
    db_path = app.config.get('DATABASE', 'catalog.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with sqlite3.connect('catalog.db') as conn:
        with open('schema.sql') as f:
            conn.executescript(f.read())


# Ensure the database is initialized
init_db()


# Add a new artist
@app.route('/artist', methods=['POST'])
def add_artist():
    name = request.form['name']
    genre = request.form['genre']
    conn = get_db_connection()
    conn.execute('INSERT INTO artists (name, genre) VALUES (?, ?)', (name, genre))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Artist added successfully'}), 201


# Get artist information
@app.route('/artist/<int:artist_id>', methods=['GET'])
def get_artist(artist_id):
    conn = get_db_connection()
    artist = conn.execute('SELECT * FROM artists WHERE id = ?',
                          (artist_id,)).fetchone()
    conn.close()
    return jsonify(dict(artist)) if artist else ('', 404)


# Add a new album
@app.route('/album', methods=['POST'])
def add_album():
    artist_id = request.form['artist_id']
    title = request.form['title']
    release_year = request.form['release_year']
    conn = get_db_connection()
    conn.execute('INSERT INTO albums (artist_id, title, release_year) VALUES (?, ?, ?)',
                 (artist_id, title, release_year))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Album added successfully'}), 201


# Get album information
@app.route('/album/<int:album_id>', methods=['GET'])
def get_album(album_id):
    conn = get_db_connection()
    album = conn.execute('SELECT * FROM albums WHERE id = ?',
                         (album_id,)).fetchone()
    conn.close()
    return jsonify(dict(album)) if album else ('', 404)


if __name__ == '__main__':
    app.run(debug=True)
