from django.urls import path
from .views import CartViewSet

cart_list = CartViewSet.as_view({"get": "list", "post": "create"})
cart_update = CartViewSet.as_view({"patch": "partial_update"})
cart_delete = CartViewSet.as_view({"delete": "destroy"})
cart_clear = CartViewSet.as_view({"delete": "clear"})

urlpatterns = [
    path("", cart_list, name="cart-list"),
    path("add/", cart_list, name="cart-add"),
    path("update/<int:pk>/", cart_update, name="cart-update"),
    path("remove/<int:pk>/", cart_delete, name="cart-remove"),
    path("clear/", cart_clear, name="cart-clear"),
]
