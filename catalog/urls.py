from rest_framework import routers

from catalog.views import BookViewSet, BorrowingViewSet

router = routers.DefaultRouter()
router.register("books", BookViewSet)
router.register("borrowings", BorrowingViewSet)

urlpatterns = router.urls

app_name = "library"
