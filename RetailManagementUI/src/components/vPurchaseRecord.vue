<template>
  <div class="person-list" v-if="canView">
    <div class="add-purchaseRecord">
      <Button @click.native="showAddPurchaseRecordModal" type="primary" icon="person-add">添加新供货记录</Button>
    </div>
    <div class="search-box">
      <Input v-model="product" placeholder="请输入商品姓名" style="width: 200px" @keyup.enter.native="searchRecord"></Input>
      <DatePicker type="date" v-model="date" :options="date" placement="bottom-end" placeholder="选择送货日期"
                  style="width: 200px"></DatePicker>
      <Button @click.native="searchRecord" type="primary" icon="search" style="margin: 5px">搜索</Button>
      <Button @click.native="clearSearch" type="primary" icon="backspace" style="margin: 5px">清除</Button>
    </div>
    <div class="purchaseRecord-list">
      <Table class="table" style="width:100%" :columns="purchaseRecordTable" :data="purchaseRecordList"></Table>
      <Page @on-change="changePage" v-if="pageFlag" :current="currPage" :total="totalCount" :page-size="20" show-elevator
            class="page"></Page>
    </div>
    <Modal title="添加订单" v-model="addPurchaseRecordFlag" :styles="{top: '20px'}" width="400">
      <Form ref="newPurchaseRecord" :model="newPurchaseRecord" :rules="checkRule" :label-width="100">
        <Select v-model="newPurchaseRecord.warehouse" placeholder="请选择仓库" style="width:200px;margin-left: 100px;">
          <Option v-for="warehouse in warehouseList" :value="warehouse.address" :key="warehouse.id">
            {{ warehouse.address }}
          </Option>
        </Select>
        <Select v-model="newPurchaseRecord.product" placeholder="请选择产品" style="width:200px;margin-left: 100px;">
          <Option v-for="product in productList" :value="product.name" :key="product.id">
            {{ product.name }}
          </Option>
        </Select>
        <Select v-model="newPurchaseRecord.supplier" placeholder="请选择供应商" style="width:200px;margin-left: 100px;">
          <Option v-for="supplier in supplierList" :value="supplier.name" :key="supplier.id">
            {{ supplier.name }}
          </Option>
        </Select>
        <!--                <FormItem label="商品" prop="name">-->
        <!--                    <Input v-model="newPurchaseRecord.product" placeholder="请输入商品名称"></Input>-->
        <!--                </FormItem>-->
        <!--                <FormItem label="仓库地址" prop="coding">-->
        <!--                    <Input v-model="newPurchaseRecord.warehouse" placeholder="请输入仓库地址"></Input>-->
        <!--                </FormItem>-->
        <FormItem label="数量" prop="quantity">
          <Input v-model="newPurchaseRecord.quantity" placeholder="请输入数量"></Input>
        </FormItem>
        <FormItem label="总价" prop="totalPrice">
          <Input v-model="newPurchaseRecord.totalPrice" placeholder="请输入总价"></Input>
        </FormItem>
        <!--              <FormItem label="供应商" prop="position">-->
        <!--                    <Input v-model="newPurchaseRecord.supplier" placeholder="请输入供应商"></Input>-->
        <!--                </FormItem>-->
        <FormItem label="送货日期" prop="position">
          <Input v-model="newPurchaseRecord.deliveryDate" placeholder="请输入送货日期"></Input>
        </FormItem>
      </Form>
      <div slot="footer">
        <Button @click.native="submitAddPurchaseRecord" type="primary">确认</Button>
        <Button @click.native="resetAddPurchaseRecord" type="text">重置</Button>
      </div>
    </Modal>
    <Modal title="编辑供货记录" v-model="editPurchaseRecordFlag" :styles="{top: '20px'}" width="400">
      <Form ref="newPurchaseRecord" :model="selectedPurchaseRecord" :label-width="100">
        <FormItem label="商品" prop="name">
          <Input disabled="true" v-model="selectedPurchaseRecord.product" placeholder="请输入商品名称"></Input>
        </FormItem>
        <FormItem label="仓库地址" prop="coding">
          <Input disabled="true" v-model="selectedPurchaseRecord.warehouse" placeholder="请输入仓库地址"></Input>
        </FormItem>
        <FormItem label="数量" prop="quantity">
          <Input v-model="selectedPurchaseRecord.quantity" placeholder="请输入数量"></Input>
        </FormItem>
        <FormItem label="总价" prop="totalPrice">
          <Input v-model="selectedPurchaseRecord.totalPrice" placeholder="请输入总价"></Input>
        </FormItem>
        <FormItem label="供应商" prop="position">
          <Input disabled="true" v-model="selectedPurchaseRecord.supplier" placeholder="请输入供应商"></Input>
        </FormItem>
        <FormItem label="送货日期" prop="position">
          <Input v-model="selectedPurchaseRecord.deliveryDate" placeholder="请输入送货日期"></Input>
        </FormItem>
      </Form>
      <div slot="footer">
        <Button @click.native="submitEditPurchaseRecord" type="primary">确认</Button>
        <Button @click.native="resetEditPurchaseRecord" type="text">取消</Button>
      </div>
    </Modal>
    <Modal title="删除供货记录" v-model="removePurchaseRecordFlag" :styles="{top: '20px'}" width="400">
      <h1>确定删除供货记录？</h1>
      <div slot="footer">
        <Button @click.native="submitRemovePurchaseRecord" type="primary">确认</Button>
        <Button @click.native="resetRemovePurchaseRecord" type="text">取消</Button>
      </div>
    </Modal>
  </div>
  <h2 v-else>
    当前用户没有权限浏览本页面
  </h2>
