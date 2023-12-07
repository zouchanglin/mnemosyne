<template>
  <div>
    <div>
      <router-view></router-view>
    </div>
    <van-tabbar v-model="active" route>
      <van-tabbar-item name="words" icon="label-o" replace to="/word-list">单词</van-tabbar-item>
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
