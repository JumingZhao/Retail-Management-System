from django.db import models
from InventoryManagement.models import Product
from InventoryManagement.models import Supplier
from InventoryManagement.models import Store
from InventoryManagement.models import SupplierPrice
from PeopleManagement.models import User


class SalesRecord(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    totalPrice = models.FloatField()
    salesPerson = models.ForeignKey(User, on_delete=models.PROTECT)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    date = models.DateField(db_index=True)

    def __str__(self):
        return self.name
