<template>
  <div class="person-list">
    <div class="add-product">
      <Button @click.native="showAddProductModal" type="primary" icon="person-add">添加新商品</Button>
    </div>
    <div class="search-box">
      <Input v-model="name" placeholder="请输入商品姓名" @keyup.enter.native="searchProduct" ></Input>
      <Input v-model="category" placeholder="请输入商品种类" @keyup.enter.native="searchProduct"></Input>
      <Button @click.native="searchProduct" type="primary" icon="search" style="margin: 5px">搜索</Button>
      <Button @click.native="clearSearch" type="primary" icon="backspace" style="margin: 5px">清除</Button>
    </div>
    <div class="product-list">
      <Table class="table" style="width:100%" :columns="productTable" :data="productList"></Table>
    </div>
    <Modal title="添加商品" v-model="addProductFlag" :styles="{top: '20px'}" width="400">
      <Form ref="newProduct" :model="newProduct" :rules="checkRule" :label-width="100">
        <FormItem label="名称" prop="name">
          <Input v-model="newProduct.name" placeholder="请输入商品姓名"></Input>
        </FormItem>
        <FormItem label="单价" prop="sell_price">
          <Input v-model="newProduct.sell_price" placeholder="请输入商品单价"></Input>
        </FormItem>
        <FormItem label="种类" prop="position">
          <Input v-model="newProduct.category" placeholder="请输入商品种类"></Input>
        </FormItem>
        <FormItem label="规格" prop="position">
          <Input v-model="newProduct.unit" placeholder="请输入商品规格"></Input>
        </FormItem>
      </Form>
      <div slot="footer">
        <Button @click.native="submitAddProduct" type="primary">确认</Button>
        <Button @click.native="resetAddProduct" type="text">重置</Button>
      </div>
    </Modal>
    <Modal title="编辑商品" v-model="editProductFlag" :styles="{top: '20px'}" width="400">
      <Form ref="newProduct" :model="selectedProduct" :rules="checkRule" :label-width="100">
        <FormItem label="名称" prop="name">
          <Input v-model="selectedProduct.name" placeholder="请输入商品姓名"></Input>
        </FormItem>
        <FormItem label="单价" prop="sell_price">
          <Input v-model="selectedProduct.sell_price" placeholder="请输入商品单价"></Input>
        </FormItem>
        <FormItem label="种类" prop="position">
          <Input v-model="selectedProduct.category" placeholder="请输入商品种类"></Input>
        </FormItem>
        <FormItem label="规格" prop="position">
          <Input v-model="selectedProduct.unit" placeholder="请输入商品规格"></Input>
        </FormItem>
      </Form>
      <div slot="footer">
        <Button @click.native="submitEditProduct" type="primary">确认</Button>
        <Button @click.native="resetEditProduct" type="text">取消</Button>
      </div>
    </Modal>
    <Modal title="删除商品" v-model="removeProductFlag" :styles="{top: '20px'}" width="400">
      <h1>确定删除商品？</h1>
      <div slot="footer">
        <Button @click.native="submitRemoveProduct" type="primary">确认</Button>
        <Button @click.native="resetRemoveProduct" type="text">取消</Button>
      </div>
    </Modal>
  </div>
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
    return {
      productTable: [
        {
          title: '名称',
          align: 'center',
          key: 'name'
        },
        {
          title: '单价',
          align: 'center',
          key: 'sell_price',
          sortable: true,
        },
        {
          title: '种类',
          align: 'center',
          key: 'category'
        },
        {
          title: '规格',
          align: 'center',
          key: 'unit'
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

                      this.editProductFlag = true
                      this.selectedProduct = this.productList[params.index]
                    } else {
                      this.$Message.error('当前用户没有编辑商品权限');
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

                      this.removeProductFlag = true
                      this.selectedProduct = this.productList[params.index]
                    } else {
                      this.$Message.error('当前用户没有删除商品权限');
                    }
                  }
                }
              }, '删除')])
          }
        }
      ],
      productList: [],
      addProductFlag: false,
      editProductFlag: false,
      removeProductFlag: false,
      newProduct: {
        name: '',
        sell_price: '',
        category: '',
        unit: '',
      },
      selectedProduct: {
        id: '',
        name: '',
        sell_price: '',
        category: '',
        unit: '',
      },
      name: '',
      category: '',
      checkRule: {
        sell_price: {validator: checkPrice, trigger: 'blur'},
      },
    }
  },
  created: function () {
    this.getAllProducts()
  },
  computed: {
    canEdit: function () {
      if (this.$store.state.currUser.role === 'super_admin') {
        return true;
      } else {
        return false;
      }
    },
    canAdd: function () {
      if (this.$store.state.currUser.role === 'super_admin') {
        return true;
      } else {
        return false;
      }
    },
    canDelete: function () {
      if (this.$store.state.currUser.role === 'super_admin') {
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
    submitAddProduct() {
      this.$http.put('http://127.0.0.1:8000/products/', this.newProduct)
          .then((response) => {
            this.$Message.success('添加成功')
            this.getAllProducts()
          }, response => {
            this.$Message.error('添加失败')
          })
      this.addProductFlag = false
      this.resetAddProduct()
    },
    resetAddProduct() {
      this.newProduct = {
        name: '',
        sell_price: '',
        category: '',
        unit: '',
      }
    },
    submitEditProduct() {
      this.$http.post('http://127.0.0.1:8000/products/', this.selectedProduct)
          .then((response) => {
            this.$Message.success('更新成功')
            this.getAllProducts()
          }, reason => {
            this.$Message.error('更新失败')
          })
      this.editProductFlag = false
      this.resetEditProduct()
    },
    resetEditProduct() {
      this.selectedProduct = {
        name: '',
        sell_price: '',
        category: '',
        unit: '',
      }
      this.editProductFlag = false
    },
    submitRemoveProduct() {

      this.$http.post('http://127.0.0.1:8000/products/remove', this.selectedProduct)
          .then((response) => {
            this.$Message.success('删除成功')
            this.getAllProducts()
          }, reason => {
            this.$Message.error('删除失败')
          })
      this.removeProductFlag = false
    },
    resetRemoveProduct() {
      this.selectedProduct = {
        name: '',
        sell_price: '',
        category: '',
        unit: '',
      }
      this.editProductFlag = false
    },
    showAddProductModal() {
      if (this.canAdd) {
        this.addProductFlag = true
      } else {
        this.$Message.error('当前用户没有添加商品权限');
      }

    },
    searchProduct() {
      let param = {};

      if (this.name !== '') {
        param['product'] = this.name;
      }
      if (this.category !== '') {
        param['category'] = this.category;
      }

      this.$http.get('http://127.0.0.1:8000/products/', {params: param})
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
      this.name = ''
      this.category = ''
      this.getAllProducts()
    }
  }
}
</script>

<style>

.add-product {
  padding: 10px;
}

.table table {
  width: 100% !important;
}

.button button {
  padding: 10px;
}

.search-box {
  padding: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.search-box > div {
  margin-right: 2em;
}

</style>
