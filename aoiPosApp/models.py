from django.db import models

# Create your models here.
class User (models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)


class Product (models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    image_path = models.ImageField(
        upload_to='images/products/',
        blank=True,
        null=True,
    )


class Transaction (models.Model):
    id = models.BigAutoField(primary_key=True)
    unique_id = models.CharField(max_length=100)
    status = models.BooleanField()
    created_at = models.DateTimeField()
    user = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
    )