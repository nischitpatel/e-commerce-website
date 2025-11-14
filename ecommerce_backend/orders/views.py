# from rest_framework import viewsets, permissions
# from .models import Order
# from .serializers import OrderSerializer

# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         # Auto-assign logged-in user when order is created
#         serializer.save(user=self.request.user)

#     def get_queryset(self):
#         # Users see only their own orders
#         user = self.request.user
#         if user.is_staff:
#             return Order.objects.all()
#         return Order.objects.filter(user=user)
    
# orders/views.py

from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer
from store.models import Product
from rest_framework.exceptions import ValidationError

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        # Calculate total price 
        total_price = product.price * quantity

        # Save with correct total_price & logged-in user
        serializer.save(user=self.request.user, total_price=total_price)

    def perform_update(self, serializer):
        product = serializer.validated_data.get('product', serializer.instance.product)
        quantity = serializer.validated_data.get('quantity', serializer.instance.quantity)

        total_price = product.price * quantity

        serializer.save(total_price=total_price)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

