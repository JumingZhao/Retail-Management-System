<template>
  <div class="person-list" v-if="canView">
    <div class="add-warehouseInventory">
      <Button @click.native="showAddWarehouseInventoryModal" type="primary" icon="person-add">添加库存记录</Button>
    </div>
    <div class="search-box">
      <Input v-model="product" placeholder="请输入商品姓名" @keyup.enter.native="searchInventory"></Input>
      <Button @click.native="searchInventory" type="primary" icon="search" style="margin: 5px">搜索</Button>
      <Button @click.native="clearSearch" type="primary" icon="backspace" style="margin: 5px">清除</Button>
    </div>
    <div class="warehouseInventory-list">
      <Table class="table" style="width:100%" :columns="warehouseInventoryTable" :data="warehouseInventoryList"></Table>
      <Page @on-change="changePage" v-if="pageFlag" :current="currPage" :total="totalCount" :page-size="20" show-elevator
            class="page"></Page>
    </div>
    <Modal title="添加库存" v-model="addWarehouseInventoryFlag" :styles="{top: '20px'}" width="400">
      <Form ref="newWarehouseInventory" :model="newWarehouseInventory" :rules="checkRule" :label-width="100">
        <Select v-model="newWarehouseInventory.warehouse" placeholder="请选择仓库" style="width:200px;margin-left: 100px;">
          <Option v-for="warehouse in warehouseList" :value="warehouse.address" :key="warehouse.id">
            {{ warehouse.address }}
          </Option>

        </Select>
        <Select v-model="newWarehouseInventory.product" placeholder="请选择产品" style="width:200px;margin-left: 100px;">
          <Option v-for="product in productList" :value="product.name" :key="product.id">
            {{ product.name }}
          </Option>
        </Select>
        <FormItem label="数量" prop="quantity">
          <Input v-model="newWarehouseInventory.quantity" placeholder="请输入数量"></Input>
        </FormItem>
      </Form>
      <div slot="footer">
        <Button @click.native="submitAddWarehouseInventory" type="primary">确认</Button>
        <Button @click.native="resetAddWarehouseInventory" type="text">重置</Button>
      </div>
    </Modal>
    <Modal title="编辑仓库" v-model="editWarehouseInventoryFlag" :styles="{top: '20px'}" width="400">
      <Form ref="newWarehouseInventory" :model="selectedWarehouseInventory" :rules="checkRule" :label-width="100">
        <FormItem label="仓库" prop="name">
          <Input disabled="true" v-model="selectedWarehouseInventory.warehouse" placeholder="请输入仓库地址"></Input>
        </FormItem>
        <FormItem label="产品" prop="name">
          <Input disabled="true" v-model="selectedWarehouseInventory.product" placeholder="请输入产品"></Input>
        </FormItem>
        <FormItem label="数量" prop="quantity">
          <Input v-model="selectedWarehouseInventory.quantity" placeholder="请输入数量"></Input>
        </FormItem>
      </Form>
      <div slot="footer">
        <Button @click.native="submitEditWarehouseInventory" type="primary">确认</Button>
        <Button @click.native="resetEditWarehouseInventory" type="text">取消</Button>
      </div>
    </Modal>
    <Modal title="删除仓库" v-model="removeWarehouseInventoryFlag" :styles="{top: '20px'}" width="400">
      <h1>确定删除仓库？</h1>
      <div slot="footer">
        <Button @click.native="submitRemoveWarehouseInventory" type="primary">确认</Button>
        <Button @click.native="resetRemoveWarehouseInventory" type="text">取消</Button>
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
      warehouseInventoryTable: [
        {
          title: '仓库',
          align: 'center',
          key: 'warehouse',
          render: (h, {row}) => {
            return row.warehouse.address
          }
        },
        {
          title: '产品',
          align: 'center',
          key: 'product',
          render: (h, {row}) => {
            return row.product.name
          }
        },
        {
          title: '数量',
          align: 'center',
          key: 'quantity'
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
                      this.editWarehouseInventoryFlag = true
                      let inventory = this.warehouseInventoryList[params.index]
                      this.selectedWarehouseInventory.id = inventory.id
                      this.selectedWarehouseInventory.warehouse = inventory.warehouse.address
                      this.selectedWarehouseInventory.product = inventory.product.name
                      this.selectedWarehouseInventory.quantity = inventory.quantity
                    } else {
                      this.$Message.error('当前用户没有编辑仓库权限');
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

                      this.removeWarehouseInventoryFlag = true
                      let inventory = this.warehouseInventoryList[params.index]
                      this.selectedWarehouseInventory.id = inventory.id
                      this.selectedWarehouseInventory.warehouse = inventory.warehouse.address
                      this.selectedWarehouseInventory.product = inventory.product.name
                      this.selectedWarehouseInventory.quantity = inventory.quantity
                    } else {
                      this.$Message.error('当前用户没有删除仓库权限');
                    }
                  }
                }
              }, '删除')])
          }
        }
      ],
      warehouseInventoryList: [],
      addWarehouseInventoryFlag: false,
      editWarehouseInventoryFlag: false,
      removeWarehouseInventoryFlag: false,
      newWarehouseInventory: {
        warehouse: '',
        product: '',
        quantity: ''
      },
      selectedWarehouseInventory: {
        id: '',
        warehouse: '',
        product: '',
        quantity: ''
      },
      warehouseList: [],
      productList: [],
      warehouse: '',
      product: '',
      pageFlag: true,
      currPage: 1,
      totalCount: 0,
      newSearch: true,
      checkRule: {
        quantity: {validator: checkQuantity, trigger: 'blur'},
      },
    }
  },
  created: function () {
    this.getAllWarehouseInventorys()
    this.getAllProducts()
    this.getAllWarehouses()
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
    canView: function () {
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
    currRole: function () {
      return this.$store.state.currUser.role
    }

  },
  methods: {
    getAllWarehouseInventorys() {
      this.$http.get('http://127.0.0.1:8000/warehouseinventory/')
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (response.status === 200) {
              this.warehouseInventoryList = res['results']
              this.currPage = 1
              this.totalCount = res['total_count']
            } else {
              this.$Message.error('查询失败')
            }
          })
    },
    submitAddWarehouseInventory() {
      this.$http.put('http://127.0.0.1:8000/warehouseinventory/', this.newWarehouseInventory)
          .then((response) => {
            this.$Message.success('添加成功')
            this.getAllWarehouseInventorys()
          }, response => {
            this.$Message.error('添加失败')
          })
      this.addWarehouseInventoryFlag = false
      this.getAllWarehouseInventorys()
    },
    resetAddWarehouseInventory() {
      this.newWarehouseInventory = {
        address: ''
      }
    },
    submitEditWarehouseInventory() {
      this.$http.post('http://127.0.0.1:8000/warehouseinventory/', this.selectedWarehouseInventory)
          .then((response) => {
            this.$Message.success('更新成功')
            this.getAllWarehouseInventorys()
          }, reason => {
            this.$Message.error('更新失败')
          })
      this.editWarehouseInventoryFlag = false
      this.selectedWarehouseInventory = {
        id: '',
        address: ''
      }
      this.getAllWarehouseInventorys()

    },
    resetEditWarehouseInventory() {
      this.selectedWarehouseInventory = {
        name: '',
        sell_price: '',
        category: ''
      }
      this.editWarehouseInventoryFlag = false
    },
    submitRemoveWarehouseInventory() {

      this.$http.post('http://127.0.0.1:8000/warehouseInventory/remove', this.selectedWarehouseInventory)
          .then((response) => {
            this.$Message.success('删除成功')
            this.getAllWarehouseInventorys()
          }, reason => {
            this.$Message.error('删除失败')
          })
      this.removeWarehouseInventoryFlag = false
      this.selectedWarehouseInventory = {
        id: '',
        address: ''
      }
      this.getAllWarehouseInventorys()
    },
    resetRemoveWarehouseInventory() {
      this.selectedWarehouseInventory = {
        name: '',
        sell_price: '',
        category: ''
      }
      this.editWarehouseInventoryFlag = false
    },
    showAddWarehouseInventoryModal() {
      if (this.canAdd) {
        this.addWarehouseInventoryFlag = true
      } else {
        this.$Message.error('当前用户没有添加仓库权限');
      }

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
    getAllProducts() {
      this.$http.get('http://127.0.0.1:8000/products/')
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (response.status === 200) {
              this.productList = res
            } else {
              this.$Message.error('查询失败')
            }
          })
    },
    clearSearch() {
      this.product = ''
      this.getAllWarehouseInventorys()
    },
    searchInventory() {
      let param = {};

      if (this.product !== '') {
        param['product'] = this.product;
      }

      if(this.newSearch)
        this.currPage = 1;
      this.newSearch = true

      param['page'] = this.currPage

      this.$http.get('http://127.0.0.1:8000/warehouseinventory/', {params: param})
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (response.status === 200) {
              this.warehouseInventoryList = res['results']
              this.totalCount = res['total_count']
            } else {
              this.$Message.error('查询失败')
            }
          })
    },
    changePage(num) {
      this.currPage = num
      this.newSearch = false
      this.searchInventory()
    }
  }
}
</script>

<style>

.add-warehouseInventory {
  padding: 10px;
}

.table table {
  width: 100% !important;
}

.button button {
  padding: 10px;
}


</style>
