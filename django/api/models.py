from django.db import models
import string
import random


def generateUniqueCode():
    length = 10

    while True:
        code = "".join(random.choices(string.ascii_uppercase, k=length))
        if User.objects.filter(code=code).count() == 0:
            break
    return code

# Create your models here.


class User(models.Model):
    code = models.CharField(max_length=10, default=generateUniqueCode, unique=True)
    host = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
