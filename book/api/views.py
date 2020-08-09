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
    pass



class AuthorOne(View):
    pass



class BookList(View):
    pass



class BookOne(View):
    pass