</template>

<script>

export default {
  data() {
  const checkPrice = (rule, value, callback) => {
  console.log(value);
      const reg = /^(\d+\.\d{1,1}|\d+)$/g;
            if (value === '') {
                console.log("empty")
                callback();
            } else if (reg.test(value)) {
            console.log("pass")
                callback();
            } else {
            console.log("fail")
                callback(new Error('商品单价应为正数'));
            }
    }

    const checkQuantity = (rule, value, callback) => {
      const reg = /^[1-9]+[0-9]*$/g;
            if (value === '') {

                console.log("empty")
                callback();
            } else if (reg.test(value)) {
            console.log("pass")

                callback();
            } else {
            console.log("fail")

                callback(new Error('数量应为正整数'));
            }
    }

    return {
      purchaseRecordTable: [
        {
          title: '商品',
          align: 'center',
          key: 'product',
          render: (h, {row}) => {
            return row.product.name
          }
        },
        {
          title: '仓库地址',
          align: 'center',
          key: 'warehouse',
          render: (h, {row}) => {
            return row.warehouse.address
          }
        },
        {
          title: '数量',
          align: 'center',
          key: 'quantity'
        },
        {
          title: '总价',
          align: 'center',
          key: 'totalPrice'
        },
        {
          title: '供应商',
          align: 'center',
          key: 'supplier',
          render: (h, {row}) => {
            return row.supplier.name
          }
        },
        {
          title: '送货日期',
          align: 'center',
          key: 'deliveryDate'
        },
        {
          title: '操作',
          align: 'center',
          key: 'action',
          render: (h, params) => {
            return h('div', [
              h('Button', {
                props: {
                  type: 'warning',
                  size: 'small',
                  icon: 'trash-b'
                },
                on: {
                  click: () => {
                    if (this.canEdit) {
                      this.editPurchaseRecordFlag = true
                      let row = this.purchaseRecordList[params.index]
                      this.selectedPurchaseRecord.id = row.id
                      this.selectedPurchaseRecord.product = row.product.name
                      this.selectedPurchaseRecord.warehouse = row.warehouse.address
                      this.selectedPurchaseRecord.quantity = row.quantity
                      this.selectedPurchaseRecord.totalPrice = row.totalPrice
                      this.selectedPurchaseRecord.supplier = row.supplier.name
                      this.selectedPurchaseRecord.deliveryDate = row.deliveryDate
                    } else {
                      this.$Message.error('当前用户没有编辑供货记录权限');
                    }
                  }
                }
              }, '编辑'),
              h('Button', {
                props: {
                  type: 'error',
                  size: 'small',
                  icon: 'trash-b'
                },
                on: {
                  click: () => {
                    if (this.canDelete) {

                      this.removePurchaseRecordFlag = true
                      let row = this.purchaseRecordList[params.index]
                      this.selectedPurchaseRecord.id = row.id
                      this.selectedPurchaseRecord.product = row.product.name
                      this.selectedPurchaseRecord.warehouse = row.warehouse.address
                      this.selectedPurchaseRecord.quantity = row.quantity
                      this.selectedPurchaseRecord.totalPrice = row.totalPrice
                      this.selectedPurchaseRecord.supplier = row.supplier.name
                      this.selectedPurchaseRecord.deliveryDate = row.deliveryDate
                    } else {
                      this.$Message.error('当前用户没有删除供货记录权限');
                    }
                  }
                }
              }, '删除')])
          }
        }
      ],
      purchaseRecordList: [],
      addPurchaseRecordFlag: false,
      editPurchaseRecordFlag: false,
      removePurchaseRecordFlag: false,
      newPurchaseRecord: {
        product: '',
        warehouse: '',
        quantity: '',
        totalPrice: '',
        supplier: '',
        deliveryDate: ''
      },
      selectedPurchaseRecord: {
        id: '',
        product: '',
        warehouse: '',
        quantity: '',
        totalPrice: '',
        supplier: '',
        deliveryDate: ''
      },
      productList: [],
      warehouseList: [],
      supplierList: [],
      product: '',
      date: '',
      pageFlag: true,
      currPage: 1,
      totalCount: 0,
      newSearch: true,
      checkRule: {
        totalPrice: {validator: checkPrice, trigger: 'blur'},
        quantity: {validator: checkQuantity, trigger: 'blur'},

      },
    }
  },
  created: function () {
    this.getAllPurchaseRecords()
    this.getAllProducts()
    this.getAllWarehouses()
    this.getAllSupplier()
  },
  computed: {
    canEdit: function () {
      if (this.$store.state.currUser.role === 'super_admin' || this.$store.state.currUser.role === 'warehouse_admin') {
        return true;
      } else {
        return false;
      }
    },
    canAdd: function () {
      if (this.$store.state.currUser.role === 'super_admin' || this.$store.state.currUser.role === 'warehouse_admin') {
        return true;
      } else {
        return false;
      }
    },
    canDelete: function () {
      if (this.$store.state.currUser.role === 'super_admin' || this.$store.state.currUser.role === 'warehouse_admin') {
        return true;
      } else {
        return false;
      }
    },
    canView: function () {
      if (this.$store.state.currUser.role === 'super_admin' || this.$store.state.currUser.role === 'warehouse_admin') {
        return true;
      } else {
        return false;
      }
    },
    currRole: function () {
      return this.$store.state.currUser.role
    }

  },
  methods: {
    getAllPurchaseRecords() {
      this.$http.get('http://127.0.0.1:8000/purchaserecord/')
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            console.log(res)
            if (response.status === 200) {
              this.purchaseRecordList = res['results']
              this.currPage = 1
              this.totalCount = res['total_count']
            } else {
              this.$Message.error('查询失败')
            }
          })
    },
    submitAddPurchaseRecord() {
      this.$http.put('http://127.0.0.1:8000/purchaserecord/', this.newPurchaseRecord)
          .then((response) => {
            this.$Message.success('添加成功')
            this.getAllPurchaseRecords()
          }, response => {
            this.$Message.error('添加失败')
          })
      this.addPurchaseRecordFlag = false
    },
    resetAddPurchaseRecord() {
      this.newPurchaseRecord = {
        name: '',
        sell_price: '',
        category: ''
      }
    },
    submitEditPurchaseRecord() {
      this.$http.post('http://127.0.0.1:8000/purchaserecord/', this.selectedPurchaseRecord)
          .then((response) => {
            this.$Message.success('更新成功')
            this.getAllPurchaseRecords()
          }, reason => {
            this.$Message.error('更新失败')
          })
      this.editPurchaseRecordFlag = false
    },
    resetEditPurchaseRecord() {
      this.selectedPurchaseRecord = {
        name: '',
        sell_price: '',
        category: ''
      }
      this.editPurchaseRecordFlag = false
    },
    submitRemovePurchaseRecord() {

      this.$http.post('http://127.0.0.1:8000/purchaserecord/remove', this.selectedPurchaseRecord)
          .then((response) => {
            this.$Message.success('删除成功')
            this.getAllPurchaseRecords()
          }, reason => {
            this.$Message.error('删除失败')
          })
      this.removePurchaseRecordFlag = false
    },
    resetRemovePurchaseRecord() {
      this.selectedPurchaseRecord = {
        name: '',
        sell_price: '',
        category: ''
      }
      this.editPurchaseRecordFlag = false
    },
    showAddPurchaseRecordModal() {
      if (this.canAdd) {
        this.addPurchaseRecordFlag = true
      } else {
        this.$Message.error('当前用户没有添加供货记录权限');
      }
    },
    getAllProducts() {
      this.$http.get('http://127.0.0.1:8000/products/')
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            console.log(res)
            if (response.status === 200) {
              this.productList = res
            } else {
              this.$Message.error('查询失败')
            }
          })
    },
    getAllWarehouses() {
      this.$http.get('http://127.0.0.1:8000/warehouse/')
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (response.status === 200) {
              this.warehouseList = res
            } else {
              this.$Message.error('查询失败')
            }
          })
    },
    getAllSupplier() {
      this.$http.get('http://127.0.0.1:8000/supplier/')
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (response.status === 200) {
              this.supplierList = res
            } else {
              this.$Message.error('查询失败')
            }
          })
    },
    clearSearch() {
      this.product = ''
      this.date = ''
      this.getAllPurchaseRecords()
    },
    searchRecord() {
      let param = {};

      if(this.newSearch)
        this.currPage = 1;
      this.newSearch = true

      param['page'] = this.currPage

      if (this.product !== '') {
        param['product'] = this.product;
      }
      if (this.date !== '') {
        param['date'] = this.date.getFullYear() + '-' + (this.date.getMonth() + 1) + '-' + this.date.getDate()
      }

      this.$http.get('http://127.0.0.1:8000/purchaserecord/',{params: param})
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            console.log(res)
            if (response.status === 200) {
              this.purchaseRecordList = res['results']
              this.totalCount = res['total_count']
            } else {
              this.$Message.error('查询失败')
            }
          })
    },
    changePage(num) {
      this.currPage = num
      this.newSearch = false
      this.searchRecord()
    }

  }
}
</script>

<style>

.add-purchaseRecord {
  padding: 10px;
}

.button button {
  padding: 10px;
}


</style>
