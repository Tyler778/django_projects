from turtle import title
from unicodedata import name
from django.shortcuts import render

# Create your views here.

from .models import Book, Author, BookInstance, Genre

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()


    #Genres that Contain the Letter F
    num_genre_f = Genre.objects.filter(name__contains='f').count()

    #Books that contain the letter S
    num_books_s = Book.objects.filter(title__contains='s').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre_f': num_genre_f,
        'num_books_s': num_books_s
        
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)




#ListView
from django.views import generic

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10   


#detailView
class BookDetailView(generic.DetailView):
    model = Book
