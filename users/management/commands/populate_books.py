import csv
from django.core.management.base import BaseCommand
from users.models import Books  # Replace "your_app" with the actual name of your Django app

class Command(BaseCommand):
    help = 'Populate the Book model with data from the CSV file'

    def handle(self, *args, **kwargs):
        # Path to your CSV file
        csv_file_path = 'books.csv'

        # Open the CSV file and iterate through its rows
        with open(csv_file_path, 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                print(row)
                # Create a Books instance and populate its fields
                book = Books(
                    title=row['Title'],
                    author=row['Author'],
                    genre=row['Genre'],
                    subgenre=row['SubGenre']
                )
                book.save()

                print(f'Successfully added book: {book}')