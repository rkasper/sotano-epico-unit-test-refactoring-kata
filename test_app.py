import json
import os
import sqlite3
import unittest
from unittest.mock import patch, MagicMock

from app import app


class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a temporary database
        cls.db_path = 'test_catalog.db'
        cls.connection = sqlite3.connect(cls.db_path)
        cls.connection.row_factory = sqlite3.Row
        with open('schema.sql') as f:
            cls.connection.executescript(f.read())

        # Insert test data
        with cls.connection:
            cls.connection.execute("INSERT INTO artists (name, genre) VALUES ('Sótano Épico', 'Metal')")
            cls.connection.execute("INSERT INTO albums (artist_id, title, release_year) VALUES (1, 'Interstate Jungle Dynamite', 2023)")

        # Configure Flask app for testing
        app.config['TESTING'] = True
        app.config['DATABASE'] = cls.db_path
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        # Close and remove the temporary database
        cls.connection.close()
        os.remove(cls.db_path)

    @patch('app.get_db_connection')
    def test_add_artist(self, mock_get_db_connection):
        # Setup a mock database connection
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn

        # Call the endpoint and make assertions
        response = self.client.post('/artist', data={'name': 'Sótano Épico', 'genre': 'Metal'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data), {'message': 'Artist added successfully'})

        # Verify that the database connection was used to execute the query
        mock_conn.execute.assert_called_with('INSERT INTO artists (name, genre) VALUES (?, ?)',
                                             ('Sótano Épico', 'Metal'))
        mock_conn.commit.assert_called_once()

    @patch('app.get_db_connection')
    def test_get_artist(self, mock_get_db_connection):
        # Setup a mock database connection
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn

        # Setup a mock artist data
        mock_artist = {'id': 1, 'name': 'Sótano Épico', 'genre': 'Metal'}
        mock_conn.execute.return_value.fetchone.return_value = mock_artist

        # Call the endpoint and make assertions
        response = self.client.get('/artist/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'id': 1, 'name': 'Sótano Épico', 'genre': 'Metal'})

        # Verify that the mock database connection was used to execute the query
        mock_conn.execute.assert_called_with('SELECT * FROM artists WHERE id = ?', (1,))

    def test_add_album(self):
        # Assuming an artist with ID 1 exists
        response = self.client.post('/album', data={'artist_id': 1, 'title': 'Interstate Jungle Dynamite', 'release_year': 2023})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data), {'message': 'Album added successfully'})

    def test_get_album(self):
        response = self.client.get('/album/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data),
                         {'id': 1, 'artist_id': 1, 'title': 'Interstate Jungle Dynamite', 'release_year': 2023})


if __name__ == '__main__':
    unittest.main()
