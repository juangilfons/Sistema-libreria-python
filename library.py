import requests
import sqlite3
import book


def db_setup():
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS books (
        isbn TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        publisher TEXT NOT NULL,
        publish_date DATE NOT NULL,
        stock INTEGER
    )""")

    connection.commit()
    connection.close()


def get_book(isbn):
    response = requests.get(f"http://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=details&format=json")
    resp_json = response.json()

    if response.status_code != 200 or len(resp_json) == 0:
        return None
    else:
        title = resp_json[f'ISBN:{isbn}']['details']['title']
        author = resp_json[f'ISBN:{isbn}']['details']['authors'][0]['name']
        publisher = resp_json[f'ISBN:{isbn}']['details']['publishers'][0]
        date = resp_json[f'ISBN:{isbn}']['details']['publish_date']

        book_object = book.Book(title, author, publisher, date)

        return book_object


def add_book(isbn, amount):
    book_obj = get_book(isbn)
    book_obj.stock = amount
    if book_obj is not None:
        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM books WHERE isbn=?", (isbn,))

        book_exists = cursor.fetchone()

        if book_exists is None:
            cursor.execute("INSERT INTO books (isbn, title, author, publisher, publish_date, stock) VALUES (?, ?, ?, ?, ?, ?)",
                           (isbn, book_obj.title, book_obj.author, book_obj.publisher, book_obj.date, book_obj.stock))
            connection.commit()
            connection.close()
            return True

        connection.close()
    return False


def add_stock(isbn, amount):
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("UPDATE books SET stock = stock + ? WHERE isbn=?", (amount, isbn))

    connection.commit()
    connection.close()


def remove_stock(isbn, amount):
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("SELECT stock FROM books WHERE isbn=?", (isbn,))
    stock = cursor.fetchone()

    if stock[0] >= amount:
        cursor.execute("UPDATE books SET stock = stock - ? WHERE isbn=?", (amount, isbn))
        return True
    else:
        return False


def remove_book(isbn):
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM books WHERE isbn=?", (isbn,))

    connection.commit()
    connection.close()


def all_books():
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    connection.close()
    return books


def main_terminal_ui():
    db_setup()

    print("Welcome to our Library!")
    print("~~~~~~~~~~~~~~~~~~~~~~~")
    while True:
        print("Please choose an option:\n")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. View Available Books")
        print("4. Exit\n")

        user_input = input("Your choice: ")

        if user_input == "1":
            isbn = input("Enter ISBN: ")
            if add_book(isbn) is False:
                print("isbn not found or already exists")
            else:
                print("Book added successfully!\n")
        elif user_input == "2":
            isbn = input("Enter ISBN: ")
            remove_book(isbn)
            print("Book removed successfully!\n")
        elif user_input == "3":
            books = all_books()
            for book in books:
                print(book)
        elif user_input == "4":
            print("Thank you for using our Library!")
            exit()
        else:
            print("Invalid input. Please choose a valid option.\n")


main_terminal_ui()
