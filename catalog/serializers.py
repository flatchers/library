from rest_framework import serializers

from catalog.models import Book, Borrowing, Payment


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover", "inventory", "daily_fee")


class BorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date", "expected_return", "actual_return", "book_id", "user_id")


class BookWithIdAndNameSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return "id: %s (%s)" % (value.id, value.title)


class UserWithIdAndNameSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return "id: %s (%s)" % (value.id, value.username)


class BorrowingListSerializer(BorrowingSerializer):
    book_id = BookWithIdAndNameSerializer(many=True, read_only=True)
    user_id = UserWithIdAndNameSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date", "expected_return", "actual_return", "book_id", "user_id")


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("status", "type", "borrowing_id", "session_url", "session_id", "money_to_pay")
