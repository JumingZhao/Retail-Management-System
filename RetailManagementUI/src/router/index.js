import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

// 引入组件

import vSupplierManagement from '../components/vSupplierManagement'
import vSupplierPrice from '../components/vSupplierPrice'
import vPersonList from '../components/vPersonList'
import vProduct from '../components/vProduct.vue'
import vSalesRecord from '../components/vSalesRecord.vue'
import vStoreManagement from '../components/vStoreManagement.vue'
import vPurchaseRecord from '../components/vPurchaseRecord'
import vWarehouse from '../components/vWarehouse.vue'
import vWarehouseInventory from '../components/vWarehouseInventory.vue'
import vSalesChart from '../components/vSalesChart.vue'
import vMonthlyChart from '../components/vMonthlyChart.vue'
import vCategoryChart from '../components/vCategoryChart.vue'

export default new Router({
  routes: [
    {
      path: '/',
    },
    {
      path: '/storeManagement',
      component: vStoreManagement
    },
    {
      path: '/supplierManagement',
      component: vSupplierManagement
    },
    {
      path: '/supplierPrice',
      component: vSupplierPrice
    },
    {
      path: '/salesRecord',
      component: vSalesRecord
    },
    {
      path: '/personList',
      component: vPersonList
    },
    {
      path: '/productManagement',
      component: vProduct
    },
    {
      path: '/purchaseRecord',
      component: vPurchaseRecord
    },
    {
      path: '/warehouseManagement',
      component: vWarehouse
    },
    {
      path: '/warehouseInventory',
      component: vWarehouseInventory
    },
    {
      path: '/saleschart',
      component: vSalesChart
    },
    {
      path: '/monthlychart',
      component: vMonthlyChart
    },
    {
      path: '/categorychart',
      component: vCategoryChart
    }


  ]
})
