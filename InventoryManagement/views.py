from django.shortcuts import render
from django.utils.dateparse import parse_date

from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
from InventoryManagement.models import Warehouse, WarehouseInventory, StoreInventory, Store, PurchaseRecord, \
    SupplierPrice, Product, Supplier
from InventoryManagement.serializers import WarehouseSerializer, WarehouseInventorySerializer, StoreInventorySerializer, \
    SupplierSerializer, PurchaseRecordSerializer, StoreSerializer, ProductAllSerializer, SupplierPriceSerializer


@api_view(['GET','PUT','POST'])
def warehouse_inventory(request):
    if request.method == 'GET':
        inventory = WarehouseInventory.objects.all()
        if request.GET.get("product") is not None:
            inventory = inventory.filter(product__name=request.GET.get("product"))
        paginator = PageNumberPagination()
        page_obj = paginator.paginate_queryset(inventory, request)
        serializer = WarehouseInventorySerializer(page_obj, many=True)
        return Response({
            'page_size': paginator.page_size,
            'total_count': paginator.page.paginator.count,
            'results': serializer.data})
    elif request.method == 'PUT':
        record = request.data
        if record['quantity'] < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        inventory = WarehouseInventory()
        warehouse = Warehouse.objects.get(address=record['warehouse'])
        product = Product.objects.get(name=record['product'])
        inventory.warehouse = warehouse
        inventory.product = product
        inventory.quantity = record['quantity']
        inventory.save()
        return Response(status=status.HTTP_200_OK)
    else:
        record = request.data
        if record['quantity'] < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        inventory = WarehouseInventory.objects.get(id=record['id'])
        warehouse = Warehouse.objects.get(address=record['warehouse'])
        product = Product.objects.get(name=record['product'])
        inventory.warehouse = warehouse
        inventory.product = product
        inventory.quantity = record['quantity']
        inventory.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
def delete_warehouse_inventory(request):
    record = request.data
    inventory = WarehouseInventory.objects.get(record['id'])
    inventory.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET','PUT','POST'])
def warehouse(request):
    if request.method == 'GET':
        warehouse = Warehouse.objects.all()
        serializer = WarehouseSerializer(warehouse, many=True)
        return Response(serializer.data)
    elif request.method == 'PUT':
        record = request.data
        warehouse = Warehouse()
        warehouse.address = record['address']
        warehouse.save()
        return Response(status=status.HTTP_200_OK)
    else:
        record = request.data
        warehouse = Warehouse.objects.get(id=record['id'])
        warehouse.address = record['address']
        warehouse.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def delete_warehouse(request):
    record = request.data
    warehouse = Warehouse.objects.get(id=record['id'])
    warehouse.delete()
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def store_inventory(request):
    store = request.GET.get("id")
    inventory = StoreInventory.objects.filter(store__id=store)
    serializer = StoreInventorySerializer(inventory, many=True)
    return Response(serializer.data)

@api_view(['GET','PUT','POST'])
def store(request):
    if request.method == 'GET':
        store = Store.objects.all()
        serializer = StoreSerializer(store, many=True)
        return Response(serializer.data)
    elif request.method == 'PUT':
        record = request.data
        store = Store()
        store.name = record['name']
        store.address = record['address']
        store.phone = record['phone']
        store.save()
        return Response(status=status.HTTP_200_OK)
    else:
        record = request.data
        store = Store.objects.get(id=record['id'])
        store.name = record['name']
        store.address = record['address']
        store.phone = record['phone']
        store.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def delete_store(request):
    record = request.data
    store = Store.objects.get(id=record['id'])
    store.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET','POST','PUT'])
