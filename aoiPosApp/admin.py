from django.contrib import admin
from aoiPosApp.models import Product, Transaction, TransactionItem, User

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(TransactionItem)