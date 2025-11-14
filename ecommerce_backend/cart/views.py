# cart/views.py

import time
from functools import wraps

from django.db import transaction, DatabaseError, OperationalError
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import CartItem
from .serializers import CartItemSerializer
from store.models import Product

# Simple retry decorator for transient DB lock errors
def retry_on_lock(max_retries=3, delay=0.1, backoff=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            current_delay = delay
            while True:
                try:
                    return func(*args, **kwargs)
                except (OperationalError, DatabaseError) as e:
                    # You may want to narrow this to specific lock/timeouts depending on DB driver
                    if retries >= max_retries:
                        raise
                    time.sleep(current_delay)
                    retries += 1
                    current_delay *= backoff
        return wrapper
    return decorator


class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        items = CartItem.objects.filter(user=request.user).select_related("product")
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)

    @retry_on_lock(max_retries=4, delay=0.05)
    @transaction.atomic
    def create(self, request):
        """
        POST /api/cart/add/
        Uses select_for_update to lock the product row while checking/updating cart quantities.
        """
        user = request.user
        product_id = request.data.get("product_id")
        try:
            quantity = int(request.data.get("quantity", 1))
            if quantity <= 0:
                return Response({"error": "Quantity must be >= 1"}, status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, TypeError):
            return Response({"error": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Lock the product row for this transaction
            product = Product.objects.select_for_update().get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check existing cart item (inside same transaction to avoid race)
        cart_item = CartItem.objects.select_for_update().filter(user=user, product=product).first()

        current_qty = cart_item.quantity if cart_item else 0
        requested_total_qty = current_qty + quantity

        if requested_total_qty > product.stock:
            return Response(
                {"error": f"Not enough stock. Requested {requested_total_qty}, only {product.stock} available."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if cart_item:
            cart_item.quantity = requested_total_qty
            cart_item.save()
            created = False
        else:
            cart_item = CartItem.objects.create(user=user, product=product, quantity=quantity)
            created = True

        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(CartItemSerializer(cart_item).data, status=status_code)

    @retry_on_lock(max_retries=4, delay=0.05)
    @transaction.atomic
    def partial_update(self, request, pk=None):
        """
        PATCH /api/cart/update/<id>/
        Locks the product row and the cart row to safely update quantity.
        """
        try:
            cart_item = CartItem.objects.select_for_update().get(id=pk, user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            new_qty = int(request.data.get("quantity"))
            if new_qty <= 0:
                return Response({"error": "Quantity must be >= 1"}, status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, TypeError):
            return Response({"error": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)

        # Lock product - select_for_update on product ensures no concurrent change to stock
        product = Product.objects.select_for_update().get(id=cart_item.product_id)

        if new_qty > product.stock:
            return Response(
                {"error": f"Only {product.stock} available, cannot set quantity to {new_qty}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_item.quantity = new_qty
        cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_200_OK)

    @transaction.atomic
    def destroy(self, request, pk=None):
        try:
            cart_item = CartItem.objects.get(id=pk, user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response({"message": "Item removed from cart"}, status=status.HTTP_200_OK)

    @transaction.atomic
    def clear(self, request):
        CartItem.objects.filter(user=request.user).delete()
        return Response({"message": "Cart cleared successfully"}, status=status.HTTP_200_OK)
