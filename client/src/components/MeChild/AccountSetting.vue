<template>
  <div>
    <van-nav-bar
        title="账户与密码"
        left-text="返回"
        right-text=""
        left-arrow
        @click-left="onClickLeft"
    />
    <van-row>
    </van-row>
    <van-empty description="开发中……" />
  </div>
</template>
<script>
import { Toast, Notify } from 'vant'
export default {
  name: 'AccountSetting',
  data() {
    return {
    }
  },
  setup() {

  },
  created() {
  },
  methods: {
    onClickLeft() {
      this.$router.push('/me')
    }
  }
}
</script>
<style scoped>

</style>
