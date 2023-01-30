<template>
  <div class="person-list">
    <div class="add-store">
      <Button @click.native="showAddStoreModal" type="primary" icon="person-add">添加新门店</Button>
    </div>
    <div class="store-list">
      <Table class="table" style="width:100%" :columns="storeTable" :data="storeList"></Table>
    </div>
    <Modal title="添加门店" v-model="addStoreFlag" :styles="{top: '20px'}" width="400">
      <Form ref="newStore" :model="newStore" :label-width="100">
        <FormItem label="名称" prop="name">
          <Input v-model="newStore.name" placeholder="请输入门店姓名"></Input>
        </FormItem>
        <FormItem label="地址" prop="coding">
          <Input v-model="newStore.address" placeholder="请输入门店地址"></Input>
        </FormItem>
        <FormItem label="电话" prop="position">
          <Input v-model="newStore.phone" placeholder="请输入门店电话"></Input>
        </FormItem>
      </Form>
      <div slot="footer">
        <Button @click.native="submitAddStore" type="primary">确认</Button>
        <Button @click.native="resetAddStore" type="text">重置</Button>
      </div>
    </Modal>
    <Modal title="编辑门店" v-model="editStoreFlag" :styles="{top: '20px'}" width="400">
      <Form ref="newStore" :model="selectedStore" :label-width="100">
        <FormItem label="名称" prop="name">
          <Input v-model="selectedStore.name" placeholder="请输入门店姓名"></Input>
        </FormItem>
        <FormItem label="地址" prop="coding">
          <Input v-model="selectedStore.address" placeholder="请输入门店地址"></Input>
        </FormItem>
        <FormItem label="电话" prop="position">
          <Input v-model="selectedStore.phone" placeholder="请输入门店电话"></Input>
        </FormItem>
      </Form>
      <div slot="footer">
        <Button @click.native="submitEditStore" type="primary">确认</Button>
        <Button @click.native="resetEditStore" type="text">取消</Button>
      </div>
    </Modal>
    <Modal title="删除门店" v-model="removeStoreFlag" :styles="{top: '20px'}" width="400">
      <h1>确定删除门店？</h1>
      <div slot="footer">
        <Button @click.native="submitRemoveStore" type="primary">确认</Button>
        <Button @click.native="resetRemoveStore" type="text">取消</Button>
      </div>
    </Modal>
  </div>
</template>

<script>

export default {
  data() {
    return {
      storeTable: [
        {
          title: '名称',
          align: 'center',
          key: 'name'
        },
        {
          title: '地址',
          align: 'center',
          key: 'address'
        },
        {
          title: '电话',
          align: 'center',
          key: 'phone'
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

                      this.editStoreFlag = true
                      this.selectedStore = this.storeList[params.index]
                    } else {
                      this.$Message.error('当前用户没有编辑门店权限');
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

                      this.removeStoreFlag = true
                      this.selectedStore = this.storeList[params.index]
                    } else {
                      this.$Message.error('当前用户没有删除门店权限');
                    }
                  }
                }
              }, '删除')])
          }
        }
      ],
      storeList: [],
      addStoreFlag: false,
      editStoreFlag: false,
      removeStoreFlag: false,
      newStore: {
        name: '',
        address: '',
        phone: ''
      },
      selectedStore: {
        id: '',
        name: '',
        address: '',
        phone: ''
      }
    }
  },
  created: function () {
    this.getAllstores()
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
    getAllstores() {
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
    submitAddStore() {
      this.$http.put('http://127.0.0.1:8000/store/', this.newStore)
          .then((response) => {
            this.$Message.success('添加成功')
            this.getAllstores()
          }, response => {
            this.$Message.error('添加失败')
          })
      this.addStoreFlag = false
    },
    resetAddStore() {
      this.newstore = {
        name: '',
        sell_price: '',
        category: ''
      }
    },
    submitEditStore() {
      this.$http.post('http://127.0.0.1:8000/store/', this.selectedStore)
          .then((response) => {
            this.$Message.success('更新成功')
            this.getAllstores()
          }, reason => {
            this.$Message.error('更新失败')
          })
      this.editStoreFlag = false
    },
    resetEditStore() {
      this.selectedstore = {
        name: '',
        sell_price: '',
        category: ''
      }
      this.editStoreFlag = false
    },
    submitRemoveStore() {

      this.$http.post('http://127.0.0.1:8000/store/remove', this.selectedStore)
          .then((response) => {
            this.$Message.success('删除成功')
            this.getAllstores()
          }, reason => {
            this.$Message.error('删除失败')
          })
      this.removeStoreFlag = false
    },
    resetRemoveStore() {
      this.selectedstore = {
        name: '',
        sell_price: '',
        category: ''
      }
      this.EditStoreFlag = false
    },
    showAddStoreModal() {
      if (this.canAdd) {
        this.addStoreFlag = true
      } else {
        this.$Message.error('当前用户没有添加门店权限');
      }

    }
  }
}
</script>

<style>

.add-store {
  padding: 10px;
}

.table table {
  width: 100% !important;
}

.button button {
  padding: 10px;
}


</style>
