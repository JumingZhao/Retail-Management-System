<template>
  <div>
    <Menu theme="dark" class="aside" active-name="goods-list" @on-select="changeMenuItem" width="200px" accordion>
      <MenuItem name='person' class="person">
        <div class="account">
          <Avatar :src="this.$store.state.currUser.avatar" icon="person" size="large"/>
          <p>{{ this.$store.state.currUser.name }}</p>
        </div>
        <div v-if="currUserFlag" class="change-account">
          <Button @click.native="logoutAccount" type="primary">退出</Button>
          <Button @click.native="changeAccount" type="primary">切换账号</Button>
        </div>
        <div v-else class="change-account">
          <Button @click.native="changeAccount" type="primary">账号登录</Button>
        </div>
      </MenuItem>
      <MenuItem name="store-management">
        <Icon type="android-list"></Icon>
        门店管理
      </MenuItem>
      <Submenu name="2">
        <template slot="title">
          <Icon type="settings"></Icon>
          仓库管理
        </template>
        <MenuItem name="supplier-management">供应商管理</MenuItem>
        <MenuItem name="supplier-price">供应商价格</MenuItem>
        <MenuItem name="purchase-record">供货订单</MenuItem>
        <MenuItem name="warehouse-management">仓库管理</MenuItem>
        <MenuItem name="warehouse-inventory">库存管理</MenuItem>

      </Submenu>
      <MenuItem name="sales-record">
        <Icon type="android-list"></Icon>
        销售管理
      </MenuItem>
      <MenuItem name="product-management">
        <Icon type="android-list"></Icon>
        商品管理
      </MenuItem>
      <MenuItem name="person-list">
        <Icon type="ios-people"></Icon>
        人员管理
      </MenuItem>
      <Submenu name="3">
        <template slot="title">
          <Icon type="ios-paper"></Icon>
          销售统计
        </template>
        <MenuItem name="sales-chart">总销售额</MenuItem>
        <MenuItem name="monthly-chart">月销售额</MenuItem>
        <MenuItem name="category-chart">商品种类</MenuItem>
      </Submenu>

    </Menu>
    <!-- 登录弹窗 -->
    <Modal title="欢迎登录" class-name="login-in" v-model="loginFlag" ok-text="登录" width="300" :closable="false"
           :mask-closable="false">
      <Form ref="login" :model="user">
        <FormItem prop="coding">
          <Input type="text" v-model="user.username" placeholder="员工工号">
            <Icon type="person" slot="prepend"></Icon>
          </Input>
        </FormItem>
        <FormItem prop="password">
          <Input type="password" v-model="user.password" placeholder="登录密码">
            <Icon type="locked" slot="prepend"></Icon>
          </Input>
        </FormItem>
      </Form>
      <!--<p style="text-align: center;">点击let me in可作为超级管理员登录</p>-->
      <div slot="footer">
        <!--                <Button @click.native="cancelLogin" type="text">取消</Button>-->
        <Button @click.native="loginSubmit" type="primary">确认</Button>
        <!--<Button @click.native="hack" type="text">let me in</Button>-->
        <Button @click.native="register" type="primary">注册</Button>
      </div>
    </Modal>
    <Modal title="注册" v-model="addUserFlag" :styles="{top: '20px'}" width="400">
      <Form ref="newUser" :model="newUser" :rules="checkNewUser" :label-width="100">
        <FormItem label="员工姓名" prop="name">
          <Input v-model="newUser.name" placeholder="请输入员工姓名"></Input>
        </FormItem>
        <FormItem label="用户名" prop="username">
          <Input v-model="newUser.username" placeholder="请输入用户名"></Input>
        </FormItem>
        <FormItem label="密码" prop="password">
          <Input type="password" v-model="newUser.password" placeholder="请输入密码"></Input>
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
  </div>
</template>

<script>

import IndexedDB from '../indexedDB/IndexedDB'

