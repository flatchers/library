from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from catalog.models import Book
from catalog.serializers import BookSerializer


BOOK_URL = reverse("library:book-list")


def sample_book(**params):
    defaults = {
        "title": "The Great Gatsby",
        "author": "Francis Scott Key Fitzgerald",
        "inventory": 10,
        "daily_fee": 10.05
    }
    defaults.update(params)
    return Book.objects.create(**defaults)


def detail_url(book_id):
    return reverse("library:book-detail", args=(book_id,))


class BookTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_book_list(self):

        resp = self.client.get(BOOK_URL)

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)

    def test_book_detail(self):
        book = sample_book()
        res = self.client.get(detail_url(book.id))

        serializer = BookSerializer(book)
        print("RESPONSE: ", detail_url(book.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class BookCreateAuthorizedTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="jackfranco@user.user", password="123465"
        )
        self.client.force_authenticate(self.user)

    def test_book_create_forbidden(self):
        payload = {
            "title": "new test",
            "author": "Jonathan Adkins",
            "inventory": 12,
            "daily_fee": 12.05
        }
        response = self.client.post(BOOK_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            password="123465",
            email="test@admin.user",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_book_create_for_admin(self):
        payload = {
            "title": "new else",
            "author": "Jonathan Adkins",
            "cover": "HARD",
            "inventory": 12,
            "daily_fee": 12.05
        }

        res = self.client.post(BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(payload["title"], "new else")
        self.assertEqual(payload["author"], "Jonathan Adkins")
        self.assertEqual(payload["cover"], "HARD")
        self.assertEqual(payload["inventory"], 12)
        self.assertEqual(payload["daily_fee"], 12.05)

    def test_book_delete_available(self):
        info = sample_book()

        res = self.client.delete(detail_url(info.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
