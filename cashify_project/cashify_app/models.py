from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Device(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.name} - {self.condition}"

class Transaction(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='transactions_bought')
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='transactions_sold')
    status = models.CharField(max_length=50, default='Pending')
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction for {self.device} - Status: {self.status}"
