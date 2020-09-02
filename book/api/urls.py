from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from . import views

router = routers.SimpleRouter()

router.register('publishers', views.PublisherListView)
router.register('authors', views.AuthorListView)
router.register('books', views.BookListView)

urlpatterns = [
    
    # path('publishers/', views.PublisherList.as_view() ),
    # path('publishers/<int:publisher_id>/', views.PublisherOne.as_view()),
    # path('authors/', views.AuthorList.as_view() ),
    # path('authors/<int:author_id>/', views.AuthorOne.as_view()),
    # path('books/', views.BookList.as_view() ),
    # path('books/<int:book_id>/', views.BookOne.as_view()),
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
