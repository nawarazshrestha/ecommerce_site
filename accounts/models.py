from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=30, blank=True)
    phone = models.BigIntegerField(null=True)


