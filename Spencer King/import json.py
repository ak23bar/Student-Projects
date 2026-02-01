import json

class Library:
    def __init__(self, name):
        self.name = name
        self.books = []
       # self.load_books()
        
    def add_books(self, title, author):
        book = (title, author, True)
        self.books.append(book)
        print("Done!")
        
    def burrow_book()