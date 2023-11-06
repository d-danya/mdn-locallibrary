from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

import uuid
from datetime import date

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a book genre')
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField()
    isbn = models.CharField(max_length=13)
    genre = models.ManyToManyField(Genre)
    def __str__(self):
        return f'{self.author}: {self.title}'
    def get_absolute_url(self):
        return reverse('catalog:book-detail', args=[str(self.id),])

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    LOAN_STATUS = (
        ('m', 'Maitenance'), 
        ('o', 'On loan'), 
        ('a', 'Avalible'), 
        ('r', 'Reserved')
	)
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m')
    class Meta():
        ordering = ['due_back']
    def __str__(self):
        return f'{self.book}({str(self.id)[:5]})'
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        else:
            return False

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True)
    date_of_deth = models.DateField('Died', null=True, blank=True)
    def get_absolute_url(self):
        return reverse('catalog:author-detail', args=[str(self.id),])
    def __str__(self):
        return f'{self.last_name} {self.first_name}({self.date_of_birth})'

