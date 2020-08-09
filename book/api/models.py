from django.db import models

# Create your models here.
class Publisher(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=50)
    synopsis = models.TextField()
    published_date = models.DateField()
    Publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    Author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title