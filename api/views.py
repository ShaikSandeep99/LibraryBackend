from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Book, Issue
from .serializers import UserSerializer, BookSerializer, IssueSerializer
from django.contrib.auth.hashers import make_password, check_password

# ------------------- USER -------------------
class RegisterUser(APIView):
    def post(self, request):
        data = request.data
        data['password'] = make_password(data['password'])  # hash password
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                return Response({'msg': 'Login successful'})
            else:
                return Response({'msg': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# ------------------- BOOK -------------------
class AddBook(APIView):
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Book added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewBooks(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class UpdateBook(APIView):
    def put(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
        except Book.DoesNotExist:
            return Response({'msg': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Book updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteBook(APIView):
    def delete(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
            book.delete()
            return Response({'msg': 'Book deleted successfully'})
        except Book.DoesNotExist:
            return Response({'msg': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)


# ------------------- ISSUE / RETURN -------------------
class IssueBook(APIView):
    def post(self, request):
        user_id = request.data.get('user')
        book_id = request.data.get('book')
        try:
            user = User.objects.get(id=user_id)
            book = Book.objects.get(id=book_id)
            if book.is_issued:
                return Response({'msg': 'Book already issued'}, status=status.HTTP_400_BAD_REQUEST)
            book.is_issued = True
            book.save()
            issue = Issue.objects.create(user=user, book=book)
            serializer = IssueSerializer(issue)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Book.DoesNotExist:
            return Response({'msg': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)


class ReturnBook(APIView):
    def post(self, request, pk):
        try:
            issue = Issue.objects.get(id=pk)
            issue.book.is_issued = False
            issue.book.save()
            issue.return_date = request.data.get('return_date')  # accept return date
            issue.save()
            return Response({'msg': 'Book returned successfully'})
        except Issue.DoesNotExist:
            return Response({'msg': 'Issue record not found'}, status=status.HTTP_404_NOT_FOUND)
