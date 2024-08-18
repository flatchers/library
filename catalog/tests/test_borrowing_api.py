from django.test import TestCase

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from catalog.models import Borrowing, Book
from catalog.serializers import BorrowingListSerializer, BorrowingDetailSerializer


BORROWING_URL = reverse("library:borrowing-list")


def borrowing_url(borrowing_id):
    return reverse("library:borrowing-detail", args=[borrowing_id])


class UnauthenticatedBorrowingApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BORROWING_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="tester_user@test.user", password="123465"
        )
        self.client.force_authenticate(self.user)
        self.book = Book.objects.create(
            title="test", author="test testerson", inventory=10, daily_fee=10.05
        )

    def test_borrowing_list(self):
        res = self.client.get(BORROWING_URL)

        borrowings = Borrowing.objects.all()
        serializer = BorrowingListSerializer(borrowings, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_borrowing_detail(self):
        borrowing = Borrowing.objects.create(
            expected_return="2024-07-12", book=self.book, user_id=self.user
        )
        url = borrowing_url(borrowing.id)
        res = self.client.get(url)
        serializer = BorrowingDetailSerializer(borrowing)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
