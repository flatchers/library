from rest_framework import routers

from catalog.views import BookViewSet, BorrowingViewSet, PaymentViewSet

router = routers.DefaultRouter()
router.register("books", BookViewSet)
router.register("borrowings", BorrowingViewSet)
router.register("payments", PaymentViewSet)

urlpatterns = router.urls

app_name = "library"
