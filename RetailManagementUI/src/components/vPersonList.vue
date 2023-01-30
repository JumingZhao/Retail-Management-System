<template>
    <div class="person-list">
        <div class="add-person">
            <Button @click.native="changeUserFlag" type="primary" icon="person-add">添加新员工</Button>
        </div>
        <div class="person-message">
            <Table :columns="userTable" :data="userList"></Table>
        </div>
        <!-- 添加员工弹窗 -->
        <Modal title="添加员工" v-model="addUserFlag" :styles="{top: '20px'}" width="400">
            <Form ref="newUser" :model="newUser" :rules="checkNewUser" :label-width="100">
                <FormItem label="员工姓名" prop="name">
                    <Input v-model="newUser.name" placeholder="请输入员工姓名"></Input>
                </FormItem>
                <FormItem label="用户名" prop="username">
                    <Input v-model="newUser.username" placeholder="请输入用户名"></Input>
                </FormItem>
                <FormItem label="密码" prop="password">
                    <Input v-model="newUser.password" placeholder="请输入密码"></Input>
                </FormItem>
                <FormItem label="确认密码" prop="password2">
                    <Input type="password" v-model="newUser.password2" placeholder="再次输入密码"></Input>
                </FormItem>
                <FormItem label="权限" prop="role">
                    <Select v-model="newUser.role" placeholder="请设置权限">
                        <Option value="super_admin">超级管理员</Option>
                        <Option value="warehouse_admin">仓库管理员</Option>
                        <Option value="store_manager">门店经理</Option>
                        <Option value="salesperson">销售人员</Option>
                    </Select>
                </FormItem>
                <FormItem label="门店" prop="store" v-if="newUser.role == 'store_manager'">
                    <Input v-model="newUser.store" placeholder="请输入门店"></Input>
                </FormItem>
                <FormItem label="金牌销售" v-if="newUser.role == 'store_manager'">
                      <i-switch v-model="newUser.isGolden" size="large">
                        <span slot="true">Yes</span>
                        <span slot="false">No</span>
                      </i-switch>
                </FormItem>
            </Form>
            <div slot="footer">
                <Button @click.native="submitAddUser" type="primary">确认</Button>
                <Button @click.native="resetAddUser" type="text">重置</Button>
            </div>
        </Modal>
        <!-- 编辑员工弹窗 -->
        <Modal title="编辑员工" v-model="editUserFlag" :styles="{top: '20px'}" width="400">
            <Form ref="newUser" :model="selectedUser" :rules="checkNewUser" :label-width="100">
                <FormItem label="员工姓名" prop="name">
                    <Input v-model="selectedUser.name" placeholder="请输入员工姓名"></Input>
                </FormItem>
                <FormItem label="用户名" prop="username">
                    <Input v-model="selectedUser.username" placeholder="请输入用户名"></Input>
                </FormItem>
                <FormItem label="密码" prop="password">
                    <Input v-model="selectedUser.password" placeholder="请输入密码"></Input>
                </FormItem>
                <FormItem label="确认密码" prop="password2">
                    <Input type="password" v-model="selectedUser.password2" placeholder="再次输入密码"></Input>
                </FormItem>
                <FormItem label="权限" prop="role">
                    <Select v-model="selectedUser.role" placeholder="请设置权限">
                        <Option value="super_admin">超级管理员</Option>
                        <Option value="warehouse_admin">仓库管理员</Option>
                        <Option value="store_manager">门店经理</Option>
                        <Option value="salesperson">销售人员</Option>
                    </Select>
                </FormItem>
                <FormItem label="门店" prop="store" v-if="selectedUser.role == 'store_manager'">
                    <Input v-model="selectedUser.store" placeholder="请输入门店"></Input>
                </FormItem>
                <FormItem label="金牌销售" v-if="selectedUser.role == 'store_manager'">
                      <i-switch v-model="selectedUser.isGolden" size="large">
                        <span slot="true">Yes</span>
                        <span slot="false">No</span>
                      </i-switch>
                </FormItem>
            </Form>
            <div slot="footer">
                <Button @click.native="submitEditUser" type="primary">确认</Button>
                <Button @click.native="resetEditUser" type="text">取消</Button>
            </div>
        </Modal>
        <Modal title="删除用户" v-model="removeUserFlag" :styles="{top: '20px'}" width="400">
          <h1>确定删除用户？</h1>
          <div slot="footer">
                  <Button @click.native="submitRemoveUser" type="primary">确认</Button>
                  <Button @click.native="resetRemoveUser" type="text">取消</Button>
              </div>
        </Modal>
    </div>
