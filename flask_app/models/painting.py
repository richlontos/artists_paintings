# import the function that will return an instance of a connection
import flask_app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
import re
# model the class after the painting table from our database
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DATABASE = 'artists_paintings'


class Painting:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.name = data['title']
        self.description = data['description']
        self.price = data['price']
        self.artist_id = data['artist_id']
        if 'first_name' in data:
            self.first_name = data['first_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database

    @classmethod
    def save(cls, data):
        query = "INSERT INTO paintings (title, description, price, artist_id) VALUES ( %(title)s, %(description)s, %(price)s, %(artist_id)s);"
        # query = "SELECT * FROM paintings;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM paintings WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) > 0:
            return Painting(result[0])
        else:
            return False


    @classmethod
    def get_all(cls):
        query = " SELECT paintings.*, first_name FROM paintings JOIN artists ON artists.id = paintings.artist_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances of paintings
        paintings = []
        # Iterate over the db results and create instances of paintings with cls.
        for painting in results:
            paintings.append(cls(painting))
        return paintings

    

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM paintings JOIN artists ON artists.id = paintings.artist_id WHERE paintings.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        painting = Painting(result[0])
        return painting


    @classmethod
    def update(cls,data):
        query = "UPDATE paintings SET title = %(title)s, description = %(description)s, price = %(price)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)





    @staticmethod
    def validate_painting(painting:dict) -> bool:
        is_valid = True
        if len(painting['title']) == False and  len(painting['description']) == False and  len(painting['price']) == False:
            is_valid = False
            flash("All fields required")
        if len(painting['title']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters", 'title')
            flash("All fields required")
        if len(painting['description']) < 10:
            is_valid = False
            flash("Description must be at least 10 characters", 'description')
            flash("All fields required")
        if  int(painting['price']) < 1:
            is_valid = False
            flash("price must be greater that 0", 'price')
        return is_valid
    


    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM paintings WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)