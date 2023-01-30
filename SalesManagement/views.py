import json
from datetime import datetime

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

# Create your views here.
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from InventoryManagement.models import Product, Store
from PeopleManagement.models import User, SalesManager
from SalesManagement.models import SalesRecord
from SalesManagement.serializers import SalesRecordSerializer



@api_view(['GET', 'POST', 'PUT'])
def salesrecord(request):

    if request.method == 'GET':

        salesrecord = SalesRecord.objects.all()
        if request.GET.get('start') is not None:
            start = parse_date(request.GET.get('start'))
            end = parse_date(request.GET.get('end'))
            salesrecord = salesrecord.filter(date__gte=start).filter(date__lte=end)
        if request.GET.get('user') is not None:
            salesrecord = salesrecord.filter(salesPerson__username=request.GET.get('user'))
        if request.GET.get('store') is not None:
            salesrecord = salesrecord.filter(store__name=request.GET.get('store'))

        paginator = PageNumberPagination()
        page_obj = paginator.paginate_queryset(salesrecord, request)
        serializer = SalesRecordSerializer(page_obj, many=True)
        return Response({
            'page_size': paginator.page_size,
            'total_count': paginator.page.paginator.count,
            'results': serializer.data})

    elif request.method == 'PUT':
        record = request.data[0]
        print(record)
        if record['quantity'] < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if record['totalPrice'] < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        salesrecord = SalesRecord()
        product = Product.objects.filter(name=record['product']).first()
        print(product)
        store = Store.objects.filter(name=record['store']).first()
        print(store)
        user = User.objects.filter(name=record['userId']).first()
        print(user)
        salesrecord.product = product
        salesrecord.store = store
        salesrecord.salesPerson = user
        salesrecord.date = record['date']
        salesrecord.quantity = record['quantity']
        salesrecord.totalPrice = record['totalPrice']
        salesrecord.save()

        return Response(status=status.HTTP_200_OK)

    else:
        record = request.data[0]
        print(record)
        if record['quantity'] < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if record['totalPrice'] < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        salesrecord = SalesRecord.objects.get(id=record['id'])
        product = Product.objects.filter(name=record['product']).first()
        print(product)
        store = Store.objects.filter(name=record['store']).first()
        print(store)
        user = User.objects.filter(name=record['userId']).first()
        print(user)
        salesrecord.product = product
        salesrecord.store = store
        salesrecord.salesPerson = user
        salesrecord.date = record['date']
        salesrecord.quantity = record['quantity']
        salesrecord.totalPrice = record['totalPrice']
        salesrecord.save()

        return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def delete_salesrecord(request):
    record = request.data
    print(record)
    salesrecord = SalesRecord.objects.get(id=record['id'])
    salesrecord.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def manager_sales(request):
    manager = SalesManager.objects.all()


@api_view(['GET'])
def sales_stats(request):
    sales_record = SalesRecord.objects.all().order_by('date')
    res = {}
    for record in sales_record:
        key = str(record.date.year) + '-' + str(record.date.month)
        value = res.get(key, 0)
        value += record.totalPrice
        res[key] = value
    return Response(json.dumps(res))

@api_view(['GET'])
def manager_monthly_sales(request):
    sales_record = SalesRecord.objects.all().filter(salesPerson__id__in=SalesManager.objects.values_list('user'))
    if request.GET.get('date') is not None:
        date = request.GET.get('date').split("-")
        sales_record = sales_record.filter(date__year=date[0],date__month=date[1])
    res = {}
    for record in sales_record:
        key = record.salesPerson.name
        value = res.get(key, 0)
        value += record.totalPrice
        res[key] = value
    return Response(json.dumps(res))

@api_view(['GET'])
def category_stats(request):
    sales_record = SalesRecord.objects.all().order_by('date')
    res = {}
    for record in sales_record:
        key = record.product.category
        value = res.get(key, 0)
        value += record.totalPrice
        res[key] = value
    return Response(json.dumps(res))


def _find_by_year_month(year, month):
    return SalesRecord.objects.filter(date__year=year).filter(date__month=month)


def _find_by_year_quarter(year, quarter):
    return SalesRecord.objects.filter(date__year=year).filter(date__quarter=quarter)

