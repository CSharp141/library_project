from django.contrib import admin
from .models import Books


# Register your models here.

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'subgenre', 'is_available']