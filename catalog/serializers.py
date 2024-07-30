from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from catalog.models import Book, Borrowing, Payment
from user.serializers import UserSerializer


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover", "inventory", "daily_fee")


class BookWithIdAndNameSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return "id: %s (%s)" % (value.id, value.title)


class UserWithIdAndNameSerializer(serializers.RelatedField):
    def to_representation(self, value):
        if not value.is_active:
            return "id: %s (%s) Offline" % (value.id, value.username)
        if value.is_active:
            return "id: %s (%s) Active" % (value.id, value.username)


class UserFullInformationSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return "%s, %s" % (value.username, value.email)


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = (
            "status",
            "session_url",
            "session_id",
            "money_to_pay",
        )


class BorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return",
            "actual_return",
            "book",
            "user_id"
        )


class BorrowingListSerializer(BorrowingSerializer):
    book = BookWithIdAndNameSerializer(read_only=True)
    user_id = UserWithIdAndNameSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return",
            "actual_return",
            "book",
            "user_id",
        )


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer()
    user_id = UserFullInformationSerializer(read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return",
            "actual_return",
            "book",
            "user_id",
            "payments"
        )
