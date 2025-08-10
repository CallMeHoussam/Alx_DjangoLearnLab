
from rest_framework import generics,filters
from .models import  Book
from .serializers import  BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework

# Create your views here.
# def index(request):
#     return HttpResponse("Hello, world! This is the API index page.")

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    #enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'publication_year','title']  # Assuming 'author' is a ForeignKey in Book model,
    
        
    search_fields = ['title']  # Assuming 'author' is a ForeignKey in Book model
    ordering_fields = ['title', 'publication_year']  # Assuming these fields exist in the
    ordering = ['title','publication_year']  # Default ordering
    
    
class BookDetailView(generics.RetrieveAPIView):
    queryset =Book.objects.all()
    serializer_class = BookSerializer
    permission_classes =[IsAuthenticatedOrReadOnly]
    
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]