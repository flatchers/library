from django_q.tasks import async_task
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from .telegram_bot import notify_borrowing_created, notify_borrowing_overdue


from catalog.models import Book, Borrowing
from catalog.permissions import IsAdminOrReadOnly
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
    queryset = Borrowing.objects.select_related("book", "user").all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def _params_to_ints(query_string):
        return [int(str_id) for str_id in query_string.split(",")]

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        return BorrowingSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(user=self.request.user)
        book = self.request.query_params.get("book")
        if book:
            book = self._params_to_ints(book)
            queryset = queryset.filter(book__id__in=book, user__is_active=True)

        return queryset.distinct()

    @extend_schema(
        # extra parameters added to the schema
        parameters=[
            OpenApiParameter(
                "book",
                type={"type": "array", "items": {"type": "number"}},
                description="Filter by book id (ex. ?book=1,2)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get list of book"""
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        borrowing = serializer.save()
        if not borrowing.actual_return:
            borrowing.book.inventory -= 1
            borrowing.book.save()
            async_task(notify_borrowing_created, borrowing.id)

    def perform_update(self, serializer):
        borrowing = serializer.save()
        if borrowing.actual_return:
            borrowing.book.inventory += 1
            borrowing.book.save()
            async_task(notify_borrowing_overdue, borrowing.id)
