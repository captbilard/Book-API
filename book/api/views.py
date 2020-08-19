import json
from datetime import datetime


from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend


from .models import Book, Publisher, Author
from .serializers import AuthorSerializer, BookSerializer, PublisherSerializer
# Create your views here.


class PublisherListView(viewsets.ModelViewSet):
    """This uses the DRF framework serializer
    and viewset model to handle all the 
    endpoints we manually specified
    for the publisher class"""
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

class AuthorListView(viewsets.ModelViewSet):
    """This uses the DRF framework serializer
    and viewset model to handle all the 
    endpoints we manually specified
    for the Author class"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookListView(viewsets.ModelViewSet):
    """"This uses the DRF framework serializer
    and viewset model to handle all the 
    endpoints we manually specified
    for the Book class"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['title','published_date', 'Author']
    filterset_fields = ['Author', 'Publisher', 'published_date']

# class PublisherList(View):
#     def get(self, request):
#         """Return a Json object of all the publishers """
#         publishers = Publisher.objects.all()
#         result = []
#         for publisher in publishers:
#             result.append({
#                 'id': publisher.id,
#                 'name': publisher.name
#             })
#         return JsonResponse({'result':result})

#     def post(self, request):
#         """Post a publisher into the database"""
#         publisher = Publisher(name=json.loads(request.body)['name'])
#         publisher.save()

#         return JsonResponse({
#             'id':publisher.id,
#             'name': publisher.name
            
#             }, status=201)
    


# class PublisherOne(View):
#     """Gets one publisher from the database"""
#     def get(self, request, publisher_id):
#         publisher = Publisher.objects.get(pk=publisher_id)
#         return JsonResponse({
#             'id': publisher.id,
#             'name': publisher.name
#         })
    
#     def patch(self, request, publisher_id):
#         """Updates a publisher in the database"""
#         publisher = Publisher.objects.get(pk=publisher_id)
#         publisher.name = json.loads(request.body)['name']
#         publisher.save()

#         return JsonResponse({
#             'id': publisher.id,
#             "name": publisher.name
#         })

#     def delete(self, request, publisher_id):
#         """Deletes a particular publisher from the db"""
#         Publisher.objects.get(pk=publisher_id).delete()
#         return JsonResponse({}, status=204)




# class AuthorList(View):
#     def get(self, request):
#         """Return a Json object of all the authors """
#         authors = Author.objects.all()
#         result = []
#         for author in authors:
#             result.append({
#                 'id': author.id,
#                 'name': author.name
#             })
#         return JsonResponse({'result':result})

#     def post(self, request):
#         """Post a author into the database"""
#         author = Author(name=json.loads(request.body)['name'])
#         author.save()

#         return JsonResponse({
#             'id':author.id,
#             'name': author.name
            
#             }, status=201)
    



# class AuthorOne(View):
#     """Gets one author from the database based on the id"""
#     def get(self, request, author_id):
#         author = Author.objects.get(pk=author_id)
#         return JsonResponse({
#             'id': author.id,
#             'name': author.name
#         })
    
#     def patch(self, request, author_id):
#         """Updates a publisher in the database"""
#         author = Author.objects.get(pk=author_id)
#         author.name = json.loads(request.body)['name']
#         author.save()

#         return JsonResponse({
#             'id': author.id,
#             "name": author.name
#         })

#     def delete(self, request, author_id):
#         """Deletes a particular publisher from the db"""
#         Author.objects.get(pk=author_id).delete()
#         return JsonResponse({}, status=204)


class BookList(View):
    def get(self, request):
        """Endpoint to get all the books in the database.
        or books associated with a particular author, 
        publisher or a specified date."""
        result = []
        #get the author id
        author_id = request.GET.get('author_id')
        #get the book by a particular author by his name
        author_name = request.GET.get('author_name')
        #get books by a particular publisher via their id
        publisher_id = request.GET.get('publisher_id')
        #get books by a particular publisher via their name
        publisher_name = request.GET.get('publisher_name')
        #get books published before a certain date
        published_before = request.GET.get('published_before')
        #get books published after a certain date
        published_after = request.GET.get('published_after')
        #Sorting of the API
        sort_by = request.GET.get('sort_by') or 'id'
        sort_by_direction = request.GET.get('sort_by_direction') or 'asc'

        sort_prefix = ''
        


        book_query = Book.objects


        if author_id:
            book_query = book_query.filter(Author__id=author_id)
        
        if author_name:
            book_query = book_query.filter(Author__name = author_name)
        
        if publisher_id:
            book_query = book_query.filter(Publisher__id=publisher_id)

        if publisher_name:
            book_query = book_query.filter(Publisher__name=publisher_name)
        #datetime.strptime converts a string to date object for python, while the other end specifies the format
        #https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
        if published_before:
            book_query = book_query.filter(published_date__lt= datetime.strptime(published_before, '%Y-%m-%d'))
        
        if published_after:
            book_query = book_query.filter(published_date__gt=datetime.strptime(published_after, '%Y-%m-%d'))
        
        if sort_by_direction == 'dsc':
            sort_prefix = '-'
        
        #Pagination is done with limit and offset
        limit = int(request.GET.get('limit') or 10)
        offset = int(request.GET.get('offset')or 0)

        book_query = book_query.order_by(sort_prefix+sort_by)
        
        #using 
        book_query = book_query[offset:limit+offset]
        
        for book in book_query.all():
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
    """Get's a particular book from the database
    using the book id."""
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
        


