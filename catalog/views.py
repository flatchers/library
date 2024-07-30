import os

from django.db import transaction
from django.utils import timezone
from django_q.tasks import async_task
from dotenv import load_dotenv
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .telegram_bot import notify_borrowing_created, notify_borrowing_overdue


from catalog.models import Book, Borrowing, Payment
from catalog.permissions import IsAdminOrReadOnly, IsAdminAndAuthenticatedOrReadOnly
from catalog.serializers import (
    BookSerializer,
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly,)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAdminAndAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        return BorrowingSerializer

    def perform_create(self, serializer):
        borrowing = serializer.save()
        borrowing.book.inventory -= 1
        borrowing.book.save()

    def perform_update(self, serializer):
        from datetime import date
        borrowing = serializer.save()
        if borrowing.expected_return_date < date.today():
            async_task(notify_borrowing_overdue, borrowing.id)
        if borrowing.actual_return_date:
            borrowing.book.inventory += 1
            borrowing.book.save()

