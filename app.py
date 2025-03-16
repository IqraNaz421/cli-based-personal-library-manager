
import sqlite3
import os
import time
from tabulate import tabulate

# Database setup
conn = sqlite3.connect("library.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER
)
''')
conn.commit()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    clear_screen()
    print("=" * 40)
    print(f"{title.center(40)}")
    print("=" * 40)

def add_book():
    print_header("📌 ADD A NEW BOOK")
    title = input("Enter book title: ").strip()
    author = input("Enter book author: ").strip()
    year = input("Enter publication year: ").strip()
    
    if not title or not author or not year.isdigit():
        print("❌ Invalid input! Please enter correct details.")
        time.sleep(2)
        return
    
    cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, int(year)))
    conn.commit()
    print("✅ Book added successfully!")
    time.sleep(2)

def view_books():
    print_header("📚 YOUR LIBRARY COLLECTION")
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    if not books:
        print("❌ No books found!")
    else:
        print(tabulate(books, headers=["ID", "Title", "Author", "Year"], tablefmt="grid"))
    input("\nPress ENTER to return to the menu...")

def search_book():
    print_header("🔍 SEARCH FOR A BOOK")
    title = input("Enter book title to search: ").strip()
    cursor.execute("SELECT * FROM books WHERE title LIKE ?", ('%' + title + '%',))
    books = cursor.fetchall()
    if not books:
        print("❌ No matching books found!")
    else:
        print(tabulate(books, headers=["ID", "Title", "Author", "Year"], tablefmt="grid"))
    input("\nPress ENTER to return to the menu...")

def update_book():
    print_header("✏️ UPDATE A BOOK")
    book_id = input("Enter book ID to update: ").strip()
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    if not book:
        print("❌ Book not found!")
        time.sleep(2)
        return
    
    new_title = input("Enter new title: ").strip()
    new_author = input("Enter new author: ").strip()
    new_year = input("Enter new publication year: ").strip()
    
    if not new_title or not new_author or not new_year.isdigit():
        print("❌ Invalid input! Please enter correct details.")
        time.sleep(2)
        return
    
    cursor.execute("UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?", 
                   (new_title, new_author, int(new_year), book_id))
    conn.commit()
    print("✅ Book updated successfully!")
    time.sleep(2)

def delete_book():
    print_header("🗑️ DELETE A BOOK")
    book_id = input("Enter book ID to delete: ").strip()
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    if not book:
        print("❌ Book not found!")
        time.sleep(2)
        return
    
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    print("🗑️ Book deleted successfully!")
    time.sleep(2)

def main_menu():
    while True:
        print_header("📚 PERSONAL LIBRARY MANAGER 📚")
        print("1️⃣ Add a new book")
        print("2️⃣ View all books")
        print("3️⃣ Search for a book")
        print("4️⃣ Update a book")
        print("5️⃣ Delete a book")
        print("6️⃣ Exit")
        print("=" * 40)
        
        choice = input("Choose an option (1-6): ").strip()
        
        if choice == '1':
            add_book()
        elif choice == '2':
            view_books()
        elif choice == '3':
            search_book()
        elif choice == '4':
            update_book()
        elif choice == '5':
            delete_book()
        elif choice == '6':
            print("📖 Exiting Personal Library Manager... Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please enter a number between 1-6.")
            time.sleep(2)

if __name__ == "__main__":
    main_menu()
    conn.close()