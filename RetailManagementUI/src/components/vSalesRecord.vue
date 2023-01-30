<template>
  <div class="sales-record" v-if="canView">
    <div class="add-person">
      <Button @click.native="showAddSalesRecord" type="primary" icon="person-add">添加销售记录</Button>
    </div>
    <div class="cash-search-box">
      <Select v-model="store" :clearable="true" placeholder="请选择门店" style="width:200px">
        <Option v-for="store in storeList" :value="store.name" :key="store.id">
          {{ store.name }}
        </Option>
        <Option value="">所有门店</Option>
      </Select>
      <!--<Select v-model="user" :clearable="true" placeholder="请选择收银员" style="width:200px">
        <Option v-for="user in userList" :value="user.name" :key="user.id">
          {{ user.name }}
        </Option>
        <Option value="">所有用户</Option>
      </Select> -->
      <DatePicker type="daterange" v-model="date" :options="daterange" placement="bottom-end" placeholder="选择日期范围"
                  style="width: 200px"></DatePicker>
      <Button @click.native="searchCashRegister" type="primary" icon="search">搜索</Button>
    </div>
    <div class="checkout-list">
      <Table :columns="salesRecordTable" :data="salesRecordList"></Table>
      <Page @on-change="changePage" v-if="pageFlag" :current="currPage" :total="totalCount" :page-size="20" show-elevator
            class="page"></Page>
    </div>
    <Modal title="添加销售记录" v-model="addSalesRecordFlag" :styles="{top: '20px'}" width="400">
      <Form ref="addSalesRecord" :model="newSalesRecord" :rules="checkRule" :label-width="100">
        <Select v-model="newSalesRecord.store" placeholder="请选择门店" style="width:200px;margin-left: 100px;">
          <Option v-for="store in storeList" :value="store.name" :key="store.id">
            {{ store.name }}
          </Option>
        </Select>
        <Select v-model="newSalesRecord.product" v-on="" change="onChange()" placeholder="请选择产品"
                style="width:200px;margin-left: 100px;">
          <Option v-for="product in productList" :value="product.name" :key="product.id">
            {{ product.name }}
          </Option>
        </Select>
        <Select v-model="newSalesRecord.salesPerson" placeholder="请选择销售员" style="width:200px;margin-left: 100px;">
          <Option v-for="user in userList" :value="user.name" :key="user.id">
            {{ user.name }}
          </Option>
        </Select>

        <FormItem label="商品单价" prop="price">
          <Input v-model.number="newSalesRecord.price" placeholder="请输入商品单价"></Input>
        </FormItem>
        <FormItem label="商品数量" prop="quantity">
          <Input v-model.number="newSalesRecord.quantity" placeholder="请输入商品数量"></Input>
        </FormItem>
      </Form>
      <div slot="footer">
        <Button type="primary" @click="submitNewSalesRecord">提交</Button>
        <Button type="ghost" @click="resetNewSalesRecord" style="margin-left: 10px">重置</Button>
      </div>

    </Modal>
    <Modal title="编辑销售记录" v-model="editSalesRecordFlag" :styles="{top: '20px'}" width="400">
      <Form ref="editSalesRecordFlag" :model="currSalesRecord" :rules="checkRule" :label-width="100">

        <FormItem label="商品名称" prop="name">
          <Input disabled="true" v-model="currSalesRecord.product" placeholder="请输入商品名称"></Input>
        </FormItem>
        <FormItem label="商品单价" prop="price">
          <Input v-model.number="currSalesRecord.price" placeholder="请输入商品单价"></Input>
        </FormItem>
        <FormItem label="商品数量" prop="quantity">
          <Input v-model.number="currSalesRecord.quantity" placeholder="请输入商品数量"></Input>
        </FormItem>
        <FormItem label="商品规格" prop="unit">
          <Input disabled="true" v-model="currSalesRecord.unit" placeholder="请输入商品规格"></Input>
        </FormItem>
        <FormItem label="销售员" prop="salesPerson">
          <Input disabled="true" v-model="currSalesRecord.salesPerson" placeholder="请输入销售员"></Input>
        </FormItem>
        <FormItem label="门店" prop="store">
          <Input disabled="true" v-model="currSalesRecord.store" placeholder="请输入门店"></Input>
        </FormItem>
      </Form>
      <div slot="footer">
        <Button type="primary" @click="submitEditSalesRecord">提交</Button>
        <Button type="ghost" @click="resetEditSalesRecord" style="margin-left: 10px">取消</Button>
      </div>

    </Modal>
    <Modal title="删除销售记录" v-model="removeSalesRecordFlag" :styles="{top: '20px'}" width="400">
      <h1>确定删除用户？</h1>
      <div slot="footer">
        <Button @click.native="submitRemoveSalesRecord" type="primary">确认</Button>
        <Button @click.native="resetRemoveSalesRecord" type="text">取消</Button>
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
      addSalesRecordFlag: false,
      editSalesRecordFlag: false,
      removeSalesRecordFlag: false,
      user: '',
      date: '',
      store: '',
      userList: [],
      storeList: [],
      productList: [],
      daterange: {
        shortcuts: [
          {
            text: '最近一周',
            value() {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
              return [start, end];
            }
          },
          {
            text: '最近一个月',
            value() {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
              return [start, end];
            }
          },
          {
            text: '最近三个月',
            value() {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
              return [start, end];
            }
          }
        ]
      },
      salesRecordList: [],
      salesRecordTable: [

        {
          title: '销售员',
          align: 'center',
          key: 'salesPerson',
          render: (h, {row}) => {
            return row.salesPerson.name
          }
        },
        {
          title: '商品名',
          align: 'center',
          key: 'product',
          render: (h, {row}) => {
            return row.product.name
          }
        },
        {
          title: '数量',
          align: 'center',
          key: 'quantity',
          sortable: true,
        },
        {
          title: '规格',
          align: 'center',
          key: 'product',
          render: (h, {row}) => {
            return row.product.unit
          }
        },
        {
          title: '订单金额',
          align: 'center',
          key: 'totalPrice',
          sortable: true,
        },
        {
          title: '门店',
          align: 'center',
          key: 'store',
          render: (h, {row}) => {
            return row.store.name
          }
        },
        {
          title: '时间',
          align: 'center',
          key: 'date',
          sortable: true,
        },
        {
          title: '操作',
          align: 'center',
          key: 'action',
          render: (h, params) => {
            return h('div', [h('Button', {
              props: {
                type: 'warning',
                size: 'small',
                icon: 'trash-b'
              },
              on: {
                click: () => {
                  if (this.canEdit) {
                    let curr = this.salesRecordList[params.index]
                    this.currSalesRecord.id = curr.id
                    this.currSalesRecord.product = curr.product.name
                    this.currSalesRecord.price = curr.totalPrice / curr.quantity
                    this.currSalesRecord.quantity = curr.quantity
                    this.currSalesRecord.salesPerson = curr.salesPerson.name
                    this.currSalesRecord.store = curr.store.name
                    this.currSalesRecord.date = curr.date
                    this.currSalesRecord.unit = curr.product.unit
                    this.editSalesRecordFlag = true
                  } else {
                    this.$Message.error('当前用户没有权限编辑销售记录');
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
                      let curr = this.salesRecordList[params.index]
                      this.currSalesRecord.id = curr.id
                      this.currSalesRecord.product = curr.product.name
                      this.currSalesRecord.price = curr.totalPrice / curr.quantity
                      this.currSalesRecord.quantity = curr.quantity
                      this.currSalesRecord.salesPerson = curr.salesPerson.name
                      this.currSalesRecord.store = curr.store.name
                      this.currSalesRecord.date = curr.date
                      this.removeSalesRecordFlag = true
                    } else {
                      this.$Message.error('当前用户没有删除销售记录');
                    }

                  }
                }
              }, '删除')])
          }
        }
      ],
      newSalesRecord: {
        product: '',
        price: '',
        quantity: '',
        unit: '',
        salesPerson: '',
        store: '',
        date: '',
      },
      currSalesRecord: {
        id: '',
        product: '',
        price: '',
        unit: '',
        quantity: '',
        salesPerson: '',
        store: '',
        date: '',
      },
      pageFlag: true,
      currPage: 1,
      totalCount: 0,
      newSearch: true,
      checkRule: {
        price: {validator: checkPrice, trigger: 'blur'},
        quantity: {validator: checkQuantity, trigger: 'blur'},

      },
    }
  },
  computed: {
    canEdit: function () {
      if (this.$store.state.currUser.role === 'super_admin' || this.$store.state.currUser.role === 'salesperson') {
        return true;
      } else {
        return false;
      }
    },
    canAdd: function () {
      if (this.$store.state.currUser.role === 'super_admin' || this.$store.state.currUser.role === 'salesperson') {
        return true;
      } else {
        return false;
      }
    },
    canDelete: function () {
      if (this.$store.state.currUser.role === 'super_admin' || this.$store.state.currUser.role === 'salesperson') {
        return true;
      } else {
        return false;
      }
    },
    canView: function () {
      if (this.$store.state.currUser.role !== 'warehouse_admin') {
        return true;
      } else {
        return false;
      }
    },
  },
  created: function () {
    this.getAllSalesRecord()
    this.getAllUsers()
    this.getAllStores()
    this.getAllProducts()
  },
  methods: {
    // 搜索收银记录
    searchCashRegister() {
      let _this = this;
      if(this.newSearch)
        this.currPage = 1;
      this.newSearch = true
      let param = {};


      if (this.user !== '') {
        param['user'] = this.user;
      }
      if (this.date.length !== 0 && this.date[0] !== null) {
        param['start'] = this.date[0].getFullYear() + '-' + (this.date[0].getMonth() + 1) + '-' + this.date[0].getDate()
        param['end'] = this.date[1].getFullYear() + '-' + (this.date[1].getMonth() + 1) + '-' + this.date[1].getDate()
      }
      if (this.store !== '') {
        param['store'] = this.store;
      }

      param['page'] = this.currPage

      this.$http.get('http://127.0.0.1:8000/salesrecord/', {params: param})
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (response.status === 200) {
              this.salesRecordList = res['results']
              this.totalCount = res['total_count']
            } else {
              this.$Message.error('查询失败')
            }
          })
    },

    getAllSalesRecord() {
      this.$http.get('http://127.0.0.1:8000/salesrecord/')
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (response.status === 200) {
              this.salesRecordList = res['results']
              this.currPage = 1
              this.totalCount = res['total_count']
            } else {
              this.$Message.error('查询失败')
            }
          })
    },
    getAllUsers() {
      this.$http.get('http://127.0.0.1:8000/users/')
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            console.log(res)
            if (response.status === 200) {
              this.userList = res
            } else {
              this.$Message.error('查询失败')
            }
          })
    },
    getAllStores() {
      this.$http.get('http://127.0.0.1:8000/store/')
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            console.log(res)
            if (response.status === 200) {
              this.storeList = res
            } else {
              this.$Message.error('查询失败')
            }
          })
    },
    submitNewSalesRecord() {
      let record = {
        product: this.newSalesRecord.product,
        quantity: this.newSalesRecord.quantity,
        store: this.newSalesRecord.store,
        totalPrice: this.newSalesRecord.quantity * this.newSalesRecord.price,
        userId: this.newSalesRecord.salesPerson,
        date: this.getCurrentDate()
      }
      let payload = [record]
      this.newSalesRecord = {
        product: '',
        price: '',
        quantity: '',
        salesPerson: '',
        store: '',
        date: '',
      },
          this.$http.put('http://127.0.0.1:8000/salesrecord/', payload)
              .then((response) => {
                    this.$Message.success('添加成功')
                    this.getAllUsers()
                  },
                  response => {
                    this.$Message.error('添加失败')
                  })
      this.addSalesRecordFlag = false;
      this.getAllSalesRecord()
      this.store = ''
      this.user = ''
      this.date = ''

    },
    // 重置
    resetNewSalesRecord() {
      this.newSalesRecord = {
        product: '',
        price: '',
        quantity: '',
        salesPerson: '',
        store: '',
        date: '',
      }
    },
    submitEditSalesRecord() {

      let record = {
        id: this.currSalesRecord.id,
        product: this.currSalesRecord.product,
        quantity: this.currSalesRecord.quantity,
        store: this.currSalesRecord.store,
        totalPrice: this.currSalesRecord.quantity * this.currSalesRecord.price,
        userId: this.currSalesRecord.salesPerson,
        date: this.getCurrentDate()
      }
      let payload = [record]
      this.currSalesRecord = {
        id: '',
        product: '',
        price: '',
        quantity: '',
        salesPerson: '',
        store: '',
        date: '',
      },
          this.$http.post('http://127.0.0.1:8000/salesrecord/', payload)
              .then((response) => {
                    this.$Message.success('编辑成功')
                    this.getAllUsers()
                  },
                  response => {
                    this.$Message.error('编辑失败')
                  })
      this.getAllSalesRecord()
      this.editSalesRecordFlag = false
      this.store = ''
      this.user = ''
      this.date = ''

    },
    // 重置
    resetEditSalesRecord() {
      this.currSalesRecord = {
        id: '',
        product: '',
        price: '',
        quantity: '',
        salesPerson: '',
        store: '',
        date: '',
      },
          this.editSalesRecordFlag = false
    },
    submitRemoveSalesRecord() {
      this.$http.post('http://127.0.0.1:8000/salesrecord/remove', this.currSalesRecord)
          .then((response) => {
                this.$Message.success('删除成功')
                this.getAllUsers()
              },
              response => {
                this.$Message.error('删除失败')
              })
      this.currSalesRecord = {
        id: '',
        product: '',
        price: '',
        quantity: '',
        salesPerson: '',
        store: '',
        date: '',
      }
      this.getAllSalesRecord()
      this.removeSalesRecordFlag = false;
      this.store = ''
      this.user = ''
      this.date = ''
    },
    resetRemoveSalesRecord() {
      this.currSalesRecord = {
        id: '',
        product: '',
        price: '',
        quantity: '',
        salesPerson: '',
        store: '',
        date: '',
      },
          this.removeSalesRecordFlag = false;
    },
    showAddSalesRecord() {
      if (this.canAdd) {
        this.addSalesRecordFlag = true
      } else {
        this.$Message.error('当前用户没有权限添加销售记录');
      }
    },
    getCurrentDate() {
      var today = new Date();
      var dd = String(today.getDate()).padStart(2, '0');
      var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
      var yyyy = today.getFullYear();
      return yyyy + '-' + mm + '-' + dd;
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
    changePage(num) {
      this.currPage = num
      this.newSearch = false
      this.searchCashRegister()
    }
  }

}
</script>

<style>
.cash-search-box {
  padding: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.cash-search-box > div {
  margin-right: 2em;
}

.page {
  margin: 10px 0;
  display: flex;
  justify-content: center;
}

.sales-record td.ivu-table-expanded-cell {
  padding: 10px;
  margin: 0px;
}

.page {
  margin: 10px 0;
  display: flex;
  justify-content: center;
}

.add-person {
  padding: 10px;
}
</style>
