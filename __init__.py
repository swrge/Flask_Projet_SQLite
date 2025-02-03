from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'

def get_db_connection():
    conn = sqlite3.connect('bibliotheque.db')
    conn.row_factory = sqlite3.Row
    return conn

# Simple user session management 
def is_logged_in():
    return 'user_id' in session

def is_admin():
    return session.get('role') == 'admin'

@app.route('/')
def index():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # Plain text password
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                          (username, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash('Successfully logged in!')
            return redirect(url_for('index'))
        
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # Plain text password
        email = request.form['email']
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)',
                        (username, password, email, 'member'))
            conn.commit()
            flash('Registration successful!')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists!')
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    if not is_admin():
        flash('Admin access required')
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        isbn = request.form['isbn']
        publication_year = request.form['publication_year']
        quantity = request.form['quantity']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO books (title, author, genre, isbn, publication_year, quantity) VALUES (?, ?, ?, ?, ?, ?)',
                    (title, author, genre, isbn, publication_year, quantity))
        conn.commit()
        conn.close()
        flash('Book successfully added!')
        return redirect(url_for('index'))
    
    return render_template('add_book.html')

@app.route('/books/borrow/<int:book_id>', methods=['POST'])
def borrow_book():
    if not is_logged_in():
        flash('Please login to borrow books')
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE book_id = ?', (book_id,)).fetchone()
    
    if book['quantity'] > 0:
        conn.execute('UPDATE books SET quantity = quantity - 1 WHERE book_id = ?', (book_id,))
        conn.execute('INSERT INTO loans (user_id, book_id, status) VALUES (?, ?, ?)',
                    (session['user_id'], book_id, 'active'))
        conn.commit()
        flash('Book borrowed successfully!')
    else:
        flash('Book not available')
    
    conn.close()
    return redirect(url_for('index'))

@app.route('/books/search')
def search_books():
    query = request.args.get('q', '')
    conn = get_db_connection()
    books = conn.execute(
        'SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?',
        (f'%{query}%', f'%{query}%', f'%{query}%')
    ).fetchall()
    conn.close()
    return render_template('search_results.html', books=books, query=query)

if __name__ == '__main__':
    app.run(debug=True)
