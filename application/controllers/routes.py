from application import app 
from application.models.users import User
from application.models.recipes import Recipe
from flask_bcrypt import Bcrypt

from flask import render_template, request, redirect, url_for, session, flash 
bcrypt = Bcrypt(app)

@app.route('/') # crear una ruta
def users(): # crear una función
    return render_template('users.html') # devolver el template index.html

@app.route('/dashboard') 
def dashboard():
    if 'user.id' in session:
        recipes = Recipe.get_all_recipes()
        print(recipes)
        return render_template('dashboard.html', recipes = recipes)
    else:
        return redirect('/')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    print(request.form)
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['user_password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "user_password": pw_hash
    }
    User.save_user(data)
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    print(request.form)
    if not User.validate_login(request.form):
        print("login failed")
        return redirect('/')
    logged_user = User.get_user_by_email(request.form)
    if logged_user == None:
        flash ("Email/Contraseña no válidos", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(logged_user.user_password, request.form['user_password']):
        flash ("Email/Contraseña no válidos", "login")
        return redirect('/')
    session ['user.id'] = logged_user.id
    session ['user.first_name'] = logged_user.first_name
    return redirect('/dashboard')

@app.route('/recipes/new', methods = ['GET', 'POST'])
def recipes(): 
    if not 'user.id' in session:
        print("no user logged in")
        return redirect('/')
    if request.method == 'GET':
        return render_template('recipes.html')
    elif request.method == 'POST':
        print(request.form)    
        if not Recipe.validate_recipe(request.form):
            print("recipe failed")
            return redirect('/recipes/new')
        data = {
            "name": request.form['name'],
            "description": request.form['description'],
            "instructions": request.form['instructions'],
            "under_thirty": int(request.form['under_thirty']),
            "date_made": request.form['date_made'],
            "user_id": session['user.id']
            }
        Recipe.save_recipe(data)
        return redirect('/dashboard')

@app.route('/recipes/edit/<int:id>')
def get_recipe_by_id(id):
    data = {
        'id': id
    }
    recipe = Recipe.get_recipe_by_id(data)
    return render_template ('edit.html', recipe = recipe)

@app.route('/recipes/update', methods=['POST'])
def update_recipe():
    Recipe.update_recipe(request.form)
    return redirect('/dashboard')

@app.route('/recipes/<int:id>')
def show_recipe(id):
    data = {
        "id" : id
    }
    recipe = Recipe.get_recipe_by_id(data)
    return render_template('show_recipe.html', recipe = recipe)

@app.route("/recipes/delete/<int:id>")
def delete(id):
    data ={
        'id': id
    }
    Recipe.delete_recipe(data)
    return redirect("/dashboard")


@app.errorhandler(404) 
def url_error(e):
    return "Página no encontrada", 404