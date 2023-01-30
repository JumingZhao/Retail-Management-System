from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from .models import Warehouse, WarehouseInventory, StoreInventory, PurchaseRecord, Supplier, SupplierPrice
from PeopleManagement.models import User
from InventoryManagement.models import Product
from InventoryManagement.models import Store
from django.contrib.auth import get_user_model


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'
        read_only_fields = ('id',)


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ('id',)


class WarehouseInventorySerializer(WritableNestedModelSerializer):
    product = ProductSerializer()
    warehouse = WarehouseSerializer()

    class Meta:
        model = WarehouseInventory
        fields = ('id', 'warehouse', 'product', 'quantity')
        read_only_fields = ('id',)


class StoreInventorySerializer(WritableNestedModelSerializer):
    warehouseinventory = serializers.SerializerMethodField()
    store = StoreSerializer()

    def get_warehouseinventory(self, obj):
        store_inventory = obj
        warehouse_inventory = WarehouseInventory.objects.filter(warehouse__id=store_inventory.warehouse.id)
        if warehouse_inventory:
            return WarehouseInventorySerializer(warehouse_inventory, many=True).data
        else:
            return None

    class Meta:
        model = StoreInventory
        fields = ('id', 'store', 'warehouseinventory')
        read_only_fields = ('id',)


class PurchaseRecordSerializer(WritableNestedModelSerializer):
    product = ProductSerializer()
    warehouse = WarehouseSerializer()
    supplier = SupplierSerializer()

    class Meta:
        model = PurchaseRecord
        fields = ('id', 'product', 'warehouse', 'quantity', 'totalPrice', 'supplier', 'deliveryDate')
        read_only_fields = ('id', 'product', 'warehouse', 'supplier')


class SupplierPriceSerializer(WritableNestedModelSerializer):
    product = ProductSerializer()
    supplier = SupplierSerializer()

    class Meta:
        model = SupplierPrice
        fields = '__all__'
        read_only_fields = ('id',)


class ProductAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('id',)
