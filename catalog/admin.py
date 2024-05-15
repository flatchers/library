from django.contrib import admin

from catalog.models import Book, Borrowing, Payment
from user.models import User


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "cover", "inventory", "daily_fee", ]
    list_filter = ["title", "author", ]
    search_fields = ["title", ]


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ["borrow_date", "expected_return", "actual_return"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["status", "type", "session_url", "session_id", ]


admin.site.register(User)
