from django.core.management.base import BaseCommand
from users.models import Books  # Replace "your_app" with the actual name of your Django app

class Command(BaseCommand):
    help = 'Delete all records in the Books table'

    def handle(self, *args, **kwargs):
        Books.objects.all().delete()
        print('All records in the Books table have been deleted.')