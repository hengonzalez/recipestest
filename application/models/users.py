from application.config.mysqlconnection import connectToMySQL # import the connectToMySQL function from the application.config.mysqlconnection module
from flask import flash
import re

class User: # crear una clase usuario
    def __init__(self, data): 
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.user_password = data["user_password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        
    @staticmethod # método de validación de usuario de formulario de registro
    def validate_user(user):
        is_valid = True
        if len(user["first_name"]) < 2:
            flash("El nombre debe tener más de 2 caracteres", "register")
            is_valid = False
        if len(user["last_name"]) < 2:
            flash("El apellido debe tener más de 2 caracteres", "register")
            is_valid = False
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' # validación con regex para email
        if not re.fullmatch(regex, user["email"]):
            flash("El email no es válido", "register")
            is_valid = False
        if len(user["user_password"]) < 8:
            flash("La contraseña debe tener más de 8 caracteres", "register")
            is_valid = False
        if user["user_password"] != user["confirm"]:
            flash ("Las contraseñas no coinciden", "register")
            is_valid = False
        return is_valid

    @staticmethod # método de validación de usuario de formulario de login
    def validate_login(user):
        is_valid = True
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' # validación con regex para email
        if not re.fullmatch(regex, user["email"]):
            flash("El imail no es válido", "register")
            is_valid = False
        if len(user["user_password"]) < 8:
            flash("La contraseña debe tener más de 8 caracteres", "register")
            is_valid = False
        return is_valid
        
    
    @classmethod # método para insertar un nuevo usuario en la base de datos
    def save_user(cls, data):
        query = "INSERT INTO t_users (first_name, last_name, email, user_password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(user_password)s, NOW(), NOW())"
        mysql = connectToMySQL("db_recipes")
        results = mysql.query_db(query, data)
        user = {"user.id": results}
        return user
    
    @classmethod # metodo para obtener todos los usuarios de la base de datos
    def get_all_users(cls):
        query = "SELECT * FROM t_users"
        mysql = connectToMySQL("db_recipes")
        results = mysql.query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
            return users
    
    @classmethod # método para obtener un usuario por su id
    def get_user_by_id(cls, id):
        query = "SELECT * FROM t_users WHERE id = %(id)s"
        data = {
            'id': id
        }
        mysql = connectToMySQL("db_recipes")
        results = mysql.query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM t_users WHERE email = %(email)s"
        mysql = connectToMySQL("db_recipes")
        result = mysql.query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None
