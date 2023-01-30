from django.db import models

# Create your models here.
from InventoryManagement.models import Store


class User(models.Model):
    role_choice = (
        (99, "super user"),  # all
        (50, "warehouse admin"),  # all to wh related
        (30, "sales person"),  # akk ti sales related
        (10, "store manager"),  # query to all
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class SalesManager(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    isGolden = models.BooleanField()
    store = models.ForeignKey(Store, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
