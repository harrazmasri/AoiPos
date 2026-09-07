from decimal import Decimal
import uuid

from django.db import models
from django.utils.crypto import get_random_string

def generate_transaction_id():
    return f"Transaction-{uuid.uuid4().hex[:8].upper()}"

# Create your models here.
class User (models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)


class Product (models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_path = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
    )


class Transaction (models.Model):
    @property
    def discount_rate(self):
        # e.g., 100 - 75 = 25
        return 100 - self.cut_price

    id = models.BigAutoField(primary_key=True)
    unique_id = models.CharField(
        max_length=100,
        default=generate_transaction_id,
        unique=True,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField()
    cut_price = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    user = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    effective_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )


class TransactionItem (models.Model):
    id = models.BigAutoField(primary_key=True)
    transaction = models.ForeignKey(
        Transaction,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.SET_NULL, 
        null=True
    )
    product_name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save (self, *args, **kwargs): # *args contain tuple of checkout items, *kwargs accept dict, * same as spread operator in js (...)
        self.subtotal = Decimal(str(self.unit_price)) * Decimal(str(self.quantity))
        super().save(*args, **kwargs)
