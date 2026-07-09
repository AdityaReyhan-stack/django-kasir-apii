from django.contrib import admin
from .models import Product, Transaction, TransactionItem

admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(TransactionItem)