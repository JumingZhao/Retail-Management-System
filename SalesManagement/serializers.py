from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from .models import SalesRecord
from PeopleManagement.models import User
from InventoryManagement.models import Product
from InventoryManagement.models import Store
from django.contrib.auth import get_user_model


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'sell_price','unit',)
        read_only_fields = ('id',)


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name',)


class SalesRecordSerializer(WritableNestedModelSerializer):
    product = ProductSerializer()
    salesPerson = UserSerializer()
    store = StoreSerializer()

    class Meta:
        model = SalesRecord
        fields = ('id', 'product', "quantity", "store", "totalPrice", "salesPerson", "date",)
        read_only_fields = ('salesPerson', 'store', 'product')


