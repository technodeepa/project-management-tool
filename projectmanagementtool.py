from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(_name_)

# Database initialization
conn = sqlite3.connect('project_management.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL)''')
c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                assigned_to INTEGER,
                FOREIGN KEY (assigned_to) REFERENCES users(id))''')
conn.commit()


# Home page - displays list of users and tasks
@app.route('/')
def index():
    # Retrieve users from the database
    c.execute('SELECT * FROM users')
    users = c.fetchall()

    # Retrieve tasks from the database
    c.execute('SELECT tasks.id, tasks.title, tasks.description, users.username FROM tasks LEFT JOIN users ON tasks.assigned_to = users.id')
    tasks = c.fetchall()

    return render_template('index.html', users=users, tasks=tasks)


# Add a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    email = request.form['email']

    # Insert user into the database
    c.execute('INSERT INTO users (username, email) VALUES (?, ?)', (username, email))
    conn.commit()

    return redirect(url_for('index'))


# Add a new task
@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    assigned_to = request.form['assigned_to']

    # Insert task into the database
    c.execute('INSERT INTO tasks (title, description, assigned_to) VALUES (?, ?, ?)', (title, description, assigned_to))
    conn.commit()

    return redirect(url_for('index'))


if _name_ == '_main_':
    app.run(debug=True)
