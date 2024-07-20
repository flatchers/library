from unittest import TestCase

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
