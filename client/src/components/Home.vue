<template>
  <div @touchmove.prevent @mousewheel.prevent>
    <div style="height: 100vh">
      <router-view></router-view>
    </div>
    <van-tabbar v-model="active" route safe-area-inset-bottom>
      <van-tabbar-item name="main" icon="home-o" replace to="/main">主页</van-tabbar-item>
      <van-tabbar-item name="me" icon="contact-o" replace to="/me">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script>
import { ref } from 'vue'
export default {
  name: 'Home',
  setup() {

  },
  data() {
    return {
      active: 'main'
    }
  },
  methods: {

  }
}

</script>

<style scoped>

</style>
