from turtle import title
from unicodedata import name
from django.shortcuts import render

# Create your views here.

from .models import Book, Author, BookInstance, Genre

def index(request):
    """View function for home page of site."""
    request = request
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    #Number of Visits
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

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
        'num_books_s': num_books_s,
        'num_visits': num_visits,
        
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)




#ListView
from django.views import generic

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10   

from django.contrib.auth.mixins import LoginRequiredMixin
#detailView

class BookDetailView(generic.DetailView):
    model = Book


#listAuthors
class AuthorListView(generic.ListView):
    model = Author

#detailAuthorView
class AuthorDetailView(generic.DetailView):
    model = Author


from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


from django.contrib.auth.mixins import PermissionRequiredMixin

class LoanedBooksLibrarianListView(PermissionRequiredMixin,generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_librarian.html'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')