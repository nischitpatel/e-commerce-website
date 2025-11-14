from django.urls import path
from .views import OrderViewSet

order_list = OrderViewSet.as_view({"get": "list", "post": "create"})
order_detail = OrderViewSet.as_view({"get": "retrieve"})

urlpatterns = [
    path("", order_list, name="order-list"),
    path("<int:pk>/", order_detail, name="order-detail"),
]
