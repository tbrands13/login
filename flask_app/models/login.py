from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
#from flask_bcrypt import Bcrypt
#bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls, data):
        query = 'INSERT INTO logins (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());'
        results = connectToMySQL('login_schema').query_db(query,data)
        return results



    @classmethod
    def choose_user_by_email(cls, data):
        query = "SELECT * FROM logins WHERE id = %(id)s;"
        results = connectToMySQL('login_schema').query_db(query,data)
        print(results)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM logins WHERE email = %(email)s;"
        results = connectToMySQL('login_schema').query_db(query,data)
        print(results[0])
        return cls(results[0])
        


    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('login_schema').query_db(query)
        return results





    @staticmethod
    def validate_user(data):
        is_legit = True
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_legit = False
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters")
            is_legit = False
        if len(data['email']) < 7:
            flash("Email must be at least 7 characters ")
            is_legit = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Email is not valid')
            is_legit = False
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters long')
            is_legit = False
        if not data['password'] == data['confirm_password']:
            flash('Passwords do not match')
            is_legit = False
        return is_legit

