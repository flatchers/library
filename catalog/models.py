from django.contrib.auth.models import User
from django.db import models

from library import settings


class Book(models.Model):
    class Cover(models.TextChoices):
        HARD = "HARD"
        SOFT = "SOFT"
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=255, choices=Cover.choices)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=None, decimal_places=2)


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now=True)
    expected_return = models.DateField()
    actual_return = models.DateField()
    book_id = models.ManyToManyField(Book)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
