from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Books(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=50)
    subgenre = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class Loan(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.book.title}'
    
class LateFee(models.Model):
    loan = models.OneToOneField(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Adjust precision as needed
    paid = models.BooleanField(default=False)

    def get_username(self):
        return self.loan.user.username

    def __str__(self):
        return f'{self.loan.user.username} - {self.loan.book.title} - Late Fee'
