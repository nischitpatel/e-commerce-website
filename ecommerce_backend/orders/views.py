from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import CartItem
from store.models import Product


class OrderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # GET /api/orders/ → list user orders
    def list(self, request):
        orders = Order.objects.filter(user=request.user).prefetch_related("items__product")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    # GET /api/orders/<id>/ → order detail
    def retrieve(self, request, pk=None):
        try:
            order = Order.objects.prefetch_related("items__product").get(id=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        serializer = OrderSerializer(order)
        return Response(serializer.data)

    # POST /api/orders/ → create order from cart
    @transaction.atomic
    def create(self, request):
        user = request.user
        cart_items = CartItem.objects.select_related("product").filter(user=user)

        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        total_price = 0
        order_items_data = []

        # Lock all product rows to prevent race conditions
        product_ids = [item.product.id for item in cart_items]
        products = Product.objects.select_for_update().filter(id__in=product_ids)
        product_map = {p.id: p for p in products}

        # Validate stock and calculate total price
        for item in cart_items:
            product = product_map[item.product.id]
            if item.quantity > product.stock:
                return Response(
                    {"error": f"Not enough stock for {product.name}. Requested {item.quantity}, available {product.stock}"},
                    status=400,
                )
            total_price += product.price * item.quantity
            order_items_data.append({
                "product": product,
                "quantity": item.quantity,
                "price": product.price
            })

        # Create order
        order = Order.objects.create(user=user, total_price=total_price)

        # Create OrderItems and deduct stock
        for data in order_items_data:
            OrderItem.objects.create(
                order=order,
                product=data["product"],
                quantity=data["quantity"],
                price=data["price"]
            )
            # Deduct stock
            data["product"].stock -= data["quantity"]
            data["product"].save()

        # Clear user's cart
        cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
