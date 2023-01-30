<template>
    <div class="person-list" v-if="canView">
        <div class="add-supplier">
            <Button @click.native="showAddSupplierProductModal" type="primary" icon="person-add">添加供货商商品</Button>
        </div>
      <div class="search-box">
          <Select v-model="supplier" :clearable="true" placeholder="请选择供应商" style="width:200px">
                <Option v-for="supplier in allSupplierList" :value="supplier.name" :key="supplier.id">
                    {{ supplier.name }}
                </Option>
                <Option value="">所有供应商</Option>
            </Select>
            <Select v-model="product" :clearable="true" placeholder="请选择产品" style="width:200px">
                <Option v-for="product in allProductList" :value="product.name" :key="product.id">
                    {{ product.name }}
                </Option>
                <Option value="">所有产品</Option>
            </Select>
            <Button @click.native="searchSupplierPrice" type="primary" icon="search">搜索</Button>
        </div>
       <div class="supplier-list">
            <Table class="table" style="width:100%" :columns="supplierTable" :data="supplierList"></Table>
        </div>
      <Modal title="添加供货商产品" v-model="addSupplierProductFlag" :styles="{top: '20px'}" width="400">
            <Form ref="newSupplier" :model="newSupplierProduct" :rules="checkRule" :label-width="100">
                <Select v-model="newSupplierProduct.supplier" placeholder="请选择供货商" style="width:200px;margin-left: 100px;">
                <Option v-for="supplier in allSupplierList" :value="supplier.name" :key="supplier.id">
                    {{ supplier.name }}
                </Option>
              </Select>
              <Select v-model="newSupplierProduct.product" placeholder="请选择产品" style="width:200px;margin-left: 100px;">
                <Option v-for="product in allProductList" :value="product.name" :key="product.id">
                    {{ product.name }}
                </Option>
            </Select>
              <FormItem label="单价" prop="price" style="width:200px">
                    <Input v-model="newSupplierProduct.price" placeholder="请输入单价"></Input>
                </FormItem>
            </Form>
            <div slot="footer">
                <Button @click.native="submitAddSupplierProduct" type="primary">确认</Button>
                <Button @click.native="resetAddSupplierProduct" type="text">取消</Button>
            </div>
        </Modal>
      <Modal title="编辑供货记录" v-model="editSupplierFlag"  :styles="{top: '20px'}" width="400">
            <Form ref="newSupplier" :model="selectedSupplier"  :rules="checkRule" :label-width="100">
                 <FormItem label="供货商" prop="name">
                    <Input v-model="selectedSupplier.supplier" :disabled="true" placeholder="请输入供货商名称"></Input>
                </FormItem>
                <FormItem label="商品" prop="coding">
                    <Input v-model="selectedSupplier.product" :disabled="true"  placeholder="请输入商品"></Input>
                </FormItem>
                <FormItem label="单价" prop="price">
                    <Input v-model="selectedSupplier.price" placeholder="请输入供货商电话"></Input>
                </FormItem>
            </Form>
            <div slot="footer">
                <Button @click.native="submitEditSupplier" type="primary">确认</Button>
                <Button @click.native="resetEditSupplier" type="text">取消</Button>
            </div>
        </Modal>
      <Modal title="删除商品" v-model="removeProductFlag" :styles="{top: '20px'}" width="400">
        <h1>确定删除商品？</h1>
        <div slot="footer">
                <Button @click.native="submitRemoveSupplierProduct" type="primary">确认</Button>
                <Button @click.native="resetRemoveSupplierProduct" type="text">取消</Button>
            </div>
      </Modal>
    </div>
  <h2 v-else>
    当前用户没有权限浏览本页面
  </h2>
</template>

<script>