def purchase_record(request):
    if request.method == 'GET':
        purchaseRecord = PurchaseRecord.objects.all()
        if request.GET.get('product') is not None:
            purchaseRecord = purchaseRecord.filter(product__name=request.GET.get('product'))
        if request.GET.get('date') is not None:
            date = parse_date(request.GET.get('date'))
            purchaseRecord = purchaseRecord.filter(deliveryDate=date)
        paginator = PageNumberPagination()
        page_obj = paginator.paginate_queryset(purchaseRecord, request)
        serializer = PurchaseRecordSerializer(page_obj, many=True)
        return Response({
            'page_size': paginator.page_size,
            'total_count': paginator.page.paginator.count,
            'results': serializer.data})
    elif request.method == 'PUT':
        record = request.data
        if record['totalPrice'] < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        purchaseRecord = PurchaseRecord()
        product = Product.objects.get(name=record['product'])
        warehouse = Warehouse.objects.get(address=record['warehouse'])
        supplier = Supplier.objects.get(name=record['supplier'])
        purchaseRecord.product = product
        purchaseRecord.warehouse = warehouse
        purchaseRecord.supplier = supplier
        purchaseRecord.quantity = record['quantity']
        purchaseRecord.totalPrice = record['totalPrice']
        purchaseRecord.deliveryDate = parse_date(record['deliveryDate'])
        purchaseRecord.save()
        return Response(status=status.HTTP_200_OK)
    else:
        record = request.data
        if record['totalPrice'] < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        purchaseRecord = PurchaseRecord.objects.get(id=record['id'])
        product = Product.objects.get(name=record['product'])
        warehouse = Warehouse.objects.get(address=record['warehouse'])
        supplier = Supplier.objects.get(name=record['supplier'])
        purchaseRecord.product = product
        purchaseRecord.warehouse = warehouse
        purchaseRecord.supplier = supplier
        purchaseRecord.quantity = record['quantity']
        purchaseRecord.totalPrice = record['totalPrice']
        purchaseRecord.deliveryDate = parse_date(record['deliveryDate'])
        purchaseRecord.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def delete_purchase_record(request):
    record = request.data
    purchaseRecord = PurchaseRecord.objects.get(id=record['id'])
    purchaseRecord.delete()
    return Response(status=status.HTTP_200_OK)

@api_view(['GET','POST','PUT'])
def supplier_price(request):
    if request.method == 'GET':
        supplier = SupplierPrice.objects.all()
        if request.GET.get('product') is not None:
            supplier = supplier.filter(product__name=request.GET.get('product'))
        if request.GET.get('supplier') is not None:
            supplier = supplier.filter(supplier__name=request.GET.get('supplier'))
        serializer = SupplierPriceSerializer(supplier, many=True)
        return Response(serializer.data)
    elif request.method == 'PUT':
        record = request.data
        if record['price'] < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        supplier_price = SupplierPrice()
        product = Product.objects.get(name=record['product'])
        supplier = Supplier.objects.get(name=record['supplier'])
        curr = SupplierPrice.objects.filter(product__id=product.id).filter(supplier__id=supplier.id).first()
        if curr is not None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        supplier_price.product = product
        supplier_price.supplier = supplier
        supplier_price.price = record['price']
        supplier_price.save()
        return Response(status=status.HTTP_200_OK)
    else:
        record = request.data
        if record['price'] < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        supplier_price = SupplierPrice.objects.get(id=record['id'])
        supplier_price.price = record['price']
        supplier_price.save()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def delete_supplier_price(request):
        record = request.data
        supplier_price = SupplierPrice.objects.get(id=record['id'])
        supplier_price.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST', 'PUT'])
def purchase(request):
    if request.method == 'PUT':
        purchase_record_serializer = PurchaseRecordSerializer(data=request.data)
        purchase_record_serializer.is_valid(raise_exception=True)
        purchase_record_serializer.save()
    elif request.method == 'POST':
        return

    return Response(status.HTTP_200_OK)


@api_view(['GET', 'POST', 'PUT'])
def product(request):
    if request.method == 'GET':
        product = Product.objects.all()
        if request.GET.get('product') is not None:
            product = product.filter(name__contains=request.GET.get('product'))
        if request.GET.get('category') is not None:
            product = product.filter(category__contains=request.GET.get('category'))
        serializer = ProductAllSerializer(product, many=True)
        return Response(serializer.data)
    elif request.method == 'PUT':
        print(request.data)
        if request.data['sell_price'] < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = ProductAllSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    else:
        record = request.data
        print(request.data)
        if record['sell_price'] < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        product = Product.objects.get(id=record['id'])
        product.name = record['name']
        product.sell_price = record['sell_price']
        product.category = record['category']
        product.unit = record['unit']
        product.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def remove_product(request):
    record = request.data
    print(request.data)
    product = Product.objects.get(id=record['id'])
    product.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET','PUT', 'POST'])
def supplier(request):
    if request.method == 'GET':
        supplier = Supplier.objects.all()
        serializer = SupplierSerializer(supplier, many=True)
        return Response(serializer.data)
    elif request.method == 'PUT':
        record = request.data
        supplier = Supplier()
        supplier.name = record['name']
        supplier.address = record['address']
        supplier.phone = record['phone']
        supplier.save()
        return Response(status=status.HTTP_200_OK)
    else:
        record = request.data
        supplier = Supplier.objects.get(id=record['id'])
        supplier.name = record['name']
        supplier.address = record['address']
        supplier.phone = record['phone']
        supplier.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def remove_supplier(request):
    record = request.data
    supplier = Supplier.objects.get(id=record['id'])
    supplier.delete()
    return Response(status=status.HTTP_200_OK)

