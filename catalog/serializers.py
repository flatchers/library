from rest_framework import serializers

from catalog.models import Book, Borrowing, Payment


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover", "inventory", "daily_fee")


class BookWithIdAndNameSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return "id: %s (%s)" % (value.id, value.title)


class UserWithIdAndNameSerializer(serializers.RelatedField):
    def to_representation(self, value):
        status = "Active" if value.is_active else "Offline"
        return f"id: {value.id} ({value.email}) {status}"


# class UserFullInformationSerializer(serializers.RelatedField):
#     def to_representation(self, value):
#         return "%s" % (value.email)


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
            "user",
        )


class BorrowingListSerializer(BorrowingSerializer):
    book = BookWithIdAndNameSerializer(read_only=True)
    user = UserWithIdAndNameSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return",
            "actual_return",
            "book",
            "user",
        )


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer()
    user = UserWithIdAndNameSerializer(read_only=True)
    payments = PaymentSerializer(read_only=True, many=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return",
            "actual_return",
            "book",
            "user",
            "payments",
        )
