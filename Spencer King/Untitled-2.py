book_one = ("Harry Potter", "J.K. Rowling")

book_two = ("The Bible", "Multiple authors")

library = [book_one, book_two]

def display_books(library):
    for book in library:
        print(library)



def add_book(library):
    title = input("What book is the title of the book you want to add: ")
    author = input("What is the author of the book: ")
    new_book = (title, author)
    library.append(new_book)
    print("Book added.")
    
#add_book(library)

def borrow_book(library):
    borrow = input("What book do you want to borrow: ")
    for book in library:
        if book[0].lower() == borrow.lower():
            library.remove(book)
            print("You have borrowed this book: " + borrow)
            return
                
borrow_book(library)

display_books(library)

             