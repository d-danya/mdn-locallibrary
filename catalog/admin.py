from django.contrib import admin

from .models import Genre, Book, BookInstance, Author

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', )
    inlines = [BookInstanceInline]

class BookInline(admin.TabularInline):
    model = Book
    extra = 0

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_deth')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_deth')]
    inlines = [BookInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back', 'id', 'borrower')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Avalability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
    list_display = ('book', 'status', 'due_back', 'id')

admin.site.register(Genre)
