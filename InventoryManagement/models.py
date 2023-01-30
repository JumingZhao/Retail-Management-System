from django.db import models

# Create your models here.


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    sell_price = models.FloatField()
    name = models.CharField(max_length=50,db_index=True)
    category = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Store(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class SupplierPrice(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT,db_index=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT,db_index=True)
    price = models.FloatField()

    def __str__(self):
        return self.name


class PurchaseRecord(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT,db_index=True)
    quantity = models.IntegerField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    totalPrice = models.FloatField()
    deliveryDate = models.DateField()
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class WarehouseInventory(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)


class StoreInventory(models.Model):
    id = models.AutoField(primary_key=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
