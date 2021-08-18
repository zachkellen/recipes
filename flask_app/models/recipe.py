from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, request
from flask_app.models.user import User

class Recipe():
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None

    @classmethod
    def create_recipe(cls,data):
        query = 'INSERT INTO recipes (name, description, instructions, date_made, under_30, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30)s, %(user_id)s);'
        result = connectToMySQL('recipes_schema').query_db(query, data)
        return result

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL('recipes_schema').query_db(query)
        recipes = []
        for recipe in results:
            newRecipe = Recipe(recipe)
            user_data = {
                'id': recipe['users.id'],
                'first_name': recipe['first_name'],
                'last_name': recipe['last_name'],
                'email': recipe['email'],
                'password': recipe['password'],
                'created_at': recipe['users.created_at'],
                'updated_at': recipe['users.updated_at']
            }
            newUser = User(user_data)
            newRecipe.user = newUser
            recipes.append(newRecipe)
        return recipes

    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;'
        result = connectToMySQL('recipes_schema').query_db(query, data)[0]
        recipe = Recipe(result)
        user_data = {
                'id': result['users.id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'email': result['email'],
                'password': result['password'],
                'created_at': result['users.created_at'],
                'updated_at': result['users.updated_at']
            }
        print(user_data)
        Recipe.user = User(user_data)
        print(recipe)
        return recipe

    @classmethod
    def delete_recipe(cls,data):
        query = 'DELETE FROM recipes WHERE id = %(id)s;'
        result = connectToMySQL('recipes_schema').query_db(query, data)

    @classmethod
    def update_recipe(cls,data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_30 = %(under_30)s WHERE id = %(id)s;'
        results = connectToMySQL('recipes_schema').query_db(query, data)
        return results


    @staticmethod
    def recipe_validator(data):
        is_valid = True
        if len(data['name']) < 3 or len(data['name']) > 45:
            flash('Name must be between 3 and 45 characters.')
            is_valid = False
        if len(data['description']) < 3:
            flash('Description must be longer than 3 characters.')
            is_valid = False
        if len(data['instructions']) < 3:
            flash('Instructions must be longer than 3 characters.')
            is_valid = False
        if len(data['date_made']) != 10:
            flash('Please provide a valid date.')
            is_valid = False
        if data['under_30'] != 0 and data['under_30'] != 1:
            flash('Please select if this recipe takes less than 30 minutes to make.')
            is_valid = False
        return is_valid