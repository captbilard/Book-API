import json

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse


from .models import Book, Publisher, Author
# Create your views here.

class PublisherList(View):
    def get(self, request):
        """Return a Json object of all the publishers """
        publishers = Publisher.objects.all()
        result = []
        for publisher in publishers:
            result.append({
                'id': publisher.id,
                'name': publisher.name
            })
        return JsonResponse({'result':result})

    def post(self, request):
        """Post a publisher into the database"""
        publisher = Publisher(name=json.loads(request.body)['name'])
        publisher.save()

        return JsonResponse({
            'id':publisher.id,
            'name': publisher.name
            
            }, status=201)
    
    





class PublisherOne(View):
    """Gets one publisher from the database"""
    def get(self, request, publisher_id):
        publisher = Publisher.objects.get(pk=publisher_id)
        return JsonResponse({
            'id': publisher.id,
            'name': publisher.name
        })
    
    def patch(self, request, publisher_id):
        """Updates a publisher in the database"""
        publisher = Publisher.objects.get(pk=publisher_id)
        publisher.name = json.loads(request.body)['name']
        publisher.save()

        return JsonResponse({
            'id': publisher.id,
            "name": publisher.name
        })

    def delete(self, request, publisher_id):
        """Deletes a particular publisher from the db"""
        Publisher.objects.get(pk=publisher_id).delete()
        return JsonResponse({}, status=204)




class AuthorList(View):
    def get(self, request):
        """Return a Json object of all the authors """
        authors = Author.objects.all()
        result = []
        for author in authors:
            result.append({
                'id': author.id,
                'name': author.name
            })
        return JsonResponse({'result':result})

    def post(self, request):
        """Post a author into the database"""
        author = Author(name=json.loads(request.body)['name'])
        author.save()

        return JsonResponse({
            'id':author.id,
            'name': author.name
            
            }, status=201)
    



class AuthorOne(View):
    """Gets one author from the database based on the id"""
    def get(self, request, author_id):
        author = Author.objects.get(pk=author_id)
        return JsonResponse({
            'id': author.id,
            'name': author.name
        })
    
    def patch(self, request, author_id):
        """Updates a publisher in the database"""
        author = Author.objects.get(pk=author_id)
        author.name = json.loads(request.body)['name']
        author.save()

        return JsonResponse({
            'id': author.id,
            "name": author.name
        })

    def delete(self, request, author_id):
        """Deletes a particular publisher from the db"""
        Author.objects.get(pk=author_id).delete()
        return JsonResponse({}, status=204)




class BookList(View):
    def get(self, request):
        """Endpoint to et all the books in the database."""
        result = []
        books = Book.objects.all()
        for book in books:
            result.append({
                'id': book.id,
                'title': book.title,
                'synopsis': book.synopsis,
                'published_date': book.published_date,
                'publisher_id': book.Publisher.id,
                'Publisher': book.Publisher.name,
                'Author_id': book.Author.id,
                'Author': book.Author.name
            })

        return JsonResponse({'result':result}, status=200) 
    
    def post(self, request):
        """Endpoint to add a book to the database"""
        result=[]
        
        book = Book(
            title=json.loads(request.body)['title'],
            synopsis=json.loads(request.body)['synopsis'],
            published_date=json.loads(request.body)['published_date'],
            Publisher_id=json.loads(request.body)['Publisher_id'],
            Author_id = json.loads(request.body)['Author_id']
        )
        book.save()
        result.append({
            'id': book.id,
            'title': book.title,
            'synopsis': book.synopsis,
            'published_date': book.published_date,
            'Publisher_id': book.Publisher.id,
            "Publisher": book.Publisher.name,
            'Author_id': book.Author.id,
            'Author' : book.Author.name
        })

        return JsonResponse({
            'result': result
        })



class BookOne(View):
    """Get's a particular book from the database"""
    def get(self, request, book_id):
        result =[]
        book = Book.objects.get(pk=book_id)
        result.append({
            'id': book.id,
            'title': book.title,
            'synopsis': book.synopsis,
            'published_date' : book.published_date,
            'publisher_id': book.Publisher.id,
            'Publisher': book.Publisher.name,
            'author_id': book.Author.id,
            'Author': book.Author.name
        })
        return JsonResponse({'result':result}, status = 200)
    
    def patch(self, request, book_id):
        """Updates a particular book based on
        if the entry was given or not"""
        result =[]
        book = Book.objects.get(pk=book_id)
        if json.loads(request.body).get('title'):
            book.title = json.loads(request.body).get('title')
        
        if json.loads(request.body).get('synopsis'):
            book.synopsis = json.loads(request.body).get('synopsis')
        
        if json.loads(request.body).get('published_date'):
            book.published_date = json.loads(request.body).get('published_date')
        
        if json.loads(request.body).get('Publisher_id'):
            book.Publisher_id = json.loads(request.body).get('Publisher_id')
        
        if json.loads(request.body).get('Author_id'):
            book.Author_id = json.loads(request.body).get('Author_id')
        
        book.save()
        result.append({
            'id': book.id,
            'title': book.title,
            'synopsis': book.synopsis,
            'published_date': book.published_date,
            'publisher_id' : book.Publisher.id,
            'Publisher' : book.Publisher.name,
            'author_id' : book.Author.id,
            'Author' : book.Author.name
        })

        return JsonResponse({'result': result}, status = 200)

    def delete(self, request, book_id):
        """Delete a book from the database"""
        Book.objects.get(pk=book_id).delete()
        return JsonResponse({}, status=204)
        


