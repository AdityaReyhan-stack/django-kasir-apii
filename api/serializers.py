from rest_framework import serializers
from .models import Product, Transaction, TransactionItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class TransactionItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = TransactionItem
        fields = ["product", "quantity"]


class TransactionSerializer(serializers.ModelSerializer):
    items = TransactionItemSerializer(many=True)

    class Meta:
        model = Transaction
        fields = ["id", "user", "date", "total_price", "items"]
        read_only_fields = ["date", "total_price"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")

        transaction = Transaction.objects.create(**validated_data)

        total = 0

        for item in items_data:
            product = item["product"]
            qty = item["quantity"]

            if product.stock < qty:
                raise serializers.ValidationError(
                    f"Stok {product.name} tidak cukup!"
                )

            product.stock -= qty
            product.save()

            subtotal = product.price * qty
            total += subtotal

            TransactionItem.objects.create(
                transaction=transaction,
                product=product,
                quantity=qty,
                price=product.price
            )

        transaction.total_price = total
        transaction.save()

        return transaction