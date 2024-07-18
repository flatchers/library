from unittest import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from catalog.models import Book
from catalog.serializers import BookSerializer


BOOK_URL = reverse("library:book-list")


class BookTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_book_list(self):
        resp = self.client.get(BOOK_URL)

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        print("Response: ", resp)
        print("response status code: ", resp.status_code)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, resp.data)
