from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic import edit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse, reverse_lazy

import datetime

from .models import Book, BookInstance, Author, Genre
from . import forms

def index(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_avalable = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.all().count()
    num_genres = Genre.objects.all().count()
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_avalable': num_instances_avalable,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_visits': num_visits,
    }
    return render(request, 'catalog/index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'catalog/books.html'
    paginate_by = 2

class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'catalog/book-detail.html'

class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'authors'
    template_name = 'catalog/authors.html'
    paginate_by = 2

class AuthorDetailView(generic.DetailView):
    model = Author
    context_object_name = 'author'
    template_name = 'catalog/author-detail.html'

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    context_object_name = 'books'
    template_name = 'catalog/my-borrowed.html'
    paginate_by = 3
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

@staff_member_required
def borrowed_books(request):
    books = BookInstance.objects.filter(status__exact='o')
    context = {'books': books}
    return render(request, 'catalog/borrowed-books.html', context=context)
"""
class BorrowedBooksListView(StaffuserRequiredMixin, generic.ListView):
    model = BookInstance
    context_object_name = 'books'
    template_name = 'catalog/borrowed-books.html'
    paginate_by = 2
    def get_queryset(self):
        return BookInstance.objects.filter(status_exact='o').order_by('due_back')
"""

@staff_member_required
def renew_book_librarian(request, pk):
    bookinst = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        form = forms.RenewBookForm(request.POST)
        if form.is_valid():
            bookinst.due_back = form.cleaned_data['renewal_date']
            bookinst.save()
            return HttpResponseRedirect(reverse('catalog:borrowed-books'))
    else: 
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = forms.RenewBookForm(initial={'renewal_date': proposed_renewal_date,})
    context = {
        'form': form,
        'bookinst': bookinst,
    }
    return render(request, 'catalog/book_renew_librarian.html', context=context)

class AuthorCreate(edit.CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_deth': datetime.date.today()}

class AuthorUpdate(edit.UpdateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_deth': datetime.date.today()}

class AuthorDelete(edit.DeleteView):
    model = Author
    success_url = reverse_lazy('catolog:authors')

class BookCreate(edit.CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(edit.UpdateView):
    model = Book
    fields = '__all__'

class BookDelete(edit.DeleteView):
    model = Book
    success_url = reverse_lazy('catalog:book-detail')