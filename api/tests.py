from django.test import TestCase
from .models import Product

class ProductTest(TestCase):

    def test_create_product(self):
        product = Product.objects.create(
            name="Teh Botol",
            price=5000,
            stock=20
        )

        self.assertEqual(product.name, "Teh Botol")
        self.assertEqual(product.stock, 20)