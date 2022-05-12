from unittest import result
from application.config.mysqlconnection import connectToMySQL # import the connectToMySQL function from the application.config.mysqlconnection module
from flask import flash
import re

class Recipe:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.under_thirty = True if data["under_thirty"] == 1 else False 
        self.date_made = data["date_made"]
        self.user_id = data["user_id"]
        
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe["name"]) < 3:
            flash("El nombre debe tener más de 3 caracteres", "error_recipe")
            print("name failed")
            is_valid = False
        if len(recipe["description"]) < 3:
            flash("La descripción debe tener más de 3 caracteres", "error_recipe")
            print("description failed")
            is_valid = False
        if len(recipe["instructions"]) < 3:
            flash("Las instrucciones debe tener más de 3 caracteres", "error_recipe")
            print("instructions failed")
            is_valid = False
        return is_valid
            
    @classmethod
    def save_recipe(cls, data):
        query = "INSERT INTO t_recipes (name, description, instructions, under_thirty, date_made, user_id, created_at, updated_at) VALUES (%(name)s, %(description)s, %(instructions)s, %(under_thirty)s, %(date_made)s, %(user_id)s, NOW(), NOW())"
        mysql = connectToMySQL("db_recipes")
        results = mysql.query_db(query, data)
        recipe = {"user.id": results}
        return recipe
    
    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM t_recipes"
        mysql = connectToMySQL("db_recipes")
        results = mysql.query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes
        
    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE t_recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under_thirty = %(under_thirty)s, date_made = %(date_made)s, updated_at = NOW() WHERE id = %(id)s"
        mysql = connectToMySQL("db_recipes")
        results = mysql.query_db(query, data)
        return results
    
    @classmethod
    def get_recipe_by_id(cls, data):
        query = "SELECT * FROM t_recipes WHERE id = %(id)s"
        mysql = connectToMySQL("db_recipes")
        results = mysql.query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM t_recipes WHERE id = %(id)s"
        mysql = connectToMySQL("db_recipes")
        results = mysql.query_db(query, data)
        return results