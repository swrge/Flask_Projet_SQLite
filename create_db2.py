import sqlite3

# Connect to the database or create it if it doesn't exist
connection = sqlite3.connect('books.db')

# Execute the schema script to create tables
with open('schema2.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Insert books into the database
cur.execute("INSERT INTO Books (title, author, genre, isbn, publication_year, quantity) VALUES (?, ?, ?, ?, ?, ?)",
            ('To Kill a Mockingbird', 'Harper Lee', 'Fiction', '9780061120084', 1960, 10))
cur.execute("INSERT INTO Books (title, author, genre, isbn, publication_year, quantity) VALUES (?, ?, ?, ?, ?, ?)",
            ('1984', 'George Orwell', 'Dystopian', '9780451524935', 1949, 8))
cur.execute("INSERT INTO Books (title, author, genre, isbn, publication_year, quantity) VALUES (?, ?, ?, ?, ?, ?)",
            ('Pride and Prejudice', 'Jane Austen', 'Romance', '9780141040349', 1813, 5))
cur.execute("INSERT INTO Books (title, author, genre, isbn, publication_year, quantity) VALUES (?, ?, ?, ?, ?, ?)",
            ('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', '9780743273565', 1925, 7))
cur.execute("INSERT INTO Books (title, author, genre, isbn, publication_year, quantity) VALUES (?, ?, ?, ?, ?, ?)",
            ('Moby Dick', 'Herman Melville', 'Adventure', '9781503280786', 1851, 4))
cur.execute("INSERT INTO Books (title, author, genre, isbn, publication_year, quantity) VALUES (?, ?, ?, ?, ?, ?)",
            ('The Catcher in the Rye', 'J.D. Salinger', 'Fiction', '9780316769488', 1951, 6))
cur.execute("INSERT INTO Books (title, author, genre, isbn, publication_year, quantity) VALUES (?, ?, ?, ?, ?, ?)",
            ('War and Peace', 'Leo Tolstoy', 'Historical', '9780199232765', 1869, 3))
cur.execute("INSERT INTO Books (title, author, genre, isbn, publication_year, quantity) VALUES (?, ?, ?, ?, ?, ?)",
            ('The Hobbit', 'J.R.R. Tolkien', 'Fantasy', '9780261102217', 1937, 12))
cur.execute("INSERT INTO Books (title, author, genre, isbn, publication_year, quantity) VALUES (?, ?, ?, ?, ?, ?)",
            ('Brave New World', 'Aldous Huxley', 'Science Fiction', '9780060850524', 1932, 9))
cur.execute("INSERT INTO Books (title, author, genre, isbn, publication_year, quantity) VALUES (?, ?, ?, ?, ?, ?)",
            ('The Adventures of Sherlock Holmes', 'Arthur Conan Doyle', 'Mystery', '9780141034327', 1892, 5))

# Commit the changes and close the connection
connection.commit()
connection.close()
