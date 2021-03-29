from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from posts.models import Post

# Create your models here.
User = get_user_model()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Post, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} of {self.item.title}'

    # Getting the total price

    def get_total(self):
        return self.item.price * self.quantity
        floattotal = float("{0:.2f}".format(total))
        return floattotal



class Order(models.Model):
    orderitems = models.ManyToManyField(Cart)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=200, blank=True, null=True)
    orderId = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += order_item.get_total()

        return total