export default {
  data () {

    const checkPrice = (rule, value, callback) => {
      const reg = /^(\d+\.\d{1,1}|\d+)$/g;
            if (value === '') {
                console.log("empty")
                callback();
            } else if (reg.test(value)) {
            console.log("pass")
                callback();
            } else {
            console.log("fail")
                callback(new Error('商品单价应为大于零的数字'));
            }
    }

     return {
       supplierTable: [
                {
                    title: '供应商',
                    align: 'center',
                    key: 'supplier',
                    render:(h,{row})=>{
                      return row.supplier.name
                    }
                },
                {
                    title: '地址',
                    align: 'center',
                    key: 'supplier',
                    render:(h,{row})=>{
                      return row.supplier.address
                    }
                },
                {
                    title: '电话',
                    align: 'center',
                    key: 'supplier',
                    render:(h,{row})=>{
                      return row.supplier.phone
                    }
                },
                {
                    title: '商品',
                    align: 'center',
                    key: 'product',
                    render:(h,{row})=>{
                      return row.product.name
                    }
                },
                {
                    title: '价格',
                    align: 'center',
                    key: 'price',
                  sortable: 'true'
                },
                {
                    title: '操作',
                    align: 'center',
                    key: 'action',
                    render: (h, params) => {
                        return h('div',[
                      h('Button', {
                            props: {
                                type: 'warning',
                                size: 'small',
                                icon: 'trash-b'
                            },
                            on: {
                                click: () => {
                                    if (this.canEdit)
                                    {
                                      this.editSupplierFlag = true
                                      let row = this.supplierList[params.index]
                                      this.selectedSupplier.id = row.id
                                      this.selectedSupplier.product = row.product.name
                                      this.selectedSupplier.price = row.price
                                      this.selectedSupplier.supplier = row.supplier.name
                                    } else {
                                      this.$Message.error('当前用户没有编辑供货记录权限');
                                    }
                                }
                            }
                        }, '编辑商品'),
                          h('Button', {
                            props: {
                                type: 'error',
                                size: 'small',
                                icon: 'trash-b'
                            },
                            on: {
                                click: () => {
                                  if (this.canDelete) {

                                    this.removeProductFlag = true
                                    let row = this.supplierList[params.index]
                                    this.selectedSupplier.id = row.id
                                      this.selectedSupplier.product = row.product.name
                                      this.selectedSupplier.price = row.price
                                      this.selectedSupplier.supplier = row.supplier.name
                                        } else {
                                            this.$Message.error('当前用户没有删除供货记录权限');
                                        }
                                }
                            }
                        }, '删除商品')])
                    }
                }
            ],
       supplierList: [],
       addSupplierFlag: false,
       addSupplierProductFlag: false,
       editSupplierFlag: false,
       removeProductFlag: false,
       supplier:'',
       product:'',
       selectedSupplier: {
         id:'',
         product:'',
         price:'',
         supplier: ''
       },
      newSupplierProduct: {
        supplier: '',
        product: '',
        price: ''
      },
       allSupplierList: [],
       allProductList: [],
       checkRule: {
        price: {validator: checkPrice, trigger: 'blur'},
      }
     }
  },
  created: function () {
      this.getAllSupplierPrice()
      this.getAllSupplier()
      this.getAllProduct()
    },
  computed: {
        canEdit: function () {
            if (this.$store.state.currUser.role ==='super_admin' || this.$store.state.currUser.role ==='warehouse_admin') {
                return true;
            } else {
                return false;
            }
        },
        canAdd: function () {
            if (this.$store.state.currUser.role ==='super_admin' || this.$store.state.currUser.role ==='warehouse_admin') {
                return true;
            } else {
                return false;
            }
        },
        canDelete: function () {
            if (this.$store.state.currUser.role ==='super_admin' || this.$store.state.currUser.role ==='warehouse_admin') {
                return true;
            } else {
                return false;
            }
        },
        canView: function () {
            if (this.$store.state.currUser.role ==='super_admin' || this.$store.state.currUser.role ==='warehouse_admin') {
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
    showAddSupplierProductModal(){
      this.addSupplierProductFlag = true;
    },
    showRemoveSupplierModal(){
      this.removeSupplierFlag = true;
    },
    getAllSupplierPrice(){
          this.$http.get('http://127.0.0.1:8000/supplierprice/')
            .then((response) => {
              var res = JSON.parse(response.bodyText)
              console.log(res)
              if (response.status === 200) {
                this.supplierList = res
              } else {
                this.$Message.error('查询失败')
              }
        })
        },
     getAllSupplier(){
          this.$http.get('http://127.0.0.1:8000/supplier/')
            .then((response) => {
              var res = JSON.parse(response.bodyText)
              console.log(res)
              if (response.status === 200) {
                this.allSupplierList = res
              } else {
                this.$Message.error('查询失败')
              }
        })
        },
     getAllProduct(){
          this.$http.get('http://127.0.0.1:8000/products/')
            .then((response) => {
              var res = JSON.parse(response.bodyText)
              console.log(res)
              if (response.status === 200) {
                this.allProductList = res
              } else {
                this.$Message.error('查询失败')
              }
        })
        },
    submitAddSupplierProduct(){
      this.$http.put('http://127.0.0.1:8000/supplierprice/', this.newSupplierProduct)
            .then((response) => {
                this.$Message.success('添加成功')
              this.getAllSupplierPrice()
        }, response => {
              if(response.status === 403){
                this.$Message.error('记录已存在，请使用编辑功能')
              } else{
                this.$Message.error('添加失败')
              }
            })
      this.addSupplierProductFlag = false
      this.product = ''
      this.supplier = ''
    },
    resetAddSupplierProduct(){
      this.newSupplier = {
        supplier: '',
        product: '',
        price: ''
       },
       this.addSupplierProductFlag = false
    },
    submitEditSupplier(){
      this.$http.post('http://127.0.0.1:8000/supplierprice/', this.selectedSupplier)
            .then((response) => {
                this.$Message.success('更新成功')
              this.getAllSupplierPrice()
        }, reason => {this.$Message.error('更新失败')})
      this.selectedSupplier = {
         id:'',
         product:'',
         price:'',
         supplier: ''
       }
      this.editSupplierFlag = false
      this.product = ''
      this.supplier = ''
    },
    resetEditSupplier(){
      this.selectedSupplier = {
         id:'',
         product:'',
         price:'',
         supplier: ''
       }
      this.editSupplierFlag = false
    },
    submitRemoveSupplierProduct(){

      this.$http.post('http://127.0.0.1:8000/supplierprice/remove',this.selectedSupplier)
            .then((response) => {
                this.$Message.success('删除成功')
              this.getAllSupplierPrice()
        },reason => {this.$Message.error('删除失败')})
      this.selectedSupplier = {
         id:'',
         product:'',
         price:'',
         supplier: ''
       }
      this.removeProductFlag = false
      this.product = ''
      this.supplier = ''
    },
    resetRemoveSupplierProduct(){
       this.selectedSupplier = {
         id:'',
         product:'',
         price:'',
         supplier: ''
       }
      this.removeProductFlag = false
    },
    searchSupplierPrice(){
      console.log(this.supplier)
      console.log(this.product)
      let param = {};
      if(this.supplier != ''){
        param['supplier'] = this.supplier
      }
      if(this.product != ''){
        param['product'] = this.product
      }

      this.$http.get('http://127.0.0.1:8000/supplierprice/',{params:param})
            .then((response) => {
              var res = JSON.parse(response.bodyText)
              console.log(res)
              if (response.status === 200) {
                this.supplierList = res
              } else {
                this.$Message.error('查询失败')
              }
        })
    }
  }
}
</script>

<style>

    .add-supplier {
        padding: 10px;
    }

    .search-box {
        padding: 10px;
        display: flex;
        justify-content: left;
        align-items: center;
    }
    .search-box>div {
        margin-right: 2em;
    }


</style>
