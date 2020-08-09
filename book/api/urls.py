from django.urls import path
from . import views

urlpatterns = [
    
    path('publishers/', views.PublisherList.as_view() ),
    path('publishers/<int:publisher_id>/', views.PublisherOne.as_view()),
    path('authors/', views.AuthorList.as_view() ),
    path('authors/<int:author_id>/', views.AuthorOne.as_view()),
    path('books/', views.BookList.as_view() ),
    path('books/<int:book_id>/', views.BookOne.as_view()),
]