</template>

<script>

import IndexedDB from '../indexedDB/IndexedDB'

export default {
    data () {
        // 检查员工工号
        const checkUserCoding = (rule, value, callback) => {
            const reg = /^[0-9]\d*$/g;
            if (value === '') {
                callback(new Error('请设置员工工号作为登录账号'));
            } else {
                if (reg.test(value)) {
                    const users = this.$store.state.users.userList;
                    for (let i = 0, len = users.length; i < len; i++) {
                        if (users[i].coding === value) {
                            callback(new Error('员工工号已存在，请重新设置'));
                        }
                    }
                    callback();
                } else {
                    callback(new Error('员工工号为数字'));
                }
            }
        }
        // 检查重复密码
        const checkPassword2 = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请再次确认登录密码'));
            } else {
                if (value === this.newUser.password) {
                    callback();
                } else {
                    callback(new Error('两次输入密码不一致'));
                }
            }
        }
        return {
            addUserFlag: false,
            editUserFlag: false,
            removeUserFlag: false,
            newUser: {
                name: '',
                username: '',
                role: '',
                password: '',
                password2: '',
                isGolden: '',
                store: ''
            },
            selectedUser: {
                id: '',
                name: '',
                username: '',
                role: '',
                password: '',
                password2: '',
                isGolden: '',
                store: ''
            },
            checkNewUser: {
              password2: { validator: checkPassword2, trigger: 'blur' },
            },
            // 表格设置
            userTable: [
                {
                    title: '姓名',
                    align: 'center',
                    key: 'name'
                },
                {
                    title: '用户名',
                    align: 'center',
                    key: 'username'
                },
                {
                    title: '权限',
                    align: 'center',
                    key: 'role'
                },
                {
                    title: '金牌销售',
                    align: 'center',
                    key: 'salesmanager',
                    render:(h,params)=>{
                      if( params.row.salesmanager ===null || params.row.salesmanager.isGolden === false){
                        return 'false'
                      } else {
                        return 'true'
                      }
                    }
                },
                {
                    title: '门店',
                    align: 'center',
                    key: 'salesmanager',
                    render:(h,{row})=>{
                    if( row.salesmanager === null ){
                        return ''
                      } else {
                        return row.salesmanager.store.name
                      }}
                },
                {
                    title: '操作',
                    align: 'center',
                    key: 'action',
                    render: (h, params) => {
                        return h('div',[h('Button', {
                            props: {
                                type: 'warning',
                                size: 'small',
                                icon: 'trash-b'
                            },
                            on: {
                                click: () => {
                                  let user = this.userList[params.index]
                                  if (this.$store.state.currUser.role  === 'super_admin' || this.$store.state.currUser.id === user.id) {
                                    this.selectedUser.id = user.id
                                    this.selectedUser.name = user.name
                                    this.selectedUser.username = user.username
                                    this.selectedUser.role = user.role
                                    this.selectedUser.password = user.password
                                    this.selectedUser.password2 = user.passowrd
                                    if(user.salesmanager !== null){
                                      this.selectedUser.isGolden = user.salesmanager.isGolden
                                      this.selectedUser.store = user.salesmanager.store.name
                                    }
                                    this.showEditModal();
                                  } else {
                                    this.$Message.error('当前用户没有权限编辑其他用户信息');
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

                                        if (this.$store.state.currUser.role  === 'super_admin') {
                                            let user = this.userList[params.index]
                                            this.selectedUser.id = user.id
                                            this.selectedUser.name = user.name
                                            this.selectedUser.username = user.username
                                            this.selectedUser.role = user.role
                                            this.selectedUser.password = user.password
                                            this.selectedUser.password2 = user.passowrd
                                            if(user.salesmanager !== null){
                                              this.selectedUser.isGolden = user.salesmanager.isGolden
                                              this.selectedUser.store = user.salesmanager.store.name
                                            }
                                            this.removeUserFlag = true
                                        } else {
                                            this.$Message.error('当前用户没有删除员工权限');
                                        }

                                }
                            }
                        }, '删除')])
                    }
                }
            ],
            userList: []
        }
    },
  created() {
      this.init()
      this.getAllUsers()
  },
  computed: {
        canEdit: function () {
            if (this.$store.state.currUser.role ==='super_admin') {
                return true;
            } else {
                return false;
            }
        },
        canAdd: function () {
            if (this.$store.state.currUser.role ==='super_admin') {
                return true;
            } else {
                return false;
            }
        },
        isSuperUser: function () {
            if (this.$store.state.currUser.role ==='super_admin') {
                return true;
            } else {
                return false;
            }
        },
        currRole: function () {
              return this.$store.state.currUser.role
          },
        canView: function (){
          if (this.$store.state.currUser.role ==='super_admin' || this.$store.state.currUser.role ==='store_manager') {
                return true;
            } else {
                return false;
            }
        }

    },
  methods: {
      init(){
        if(this.isSuperUser){
          this.userTable.splice(2,0,{
                    title: '密码',
                    align: 'center',
                    key: 'password'
                },)
        }

      },
        changeUserFlag () {
          if(this.canAdd){
            this.addUserFlag = true;
          } else {
            this.$Message.error('当前用户没有权限添加用户')
          }
        },
        showEditModal () {
            this.editUserFlag = true;
        },
        // 提交新用户
        submitAddUser () {
          this.$http.put('http://127.0.0.1:8000/useradmin/', this.newUser)
            .then((response) => {
              this.$Message.success('添加成功')
              this.getAllUsers()},
              response => {
                  this.$Message.error('添加失败')
                })
          this.addUserFlag = false
        },
        // 重置
        resetAddUser () {
            this.newUser =  {
                name: '',
                username: '',
                role: '',
                password: '',
                password2: '',
                isGolden: ''
            }
        },
        submitEditUser () {
            this.$http.post('http://127.0.0.1:8000/useradmin/', this.selectedUser)
            .then((response) => {
              this.$Message.success('编辑成功')
              this.getAllUsers()},
              response => {
                  this.$Message.error('编辑失败')
                })
          this.editUserFlag = false
        },
        // 重置
        resetEditUser () {
            this.selectedUser =  {
                id: '',
                name: '',
                username: '',
                role: '',
                password: '',
                password2: '',
                isGolden: ''
            }
            this.editUserFlag = false
        },
        submitRemoveUser () {
            this.$http.post('http://127.0.0.1:8000/useradmin/remove', this.selectedUser)
            .then((response) => {
              this.$Message.success('删除成功')
              this.getAllUsers()},
              response => {
                  this.$Message.error('删除失败')
                })
          this.removeUserFlag = false
        },
        // 重置
        resetRemoveUser () {
            this.selectedUser =  {
                id: '',
                name: '',
                username: '',
                role: '',
                password: '',
                password2: '',
                isGolden: ''
            }
            this.removeUserFlag = false
        },
        getAllUsers () {
          if(!this.canView){
            let param = {}
            param['id'] = this.$store.state.currUser.id
            this.$http.get('http://127.0.0.1:8000/useradmin/',{params:param})
            .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (response.status === 200) {
                this.userList = res
              } else {
                this.$Message.error('查询失败')
              }})
          }else{
            this.$http.get('http://127.0.0.1:8000/useradmin/')
            .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (response.status === 200) {
                this.userList = res
              } else {
                this.$Message.error('查询失败')
              }})
          }

        }
    }
}
</script>

<style scoped>
    .add-person {
        padding: 10px;
    }
    .img-place {
        width: 200px;
        height: 200px;
        margin-top: 10px;
        border: 1px dashed #dddee1;
    }
    .img-place img {
        width: 100%;
        height: 100%;
    }
</style>
