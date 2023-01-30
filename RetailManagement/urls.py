"""RetailManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from SalesManagement import views as salesManagement
from InventoryManagement import views as inventoryManagement
from PeopleManagement import views as peopleManagement

urlpatterns = [
    path('admin/', admin.site.urls),
    path('salesrecord/', salesManagement.salesrecord),
    path('salesrecord/remove', salesManagement.delete_salesrecord),
    path('warehouseinventory/', inventoryManagement.warehouse_inventory),
    path('warehouse/', inventoryManagement.warehouse),
    path('warehouse/remove', inventoryManagement.delete_warehouse),
    path('storeinventory/', inventoryManagement.store_inventory),
    path('store/', inventoryManagement.store),
    path('store/remove', inventoryManagement.delete_store),
    path('purchaserecord/', inventoryManagement.purchase_record),
    path('purchaserecord/remove', inventoryManagement.delete_purchase_record),
    path('supplierprice/', inventoryManagement.supplier_price),
    path('supplierprice/remove', inventoryManagement.delete_supplier_price),
    path('supplier/', inventoryManagement.supplier),
    path('supplier/remove', inventoryManagement.remove_supplier),
    path('purchase/', inventoryManagement.purchase),
    path('users/', peopleManagement.all_users),
    path('products/', inventoryManagement.product),
    path('products/remove', inventoryManagement.remove_product),
    path('useradmin/', peopleManagement.user_admin),
    path('useradmin/remove', peopleManagement.remove_user),
    path('login/', peopleManagement.login),
    path('salesbymonth/', salesManagement.sales_stats),
    path('managersales/', salesManagement.manager_monthly_sales),
    path('categorystats/', salesManagement.category_stats),

]
