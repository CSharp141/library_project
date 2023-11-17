from django.db import models

# Create your models here.
class Users(models.Model):
     # Define the choices for the 'role' field
    STUDENT = 'student'
    STAFF = 'staff'
    LIBRARIAN = 'librarian'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (STAFF, 'Staff'),
        (LIBRARIAN, 'Librarian'),
        (ADMIN, 'Admin'),
    ]

    # Add the custom 'role' field
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)

    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    userName = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.userName
