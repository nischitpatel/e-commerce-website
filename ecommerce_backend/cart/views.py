from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import CartItem
from .serializers import CartItemSerializer
from store.models import Product

class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # GET /cart/ → List all cart items for logged-in user
    def list(self, request):
        items = CartItem.objects.filter(user=request.user).select_related("product")
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)

    # POST /cart/add/
    @transaction.atomic
    def create(self, request):
        user = request.user
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)
        
        if quantity == 0:
            return Response(
                {"error": f"Quantity should be atleast 1"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if product.stock < quantity:
            return Response(
                {"error": f"Only {product.stock} in stock"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if product already exists in cart
        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            product=product,
            defaults={"quantity": quantity}
        )

        if not created:
            # Update quantity but check stock
            if product.stock < cart_item.quantity + quantity:
                return Response(
                    {"error": f"Not enough stock. Only {product.stock} left."},
                    status=400,
                )
            cart_item.quantity += quantity
            cart_item.save()

        return Response(
            CartItemSerializer(cart_item).data,
            status=status.HTTP_201_CREATED
        )

    # PATCH /cart/update/<id>/
    @transaction.atomic
    def partial_update(self, request, pk=None):
        try:
            cart_item = CartItem.objects.get(id=pk, user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=404)

        new_qty = int(request.data.get("quantity"))

        if cart_item.product.stock < new_qty:
            return Response(
                {"error": f"Only {cart_item.product.stock} available"},
                status=400,
            )

        cart_item.quantity = new_qty
        cart_item.save()

        return Response(CartItemSerializer(cart_item).data)

    # DELETE /cart/remove/<id>/
    def destroy(self, request, pk=None):
        try:
            cart_item = CartItem.objects.get(id=pk, user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=404)

        cart_item.delete()
        return Response({"message": "Item removed from cart"})

    # DELETE /cart/clear/
    def clear(self, request):
        CartItem.objects.filter(user=request.user).delete()
        return Response({"message": "Cart cleared successfully"})
