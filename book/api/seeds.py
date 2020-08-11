import random

from faker import Faker
from faker.providers import date_time

from .models import Author, Publisher, Book

#Instantiate the faker class
fake = Faker()

def seed_data():
    """Generate Random name and store 
    it in the database as names of 
    authors"""
    
    list_of_authors = []
    for _ in range(1,11):
        author=Author(name=fake.name())
        author.save()
        list_of_authors.append(author)
        print(list_of_authors)

    """Generate Random name and store 
    it in the database as names of 
    publishers"""
    list_of_publishers = []
    for _ in range(1, 11):
        publisher = Publisher(name = fake.company())
        publisher.save()
        list_of_publishers.append(publisher)
        print(list_of_publishers)
    
    """Generate Random name and store 
    it in the database as title of 
    the book
    -> fake.word gives just a single fake word
    -> fake.date_between is used to generate dates 
    --- between a specific time frame
    """
    for _ in range(1, 101):
        book = Book(
            title = fake.word().capitalize(),
            synopsis = fake.text(),
            published_date= fake.date_between(start_date='-600d', end_date='now'),
            Publisher = random.choice(list_of_publishers),
            Author = random.choice(list_of_authors)
            )
        book.save()

