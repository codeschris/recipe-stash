#importing the required modules
from flask import Flask, render_template, request, flash, redirect, url_for
import sqlite3
import markdown

#defining the Flask web application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisaclassproject'

#creating connection with the database
def get_db_conn():
    conn = sqlite3.connect('proj_db.db')
    conn.row_factory = sqlite3.Row
    return conn

#landing page route
@app.route('/')
def index():
    conn = get_db_conn()
    db_recipes = conn.execute('SELECT id, created, title, ingredients, guide, servings FROM recipes;').fetchall()

    #converting text in database to markdown after selecing
    recipes = []
    for recipe in db_recipes:
        recipe = dict(recipe)
        recipe['title'] = markdown.markdown(recipe['title'])
        recipe['ingredients'] = markdown.markdown(recipe['ingredients'])
        recipe['guide'] = markdown.markdown(recipe['guide'])
        recipe['servings'] = markdown.markdown(recipe['servings'])

        recipes.append(recipe)
    
    #returning the index page with the recipes being displayed
    return render_template('index.html', recipes=recipes)

#Index page redirection
@app.route('/index.html')
def redirection():
    return redirect(url_for('index'))

#Create function
@app.route('/create.html', methods=('GET', 'POST'))
def create():
    conn = get_db_conn()

    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        guide = request.form['guide']
        servings = request.form['servings']

        if not title:
            flash('Title is required!')
            return redirect(url_for('index'))
        elif not ingredients:
            flash('Ingredients are required!')
            return redirect(url_for('index'))
        elif not guide:
            flash('Procedure is required!')
            return redirect(url_for('index'))
        elif not servings:
            flash('Servings is required!')
            return redirect(url_for('index'))
        else:
            conn.execute('INSERT INTO recipes (title, ingredients, guide, servings) VALUES (?, ?, ?, ?)', (title, ingredients, guide, servings,))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')

#Edit Recipe function
@app.route('/edit/<int:recipe_id>', methods=['GET', 'POST'])
def edit(recipe_id):
    conn = get_db_conn()

    if request.method == 'POST':
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')
        guide = request.form.get('guide')
        servings = request.form.get('servings')

        if not title:
            flash('Title is required!')
            return redirect(url_for('edit', recipe_id=recipe_id))
        elif not ingredients:
            flash('Ingredients are required!')
            return redirect(url_for('edit', recipe_id=recipe_id))
        elif not guide:
            flash('Procedure is required!')
            return redirect(url_for('edit', recipe_id=recipe_id))
        elif not servings:
            flash('Servings is required!')
            return redirect(url_for('edit', recipe_id=recipe_id))
        else:
            conn.execute('UPDATE recipes SET title = ?, ingredients = ?, guide = ?, servings = ? WHERE id = ?',
                         (title, ingredients, guide, servings, recipe_id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    
    recipe = conn.execute('SELECT id, title, ingredients, guide, servings FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
    if not recipe:
        flash('Recipe not found!')
        return redirect(url_for('index'))
    
    return render_template('edit.html', recipe=recipe)

#delete function
@app.route('/delete/<int:recipe_id>', methods=['POST'])
def delete(recipe_id):
    conn = get_db_conn()
    conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
    conn.commit()
    conn.close()
    flash('Recipe deleted successfully!')
    return redirect(url_for('index'))

#function to run
if __name__ == '__main__':
    app.run(debug=True)