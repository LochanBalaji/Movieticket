# -*- coding: utf-8 -*-
"""
Created on Tue May  7 09:55:24 2024

@author: Lochan
"""

from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create a basic SQLite database for storing dishes
def init_db():
    with sqlite3.connect('restaurant.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS dishes
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         name TEXT, 
                         category TEXT, 
                         price REAL)''')
@app.route('/')
def home():
    # Fetch all dishes from the database
    with sqlite3.connect('restaurant.db') as conn:
        dishes = conn.execute('SELECT * FROM dishes').fetchall()
    return render_template('restaurant.html', dishes=dishes)

@app.route('/add', methods=['POST'])
def add_dish():
    name = request.form['name']
    category = request.form['category']
    price = float(request.form['price'])
    with sqlite3.connect('restaurant.db') as conn:
        conn.execute('INSERT INTO dishes (name, category, price) VALUES (?, ?, ?)', (name, category, price))
    return redirect(url_for('home'))

@app.route('/update', methods=['POST'])
def update_dish():
    dish_id = int(request.form['id'])
    name = request.form['name']
    category = request.form['category']
    price = float(request.form['price'])
    with sqlite3.connect('restaurant.db') as conn:
        conn.execute('UPDATE dishes SET name=?, category=?, price=? WHERE id=?', (name, category, price, dish_id))
    return 'Dish updated successfully!'

@app.route('/delete', methods=['POST'])
def delete_dish():
    dish_id = int(request.form['id'])
    with sqlite3.connect('restaurant.db') as conn:
        conn.execute('DELETE FROM dishes WHERE id=?', (dish_id,))
    return 'Dish deleted successfully!'

@app.route('/search', methods=['GET'])
def search_dishes():
    search_query = request.args.get('query', '')
    with sqlite3.connect('restaurant.db') as conn:
        results = conn.execute('SELECT * FROM dishes WHERE name LIKE ? OR category LIKE ?', (f'%{search_query}%', f'%{search_query}%')).fetchall()
    return jsonify(results)

if __name__ == '_main_':
    init_db()
    app.run(port=9001)