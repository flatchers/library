from django.contrib import admin

from catalog.models import Book, Borrowing, Payment


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "cover", "inventory", "daily_fee"]
    list_filter = ["title", "author"]
    search_fields = ["title", ]


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ["borrow_date", "expected_return", "actual_return"]


admin.site.register(Payment)
