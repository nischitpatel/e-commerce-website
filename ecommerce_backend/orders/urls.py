from django.urls import path
from .views import OrderViewSet

order_list = OrderViewSet.as_view({"get": "list", "post": "create"})
order_detail = OrderViewSet.as_view({"get": "retrieve"})
order_create = OrderViewSet.as_view({"post": "create"})
order_capture = OrderViewSet.as_view({"post": "capture"})

urlpatterns = [
    path("", order_list, name="order-list"),
    path("<int:pk>/", order_detail, name="order-detail"),
    path("create/", order_create, name="order-create"),
    path("<int:pk>/capture/", order_capture, name="order-capture"),
]
