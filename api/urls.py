from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterUser.as_view()),
    path('login/', LoginUser.as_view()),
    path('books/add/', AddBook.as_view()),
    path('books/', ViewBooks.as_view()),
    path('books/update/<int:pk>/', UpdateBook.as_view()),
    path('books/delete/<int:pk>/', DeleteBook.as_view()),
    path('books/issue/', IssueBook.as_view()),
    path('books/return/<int:pk>/', ReturnBook.as_view()),
]
