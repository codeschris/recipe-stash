from flask import Flask, render_template, request, flash, redirect, url_for
import sqlite3
import markdown

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisaclassproject'

def get_db_conn():
    conn = sqlite3.connect('proj_db.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_conn()
    db_recipes = conn.execute('SELECT id, created, title, ingredients, guide, servings FROM recipes;').fetchall()

    recipes = []
    for recipe in db_recipes:
        recipe = dict(recipe)
        recipe['title'] = markdown.markdown(recipe['title'])
        recipe['ingredients'] = markdown.markdown(recipe['ingredients'])
        recipe['guide'] = markdown.markdown(recipe['guide'])
        recipe['servings'] = markdown.markdown(recipe['servings'])

        recipes.append(recipe)
    
    return render_template('index.html', recipes=recipes)

@app.route('/index.html')
def redirection():
    return redirect(url_for('index'))

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
        if not ingredients:
            flash('Ingredients are required!')
            return redirect(url_for('index'))
        if not guide:
            flash('Procedure is required!')
            return redirect(url_for('index'))
        if not servings:
            flash('Servings is required!')
            return redirect(url_for('index'))
        
        conn.execute('INSERT INTO recipes (title, ingredients, guide, servings) VALUES (?, ?, ?, ?)', (title, ingredients, guide, servings,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/delete/<int:recipe_id>', methods=['POST'])
def delete(recipe_id):
    conn = get_db_conn()
    conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
    conn.commit()
    conn.close()
    flash('Recipe deleted successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)