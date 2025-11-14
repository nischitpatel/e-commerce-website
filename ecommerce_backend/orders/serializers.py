from rest_framework import serializers
from .models import Order
from store.models import Product

class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = Order
        fields = ['id', 'user', 'product_name', 'product_id', 'quantity', 'total_price', 'status', 'ordered_at']
        read_only_fields = ['user', 'ordered_at', 'total_price']
