```markdown
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book.save()

book = Book.objects.get(title="1984")
print(f"Title: {book.title}, Author: {book.author}, Year: {book.publication_year}")

book.title = "Nineteen Eighty-Four"
book.save()
updated_book = Book.objects.get(pk=book.id)
print(updated_book.title)

book.delete()
books = Book.objects.all()
print(books)
