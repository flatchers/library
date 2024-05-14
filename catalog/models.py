import uuid

from django.contrib.auth.models import User
from django.db import models

from library import settings


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "HARD"
        SOFT = "SOFT"
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=255, choices=CoverChoices.choices)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.title}"


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now=True)
    expected_return = models.DateField()
    actual_return = models.DateField(blank=True, null=True)
    book_id = models.ManyToManyField(Book)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Payment(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING"
        PAID = "PAID"

    class Type(models.TextChoices):
        PAYMENT = "PAYMENT"
        FINE = "FINE"
    status = models.CharField(max_length=255, choices=Status.choices)
    type = models.CharField(max_length=255, choices=Type.choices)
    borrowing_id = models.ForeignKey(Borrowing, related_name="payments", on_delete=models.CASCADE)
    session_url = models.URLField(max_length=200)

    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    money_to_pay = models.ManyToManyField(Borrowing)
