<template>
    <div class="person-list" v-if="canView">
        <div class="add-supplier">
            <Button @click.native="showAddSupplierModal" type="primary" icon="person-add">添加供货商</Button>
        </div>
       <div class="supplier-list">
            <Table class="table" style="width:100%" :columns="supplierTable" :data="supplierList"></Table>
        </div>
       <Modal title="添加供货商" v-model="addSupplierFlag" :styles="{top: '20px'}" width="400">
            <Form ref="newSupplier" :model="newSupplier"  :label-width="100">
                <FormItem label="名称" prop="name">
                    <Input v-model="newSupplier.name" placeholder="请输入供货商名称"></Input>
                </FormItem>
                <FormItem label="地址" prop="coding">
                    <Input v-model="newSupplier.address" placeholder="请输入供货商地址"></Input>
                </FormItem>
                <FormItem label="电话" prop="position">
                    <Input v-model="newSupplier.phone" placeholder="请输入供货商电话"></Input>
                </FormItem>
            </Form>
            <div slot="footer">
                <Button @click.native="submitAddSupplier" type="primary">确认</Button>
                <Button @click.native="resetAddSupplier" type="text">重置</Button>
            </div>
        </Modal>
      <Modal title="编辑供货商" v-model="editSupplierFlag" :styles="{top: '20px'}" width="400">
            <Form ref="newSupplier" :model="selectedSupplier"  :label-width="100">
                <FormItem label="名称" prop="name">
                    <Input v-model="selectedSupplier.name" placeholder="请输入供货商名称"></Input>
                </FormItem>
                <FormItem label="地址" prop="coding">
                    <Input v-model="selectedSupplier.address" placeholder="请输入供货商地址"></Input>
                </FormItem>
                <FormItem label="电话" prop="position">
                    <Input v-model="selectedSupplier.phone" placeholder="请输入供货商电话"></Input>
                </FormItem>
            </Form>
            <div slot="footer">
                <Button @click.native="submitEditSupplier" type="primary">确认</Button>
                <Button @click.native="resetEditSupplier" type="text">重置</Button>
            </div>
        </Modal>
      <Modal title="删除供货商" v-model="removeSupplierFlag" :styles="{top: '20px'}" width="400">
        <h1>确定删除供货商？</h1>
        <div slot="footer">
                <Button @click.native="submitRemoveSupplier" type="primary">确认</Button>
                <Button @click.native="resetRemoveSupplier" type="text">取消</Button>
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
       supplierTable: [
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
                                      this.selectedSupplier = this.supplierList[params.index]

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

                                           this.removeSupplierFlag = true
                                           this.selectedSupplier = this.supplierList[params.index]
                                        } else {
                                            this.$Message.error('当前用户没有删除供货记录权限');
                                        }
                                }
                            }
                        }, '删除')])
                    }
                }
            ],
       supplierList: [],
       addSupplierFlag: false,
       removeSupplierFlag: false,
       editSupplierFlag: false,
       newSupplier: {
         name:'',
         address:'',
         phone:''
       },
       selectedSupplier: {
         id:'',
         name:'',
         address:'',
         phone:''
       }
     }
  },
  created: function () {
      this.getAllSupplier()
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
     getAllSupplier(){
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
    submitAddSupplier(){
      this.$http.put('http://127.0.0.1:8000/supplier/', this.newSupplier)
            .then((response) => {
                this.$Message.success('添加成功')
              this.getAllSupplier()
        }, response => {
              this.$Message.error('添加失败')
            })
      this.newSupplier = {
         name:'',
         address:'',
         phone:''
      }
      this.addSupplierFlag = false
      this.getAllSupplier()
    },
    resetAddSupplier(){
      this.newSupplier = {
         name:'',
         address:'',
         phone:''
       }
    },
    submitEditSupplier(){
      this.$http.post('http://127.0.0.1:8000/supplier/', this.selectedSupplier)
            .then((response) => {
                this.$Message.success('更新成功')
              this.getAllSupplier()
        }, reason => {this.$Message.error('更新失败')})
      this.editSupplierFlag = false
      this.selectedSupplier = {
        id:'',
         name:'',
         address:'',
         phone:''
      }
      this.getAllSupplier()
    },
    resetEditSupplier(){
      this.selectedSupplier = {
        id:'',
         name:'',
         address:'',
         phone:''
      }
      this.editSupplierFlag = false
    },
    submitRemoveSupplier(){

      this.$http.post('http://127.0.0.1:8000/supplier/remove',this.selectedSupplier)
            .then((response) => {
                this.$Message.success('删除成功')
              this.getAllSupplier()
        },reason => {this.$Message.error('删除失败')})
      this.removeSupplierFlag = false
      this.selectedSupplier = {
        id:'',
         name:'',
         address:'',
         phone:''
      }
      this.getAllSupplier()
    },
    resetRemoveSupplier(){
       this.selectedSupplier = {
        id:'',
         name:'',
         address:'',
         phone:''
      }
      this.removeSupplierFlag = false
    },

    showAddSupplierModal(){
      if(this.canAdd){
        this.addSupplierFlag = true
      } else {
        this.$Message.error('当前用户没有添加供货记录权限');
      }

    }
  }
}
</script>

<style>

    .add-supplier {
        padding: 10px;
    }

    .button button {
      padding: 10px;
    }


</style>
