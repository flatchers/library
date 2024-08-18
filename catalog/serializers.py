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


class UserFullInformationSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return "%s" % (value.email)


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
            "user_id",
        )

    def validate(self, attrs):
        if attrs["book"].inventory < 0:
            raise serializers.ValidationError(
                {"inventory": "there are no books left in the library"}
            )
        if self.instance and self.instance.actual_return:
            raise serializers.ValidationError({"actual_return": "Borrowing is closed"})
        return attrs


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
            "payments",
        )
