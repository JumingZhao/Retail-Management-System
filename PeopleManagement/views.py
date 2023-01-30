from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from InventoryManagement.models import Product, Store
from PeopleManagement.models import User, SalesManager
from PeopleManagement.serializer import UserSerializer, UserAdminSerializer
from SalesManagement.models import SalesRecord
from SalesManagement.serializers import SalesRecordSerializer


@api_view(['GET'])
def all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST', 'PUT'])
def user_admin(request):
    if request.method == 'GET':
        users = User.objects.all()
        if request.GET.get('id') is not None:
            users = users.filter(id=request.GET.get('id'))
        serializer = UserAdminSerializer(users, many=True)
        return Response(serializer.data)
    elif request.method == 'PUT':
        user = User()
        record = request.data
        user.name = record['name']
        user.username = record['username']
        user.password = record['password']
        user.role = record['role']
        user.save()
        print(user.id)
        if record['role'] == 'store_manager':
            sales_manager = SalesManager()
            store = Store.objects.get(name=record['store'])
            sales_manager.store = store
            sales_manager.user_id = user.id
            if record['isGolden']:
                sales_manager.isGolden = 1
            else:
                sales_manager.isGolden = 0
            sales_manager.save()
        return Response(status=status.HTTP_200_OK)
    else:
        record = request.data
        user = User.objects.get(id=record['id'])
        user.name = record['name']
        user.username = record['username']
        user.password = record['password']
        user.role = record['role']
        user.save()
        print(user.id)
        try:
            sales_manager = SalesManager.objects.get(user__id=record['id'])
        except SalesManager.DoesNotExist:
            sales_manager = None
        if sales_manager is not None and record['role'] != 'store_manager':
            sales_manager.delete()
        if record['role'] == 'store_manager':
            if sales_manager is None:
                sales_manager = SalesManager()
            sales_manager.user = user
            store = Store.objects.get(name=record['store'])
            sales_manager.store = store
            sales_manager.user_id = user.id
            if record['isGolden']:
                sales_manager.isGolden = 1
            else:
                sales_manager.isGolden = 0
            sales_manager.save()

        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def remove_user(request):
    record = request.data
    print(request.data)
    try:
        sales_manager = SalesManager.objects.get(user__id=record['id'])
    except SalesManager.DoesNotExist:
        sales_manager = None
    if sales_manager is not None:
        sales_manager.delete()
    user = User.objects.get(id=record['id'])
    user.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def login(request):
    record = request.data
    user = User.objects.filter(username=record['username']).filter(password=record['password']).first()
    if user is None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    else:
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)


