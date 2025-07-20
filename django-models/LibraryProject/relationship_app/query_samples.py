from relationship_app.models import Author, Book, Library, Librarian

def get_books_by_author(author_name):
    """Query all books by a specific author"""
    try:
        author = Author.objects.get(name=author_name)
        return author.books.all()  # Using the related_name 'books'
    except Author.DoesNotExist:
        return Book.objects.none()

def get_books_in_library(library_name):
    """List all books in a library"""
    try:
        library = Library.objects.get(name=library_name)
        return library.books.all()
    except Library.DoesNotExist:
        return Book.objects.none()

def get_librarian_for_library(library_name):
    """Retrieve the librarian for a library"""
    try:
        library = Library.objects.get(name=library_name)
        return library.librarian  # Using the related_name 'librarian'
    except Library.DoesNotExist:
        return None

# Example usage:
if __name__ == "__main__":
    # Create sample data
    author1 = Author.objects.create(name="J.K. Rowling")
    book1 = Book.objects.create(title="Harry Potter 1", author=author1)
    book2 = Book.objects.create(title="Harry Potter 2", author=author1)
    
    library1 = Library.objects.create(name="Central Library")
    library1.books.add(book1, book2)
    
    librarian1 = Librarian.objects.create(name="Ms. Smith", library=library1)
    
    # Test the queries
    print("Books by J.K. Rowling:")
    for book in get_books_by_author("J.K. Rowling"):
        print(f"- {book.title}")
    
    print("\nBooks in Central Library:")
    for book in get_books_in_library("Central Library"):
        print(f"- {book.title}")
    
    print("\nLibrarian for Central Library:")
    librarian = get_librarian_for_library("Central Library")
    print(librarian.name if librarian else "No librarian found")
