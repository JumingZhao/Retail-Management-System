from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from InventoryManagement.models import Store
from PeopleManagement.models import User, SalesManager


class UserSerializer(WritableNestedModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name', 'role', 'username', )
        read_only_fields = ('id',)


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ('id',)


class SalesManagerSerializer(serializers.ModelSerializer):
    store = StoreSerializer()

    class Meta:
        model = SalesManager
        fields = '__all__'
        read_only_fields = ('id',)


class UserAdminSerializer(WritableNestedModelSerializer):
    salesmanager = serializers.SerializerMethodField()

    def get_salesmanager(self, obj):
        user = obj
        try:
            sales_manager = SalesManager.objects.get(user__id=user.id)
        except SalesManager.DoesNotExist:
            sales_manager = None
        if sales_manager is not None:
            return SalesManagerSerializer(sales_manager, many=False).data
        else:
            return None

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id',)
