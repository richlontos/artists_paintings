# import the function that will return an instance of a connection
from ast import If
import flask_app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from pprint import pprint
import re
from flask_app.models.painting import Painting
# model the class after the artist table from our database
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DATABASE = 'artists_paintings'


class Artist:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.paintings = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database

    @classmethod
    def save(cls, data):
        query = "INSERT INTO artists (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        # query = "SELECT * FROM artists;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM artists WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) > 0:
            return Artist(result[0])
        else:
            return False


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM artists;"
        results = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances of artists
        artists = []
        # Iterate over the db results and create instances of artists with cls.
        for artist in results:
            artists.append(cls(artist))
        return artists

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM artists WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        artist = Artist(result[0])
        return artist




    @staticmethod
    def validate_artist(artist:dict) -> bool:
        is_valid = True
        if len(artist['first_name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters", 'first_name')
        if len(artist['last_name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters", 'last_name')
        if artist['confirm-password'] != artist['password']:
            is_valid = False
            flash("passwords must match")
        if len(artist['password']) < 8:
            is_valid = False
            flash('password must be at least 8 characters')
        if not EMAIL_REGEX.match(artist['email']): 
            is_valid = False
            flash("Invalid email address!")
        return is_valid


    @classmethod
    def get_one_with_paintings(cls, data):
        query = "SELECT * FROM artists LEFT JOIN paintings ON artists.id = paintings.artist_id WHERE artists.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        artist = Artist(results[0])

        for result in results:
            temp_painting = {
                "id": result['id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "artist_id": result['artist_id'],

                # "age": result['age'],
                "created_at": result['paintings.created_at'],
                "updated_at": result['paintings.updated_at']
            }
            artist.paintings.append(Painting(temp_painting))

        return artist
