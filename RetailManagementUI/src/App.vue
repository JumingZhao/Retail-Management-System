<template>
    <div id="app">
      <v-header></v-header>
      <div class="main">
        <v-aside></v-aside>
        <div class="mian-right">
          <router-view></router-view>
        </div>
      </div>
      <v-footer></v-footer>
    </div>
</template>

<script>

import vHeader from './components/vHeader'
import vAside from './components/vAside'
import vFooter from './components/vFooter'

// 引入IndexedDB
import IndexedDB from './indexedDB/IndexedDB'

export default {
  name: 'app',
  components: {
    vHeader,
    vFooter,
    vAside,
  },
  data () {
    return {
      //
    }
  },
  created: function () {
  }
}
</script>

<style>
html, body, #app {
  height: 100%;
  min-width: 992px;
}
.main {
  height: calc(100% - 80px);
  display: flex;
}
.mian-right {
  width: calc(100% - 200px);
  height: 100%;
  background-color: #f8f8f9;
  padding: 0 10px;
  overflow-y: scroll;
}
</style>