export default {
  data() {
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
      loginFlag: true,
      addUserFlag: false,
      user: {
        id: '',
        username: '',
        name: '',
        password: '',
        role: '',
      },
      newUser: {
        name: '',
        username: '',
        role: '',
        password: '',
        password2: '',
        isGolden: '',
        store: ''
      },
      checkNewUser: {
        password2: {validator: checkPassword2, trigger: 'blur'},
      },
    }
  },
  computed: {
    currUserFlag: function () {
      if (this.$store.state.currUser) {
        return true;
      } else {
        return false;
      }
    }
  },
  methods: {
    // 点击侧边栏
    changeMenuItem(name) {
      switch (name) {
        case 'person':
          // this.loginFlag = true;
          break;
        case 'store-management':
          this.$router.push({
            path: '/storeManagement'
          });
          break;
        case 'supplier-management':
          this.$router.push({
            path: '/supplierManagement'
          });
          break;
        case 'supplier-price':
          this.$router.push({
            path: '/supplierPrice'
          });
          break;
        case 'warehouse-management':
          this.$router.push({
            path: '/warehouseManagement'
          });
          break;
        case 'warehouse-inventory':
          this.$router.push({
            path: '/warehouseInventory'
          });
          break;
        case 'purchase-record':
          this.$router.push({
            path: '/purchaseRecord'
          });
          break;
        case 'sales-record':
          this.$router.push({
            path: '/salesRecord'
          });
          break;
        case 'message-list':
          this.$store.commit('resetMessageNumber');
          let _this = this;
          let vshopDB = null;
          IndexedDB.openDB('vshopDB', 1, vshopDB, {
            name: 'vshop',
            key: 'name'
          }, function (db) {
            let vshopDB = db;
            IndexedDB.putData(vshopDB, 'vshop', [_this.$store.state.messages]);
          });
          this.$router.push({
            path: '/messageList'
          });
          break;
        case 'data-statistics':
          this.$router.push({
            path: '/dataStatistics'
          });
          break;
        case 'person-list':
          this.$router.push({
            path: '/personList'
          });
          break;
        case 'todo-list':
          this.$router.push({
            path: '/todoList'
          });
          break;
        case 'product-management':
          this.$router.push({
            path: '/productManagement'
          });
          break;
        case 'sales-chart':
          this.$router.push({
            path: '/saleschart'
          });
          break;
        case 'monthly-chart':
          this.$router.push({
            path: '/monthlychart'
          });
          break;
        case 'category-chart':
          this.$router.push({
            path: '/categorychart'
          });
          break;
        default:
          break;
      }
    },
    // 提交登录
    loginSubmit() {
      this.$http.post('http://127.0.0.1:8000/login/', this.user)
          .then((response) => {
                this.user = JSON.parse(response.bodyText)
                this.$store.commit('setCurrUser', this.user);
                this.loginFlag = false;
                this.$Message.success('登录成功')
              },
              response => {
                if (response.status === 403) {
                  this.$Message.error('用户名或密码输入错误')
                } else {
                  this.$Message.error('登陆失败')
                }

              })
    },
    // 退出登录
    logoutAccount() {
      this.$Modal.confirm({
        title: '退出账号登录',
        content: '<h3>确认是否退出当前账号？</h3><p>未登录状态操作受限，只可进行基本的查看操作。<p>',
        onOk: () => {
          this.$store.commit('logoutAccount');
          this.$Message.error('当前用户已退出');
        }
      });
    },
    // 切换账号
    changeAccount() {
      this.loginFlag = true;
    },
    hack() {
      this.user.id = 1
      this.user.name = 'Scott'
      this.user.role = 'super_admin'
      this.$store.commit('setCurrUser', this.user)
      this.loginFlag = false
      this.$Message.success('登录成功')

    },
    register() {
      this.addUserFlag = true;
    },
    submitAddUser() {
      this.$http.put('http://127.0.0.1:8000/useradmin/', this.newUser)
          .then((response) => {
                this.$Message.success('注册成功')
                this.user.id = this.newUser.id
                this.user.name = this.newUser.name
                this.user.role = this.newUser.role
                this.$store.commit('setCurrUser', this.user)
                this.loginFlag = false
                this.resetAddUser()
              },
              response => {
                this.$Message.error('注册失败')
              })
      this.addUserFlag = false
    },
    // 重置
    resetAddUser() {
      this.newUser = {
        name: '',
        username: '',
        role: '',
        password: '',
        password2: '',
        isGolden: ''
      }
    },
  }
}

</script>

<style>
.aside {
  height: 100%;
  overflow-y: scroll;
}

.person:hover .change-account {
  display: block;
  display: flex;
  justify-content: center;
  align-items: center;
}

.person .change-account {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0px;
  left: 0px;
  background-color: rgba(73, 80, 96, 0.8);
  display: none;
}

.change-account button {
  margin: 5px;
}

.account {
  display: flex;
  align-items: center;
}

.account p {
  margin-left: 2em;
}

.login-in {

}
</style>
