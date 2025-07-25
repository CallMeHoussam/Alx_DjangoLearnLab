from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Book
from .forms import BookForm

@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_create_book', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        Book.objects.create(
            title=request.POST['title'],
            author=request.POST['author'],
            published_date=request.POST['published_date']
        )
        return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})
def book_search(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(
        Q(title__icontains=query) | Q(author__icontains=query)
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_edit_book', raise_exception=True)
def book_edit(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.published_date = request.POST['published_date']
        book.save()
        return redirect('book_list')
    return render(request, 'books/edit.html', {'book': book})

@login_required
@permission_required('bookshelf.can_delete_book', raise_exception=True)
def book_delete(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/delete.html', {'book': book})