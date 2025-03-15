import streamlit as st
import json
import os

# File to store book data
STORAGE_FILE = "books_data.json"

# Function to load books from JSON file
def load_books():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

# Function to save books to JSON file
def save_books(books):
    with open(STORAGE_FILE, "w") as file:
        json.dump(books, file, indent=4)

# Load books at the start
books = load_books()

# Streamlit UI
st.title("📚 Book Collection Manager")

# Sidebar Menu
menu = st.sidebar.selectbox("Select an option", ["View Books", "Add Book", "Search Book", "Update Book", "Delete Book", "Reading Progress"])

# 📌 View All Books
if menu == "View Books":
    st.subheader("📖 Your Book Collection")
    if books:
        for book in books:
            st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} | {'✅ Read' if book['read'] else '❌ Unread'}")
    else:
        st.warning("No books in your collection.")

# 📌 Add a New Book
elif menu == "Add Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.text_input("Publication Year")
    genre = st.text_input("Genre")
    read = st.checkbox("Have you read this book?")

    if st.button("Add Book"):
        if title and author and year and genre:
            books.append({"title": title, "author": author, "year": year, "genre": genre, "read": read})
            save_books(books)
            st.success("Book added successfully!")
        else:
            st.error("Please fill in all fields.")

# 📌 Search for a Book
elif menu == "Search Book":
    st.subheader("🔍 Search for a Book")
    search_query = st.text_input("Enter title or author to search:")
    
    if st.button("Search"):
        results = [book for book in books if search_query.lower() in book["title"].lower() or search_query.lower() in book["author"].lower()]
        if results:
            for book in results:
                st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} | {'✅ Read' if book['read'] else '❌ Unread'}")
        else:
            st.warning("No matching books found.")

# 📌 Update a Book
elif menu == "Update Book":
    st.subheader("✏️ Update a Book")
    book_titles = [book["title"] for book in books]
    selected_book = st.selectbox("Select a book to update", [""] + book_titles)

    if selected_book:
        book = next((b for b in books if b["title"] == selected_book), None)
        if book:
            new_title = st.text_input("New Title", book["title"])
            new_author = st.text_input("New Author", book["author"])
            new_year = st.text_input("New Year", book["year"])
            new_genre = st.text_input("New Genre", book["genre"])
            new_read = st.checkbox("Have you read this book?", book["read"])

            if st.button("Update Book"):
                book.update({"title": new_title, "author": new_author, "year": new_year, "genre": new_genre, "read": new_read})
                save_books(books)
                st.success("Book updated successfully!")

# 📌 Delete a Book
elif menu == "Delete Book":
    st.subheader("🗑️ Delete a Book")
    book_titles = [book["title"] for book in books]
    selected_book = st.selectbox("Select a book to delete", [""] + book_titles)

    if selected_book and st.button("Delete Book"):
        books = [book for book in books if book["title"] != selected_book]
        save_books(books)
        st.success("Book deleted successfully!")

# 📌 Show Reading Progress
elif menu == "Reading Progress":
    st.subheader("📊 Your Reading Progress")
    total_books = len(books)
    read_books = sum(1 for book in books if book["read"])
    progress = (read_books / total_books) * 100 if total_books > 0 else 0

    st.write(f"Total Books: {total_books}")
    st.write(f"Books Read: {read_books}")
    st.progress(progress / 100)
    st.write(f"Reading Completion: {progress:.2f}%")

