# app.py

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import csv

app = Flask(__name__)

# Create and populate the database
def create_database():
    conn = sqlite3.connect('cricket.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cricket_data (
            batsman_id INTEGER PRIMARY KEY,
            batsman_name TEXT,
            bowler_id INTEGER,
            score INTEGER
        )
    ''')

    with open('C:/Users/cadet/OneDrive/Desktop/New folder/3rd Semester/PAI Assignment 01/LAB 13/LAB !$/Ball_by_Ball.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header
        for row in csv_reader:
            cursor.execute('''
                INSERT INTO cricket_data (batsman_name, bowler_id, score) 
                VALUES (?, ?, ?)
            ''', (row[0], row[1], row[2]))

    conn.commit()
    conn.close()

# Show all data on the browser
@app.route('/')
def show_all():
    conn = sqlite3.connect('cricket.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cricket_data ORDER BY bowler_id')
    data = cursor.fetchall()
    conn.close()
    return render_template('show_all.html', data=data)

# Get data from the database and show only the records sorted by bowler ID
@app.route('/sorted_by_bowler')
def sorted_by_bowler():
    conn = sqlite3.connect('cricket.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cricket_data ORDER BY bowler_id')
    data = cursor.fetchall()
    conn.close()
    return render_template('sorted_by_bowler.html', data=data)

# Add a new record to the database using a form
@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        batsman_name = request.form['batsman_name']
        bowler_id = request.form['bowler_id']
        score = request.form['score']

        conn = sqlite3.connect('cricket.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cricket_data (batsman_name, bowler_id, score) 
            VALUES (?, ?, ?)
        ''', (batsman_name, bowler_id, score))

        conn.commit()
        conn.close()

        return redirect(url_for('show_all'))

    return render_template('add_record.html')

# Get Bowler ID from the form and show all records with that ID
@app.route('/get_by_bowler_form', methods=['GET', 'POST'])
def get_by_bowler():
    if request.method == 'POST':
        bowler_id = request.form['bowler_id']

        conn = sqlite3.connect('cricket.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cricket_data WHERE bowler_id = ? ORDER BY bowler_id', (bowler_id,))
        data = cursor.fetchall()
        conn.close()

        return render_template('get_by_bowler.html', data=data)

    return render_template('get_by_bowler_form.html')

if __name__ == '__main__':
    create_database()
    app.run(debug=True)
