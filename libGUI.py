import tkinter as tk
from tkinter import messagebox
import json
import os

# Initialize empty dictionaries to store books and members
books = {}
members = {}

# File names for storing data
BOOKS_FILE = "books.json"
MEMBERS_FILE = "members.json"

# Load existing data from files
def load_data():
    global books, members
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, 'r') as f:
            books = json.load(f)
    if os.path.exists(MEMBERS_FILE):
        with open(MEMBERS_FILE, 'r') as f:
            members = json.load(f)

# Save data to files
def save_data():
    with open(BOOKS_FILE, 'w') as f:
        json.dump(books, f)
    with open(MEMBERS_FILE, 'w') as f:
        json.dump(members, f)

# Add book function
def add_book():
    title = book_title_entry.get()
    author = book_author_entry.get()
    if title and author:
        books[title] = {"author": author, "available": True}
        messagebox.showinfo("Success", f"Book '{title}' added successfully.")
        book_title_entry.delete(0, tk.END)
        book_author_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please enter both title and author.")

# Delete book function
def delete_book():
    title = book_title_entry.get()
    if title in books:
        del books[title]
        messagebox.showinfo("Success", f"Book '{title}' deleted successfully.")
        book_title_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Book not found.")

# Check if a book exists
def check_book():
    title = book_title_entry.get()
    if title in books:
        status = "available" if books[title]["available"] else "borrowed"
        messagebox.showinfo("Info", f"Book '{title}' exists and is currently {status}.")
    else:
        messagebox.showerror("Error", "Book not found.")

# Register member function
def register_member():
    name = member_name_entry.get()
    if name:
        member_id = str(len(members) + 1)
        members[member_id] = {"name": name, "books": []}
        messagebox.showinfo("Success", f"Member '{name}' registered with ID: {member_id}")
        member_name_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please enter a name.")

# Borrow book function
def borrow_book():
    member_id = member_id_entry.get()
    title = book_title_entry.get()

    if member_id in members and title in books and books[title]["available"]:
        books[title]["available"] = False
        members[member_id]["books"].append(title)
        messagebox.showinfo("Success", f"Book '{title}' borrowed successfully.")
        book_title_entry.delete(0, tk.END)
        member_id_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Invalid member ID, book title, or the book is not available.")

# Return book function
def return_book():
    member_id = member_id_entry.get()
    title = book_title_entry.get()

    if member_id in members and title in members[member_id]["books"]:
        books[title]["available"] = True
        members[member_id]["books"].remove(title)
        messagebox.showinfo("Success", f"Book '{title}' returned successfully.")
        book_title_entry.delete(0, tk.END)
        member_id_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Invalid member ID or the book was not borrowed.")

# Display all books
def display_books():
    if not books:
        messagebox.showinfo("Books", "No books in the library.")
    else:
        books_list = "\n".join([f"{title} by {info['author']} ({'Available' if info['available'] else 'Borrowed'})" for title, info in books.items()])
        messagebox.showinfo("Books", f"Books in the library:\n{books_list}")

# Display all members
def display_members():
    if not members:
        messagebox.showinfo("Members", "No registered members.")
    else:
        members_list = "\n".join([f"ID: {member_id}, Name: {info['name']}, Books borrowed: {', '.join(info['books'])}" for member_id, info in members.items()])
        messagebox.showinfo("Members", f"Registered members:\n{members_list}")

# Main GUI setup
root = tk.Tk()
root.title("Library Management System")

# Add book section
tk.Label(root, text="Book Title:").grid(row=0, column=0, padx=10, pady=5)
book_title_entry = tk.Entry(root)
book_title_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Book Author:").grid(row=1, column=0, padx=10, pady=5)
book_author_entry = tk.Entry(root)
book_author_entry.grid(row=1, column=1, padx=10, pady=5)

add_book_button = tk.Button(root, text="Add Book", command=add_book)
add_book_button.grid(row=2, column=0, columnspan=2, pady=10)

# Delete book section
delete_book_button = tk.Button(root, text="Delete Book", command=delete_book)
delete_book_button.grid(row=3, column=0, columnspan=2, pady=10)

# Check book section
check_book_button = tk.Button(root, text="Check Book", command=check_book)
check_book_button.grid(row=4, column=0, columnspan=2, pady=10)

# Register member section
tk.Label(root, text="Member Name:").grid(row=5, column=0, padx=10, pady=5)
member_name_entry = tk.Entry(root)
member_name_entry.grid(row=5, column=1, padx=10, pady=5)

register_member_button = tk.Button(root, text="Register Member", command=register_member)
register_member_button.grid(row=6, column=0, columnspan=2, pady=10)

# Borrow book section
tk.Label(root, text="Member ID:").grid(row=7, column=0, padx=10, pady=5)
member_id_entry = tk.Entry(root)
member_id_entry.grid(row=7, column=1, padx=10, pady=5)

borrow_book_button = tk.Button(root, text="Borrow Book", command=borrow_book)
borrow_book_button.grid(row=8, column=0, columnspan=2, pady=10)

# Return book section
return_book_button = tk.Button(root, text="Return Book", command=return_book)
return_book_button.grid(row=9, column=0, columnspan=2, pady=10)

# Display books section
display_books_button = tk.Button(root, text="Display All Books", command=display_books)
display_books_button.grid(row=10, column=0, columnspan=2, pady=10)

# Display members section
display_members_button = tk.Button(root, text="Display All Members", command=display_members)
display_members_button.grid(row=11, column=0, columnspan=2, pady=10)

# Save and exit button
save_exit_button = tk.Button(root, text="Save and Exit", command=lambda: [save_data(), root.destroy()])
save_exit_button.grid(row=12, column=0, columnspan=2, pady=10)

# Load data and run the application
load_data()
root.mainloop()
