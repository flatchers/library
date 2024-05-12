from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from catalog.models import Book
from catalog.permissions import IsAdminOrReadOnly
from catalog.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly, )
