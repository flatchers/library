from rest_framework import serializers

from catalog.models import Book, Borrowing, Payment


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("title", "author", "cover", "inventory", "daily_fee")


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date", "expected_return", "actual_return")


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("id", "status", "type", "borrowing_id", "session_url", "session_id", "money_to_pay")
