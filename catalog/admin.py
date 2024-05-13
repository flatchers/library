from django.contrib import admin

from catalog.models import Book, Borrowing, Payment


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "cover", "inventory", "daily_fee"]
    list_filter = ["title", "author"]
    search_fields = ["title", ]


admin.site.register(Borrowing)
admin.site.register(Payment)
