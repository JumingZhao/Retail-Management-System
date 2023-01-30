<template>
    <div class="person-list" v-if="canView">
        <div class="add-warehouse">
            <Button @click.native="showAddWarehouseModal" type="primary" icon="person-add">添加新仓库</Button>
        </div>
       <div class="warehouse-list">
            <Table class="table" style="width:100%" :columns="warehouseTable" :data="warehouseList"></Table>
        </div>
       <Modal title="添加仓库" v-model="addWarehouseFlag" :styles="{top: '20px'}" width="400">
            <Form ref="newWarehouse" :model="newWarehouse"  :label-width="100">
                <FormItem label="地址" prop="name">
                    <Input v-model="newWarehouse.address" placeholder="请输入仓库地址"></Input>
                </FormItem>
            </Form>
            <div slot="footer">
                <Button @click.native="submitAddWarehouse" type="primary">确认</Button>
                <Button @click.native="resetAddWarehouse" type="text">重置</Button>
            </div>
        </Modal>
      <Modal title="编辑仓库" v-model="editWarehouseFlag" :styles="{top: '20px'}" width="400">
            <Form ref="newWarehouse" :model="selectedWarehouse"  :label-width="100">
                <FormItem label="名称" prop="name">
                    <Input v-model="selectedWarehouse.address" placeholder="请输入仓库姓名"></Input>
                </FormItem>
            </Form>
            <div slot="footer">
                <Button @click.native="submitEditWarehouse" type="primary">确认</Button>
                <Button @click.native="resetEditWarehouse" type="text">取消</Button>
            </div>
        </Modal>
      <Modal title="删除仓库" v-model="removeWarehouseFlag" :styles="{top: '20px'}" width="400">
        <h1>确定删除仓库？</h1>
        <div slot="footer">
                <Button @click.native="submitRemoveWarehouse" type="primary">确认</Button>
                <Button @click.native="resetRemoveWarehouse" type="text">取消</Button>
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
     return {
       warehouseTable: [
                {
                    title: '地址',
                    align: 'center',
                    key: 'address'
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
                                    if (this.canEdit) {

                                           this.editWarehouseFlag = true
                                            this.selectedWarehouse = this.warehouseList[params.index]
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

                                           this.removeWarehouseFlag = true
                                            this.selectedWarehouse = this.warehouseList[params.index]
                                        } else {
                                            this.$Message.error('当前用户没有删除仓库权限');
                                        }
                                }
                            }
                        }, '删除')])
                    }
                }
            ],
       warehouseList: [],
       addWarehouseFlag: false,
       editWarehouseFlag: false,
       removeWarehouseFlag: false,
       newWarehouse: {
         address:''
       },
       selectedWarehouse: {
         id:'',
         address:''
       }
     }
  },
  created: function () {
      this.getAllWarehouses()
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
    getAllWarehouses(){
          this.$http.get('http://127.0.0.1:8000/warehouse/')
            .then((response) => {
              var res = JSON.parse(response.bodyText)
              console.log(res)
              if (response.status === 200) {
                this.warehouseList = res
              } else {
                this.$Message.error('查询失败')
              }
        })
        },
    submitAddWarehouse(){
      this.$http.put('http://127.0.0.1:8000/warehouse/', this.newWarehouse)
            .then((response) => {
                this.$Message.success('添加成功')
              this.getAllWarehouses()
        }, response => {
              this.$Message.error('添加失败')
            })
      this.addWarehouseFlag = false
      this.getAllWarehouses()
    },
    resetAddWarehouse(){
      this.newWarehouse = {
         address:''
       }
    },
    submitEditWarehouse(){
      this.$http.post('http://127.0.0.1:8000/warehouse/', this.selectedWarehouse)
            .then((response) => {
                this.$Message.success('更新成功')
              this.getAllWarehouses()
        }, reason => {this.$Message.error('更新失败')})
      this.editWarehouseFlag = false
      this.selectedWarehouse = {
         id:'',
         address:''
       }
      this.getAllWarehouses()

    },
    resetEditWarehouse(){
      this.selectedWarehouse = {
         name:'',
         sell_price:'',
         category:''
       }
      this.editWarehouseFlag = false
    },
    submitRemoveWarehouse(){

      this.$http.post('http://127.0.0.1:8000/warehouse/remove',this.selectedWarehouse)
            .then((response) => {
                this.$Message.success('删除成功')
              this.getAllWarehouses()
        },reason => {this.$Message.error('删除失败')})
      this.removeWarehouseFlag = false
      this.selectedWarehouse = {
         id:'',
         address:''
       }
      this.getAllWarehouses()
    },
    resetRemoveWarehouse(){
      this.selectedWarehouse = {
         name:'',
         sell_price:'',
         category:''
       }
      this.editWarehouseFlag = false
    },
    showAddWarehouseModal(){
      if(this.canAdd){
        this.addWarehouseFlag = true
      } else {
        this.$Message.error('当前用户没有添加仓库权限');
      }

    }
  }
}
</script>

<style>

    .add-warehouse {
        padding: 10px;
    }

    .table table {
	  width: 100% !important;
  }
    .button button {
      padding: 10px;
    }


</style>
