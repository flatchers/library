from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from catalog.models import Book, Borrowing, Payment
from catalog.permissions import IsAdminOrReadOnly
from catalog.serializers import (
    BookSerializer,
    BorrowingSerializer,
    PaymentSerializer,
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

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the movies with filters"""
        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        queryset = self.queryset

        if user_id:
            user_id_ids = self._params_to_ints(user_id)
            queryset = queryset.filter(user_id__id__in=user_id_ids)

        if is_active:
            queryset = queryset.filter(user_id__is_active=is_active)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        else:
            return BorrowingSerializer

    def perform_create(self, serializer):
        book_id = self.request.data.get("book_id")
        borrowing_ar = self.request.data.get("actual_return")

        if book_id and not borrowing_ar:
            book = Book.objects.get(pk=book_id)
            book.inventory -= 1
            book.save()
        return serializer.save()

    def perform_update(self, serializer):
        book_id = self.request.data.get("book_id")
        borrowing_ar = self.request.data.get("actual_return")
        if borrowing_ar:
            book = Book.objects.get(pk=book_id)
            book.inventory += 1
            book.save()
        return serializer.save()


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
