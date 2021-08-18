from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login first', 'login')
        return redirect('/')
    recipes = Recipe.get_all_recipes()
    return render_template('dashboard.html', user_id = session['user_id'], first_name = session['first_name'], recipes = recipes)

@app.route('/recipe/create')
def create_recipe():
    if 'user_id' not in session:
        flash('Please login first', 'login')
        return redirect('/')
    return render_template('create.html')

@app.route('/recipe/submit', methods = ['post'])
def submit_recipe():
    if 'user_id' not in session:
        flash('Please login first', 'login')
        return redirect('/')
    data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'date_made': request.form['date_made'],
            'under_30': int(request.form['under_30']),
            'user_id': session['user_id']
        }
    if Recipe.recipe_validator(data):
        Recipe.create_recipe(data)
        return redirect('/dashboard')
    return redirect('/recipe/create')

@app.route('/recipe/<int:recipe_id>/view')
def view_recipe(recipe_id):
    if 'user_id' not in session:
        flash('Please login first', 'login')
        return redirect('/')
    data = {
        'id': recipe_id
    }
    recipe = Recipe.get_by_id(data)
    return render_template('view.html', recipe = recipe, first_name = session['first_name'])

@app.route('/recipe/<int:recipe_id>/delete')
def delete_recipe(recipe_id):
    recipe = Recipe.get_by_id({'id': recipe_id})
    print(recipe)
    if recipe.user_id != session['user_id']:
        return redirect('/dashboard')
    Recipe.delete_recipe({'id': recipe_id})
    return redirect('/dashboard')

@app.route('/recipe/<int:recipe_id>/edit')
def view_edit(recipe_id):
    recipe = Recipe.get_by_id({'id': recipe_id})
    if recipe.user_id != session['user_id']:
        return redirect('/dashboard')
    return render_template('edit.html', recipe = recipe)

@app.route('/recipe/<int:recipe_id>/update', methods = ['POST'])
def submit_edit(recipe_id):
    recipe = Recipe.get_by_id({'id': recipe_id})
    if recipe.user_id != session['user_id']:
        return redirect('/dashboard')
    data = {
            'id': recipe_id,
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'date_made': request.form['date_made'],
            'under_30': int(request.form['under_30']),
        }
    Recipe.update_recipe(data)
    return redirect(f'/recipe/{recipe.id}/view')