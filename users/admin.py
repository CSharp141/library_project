from django.contrib import admin
from .models import Books, LateFee, Loan


# Register your models here.

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'subgenre', 'is_available']

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'loan_date', 'return_date', 'is_returned']

@admin.register(LateFee)
class LateFeeAdmin(admin.ModelAdmin):
    list_display = ['loan', 'amount', 'paid']