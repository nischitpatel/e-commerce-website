from rest_framework import serializers
from .models import CartItem
# from store.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")
    product_price = serializers.ReadOnlyField(source="product.price")
    stock = serializers.ReadOnlyField(source="product.stock")

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_price",
            "stock",
            "quantity",
            "added_at",
        ]

    def validate(self, data):
        product = data.get("product")
        quantity = data.get("quantity")

        if product.stock < quantity:
            raise serializers.ValidationError(
                {"stock": f"Only {product.stock} items left in stock."}
            )
        return data
