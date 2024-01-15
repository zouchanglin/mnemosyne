<template>
  <div @touchmove.prevent @mousewheel.prevent>
    <van-nav-bar
        left-text=""
        right-text=""
        fixed="fixed"
        :placeholder="false"
        :left-arrow="false"
        :safe-area-inset-top="true"
    >
      <template #title>
        <span style="color: white"></span>
      </template>
    </van-nav-bar>
    <div style="width: 100vw; height: 46px"/>
    <van-row>
      <van-col span="6"></van-col>
      <van-col span="12" style="text-align: center">
        <van-image
            round
            width="8rem"
            height="8rem"
            src="https://img.zouchanglin.cn/website-logo.png"
        />
        <van-icon name="guide-o" />
        <div style="height: 50px; text-align: center; margin-top: 10px">
          <span style="color: #525252"> {{nickname}}</span>
        </div>
      </van-col>
      <van-col span="6"></van-col>
    </van-row>

    <van-row>
      <van-cell-group inset>
        <van-cell title="账户设置" is-link to="account-setting" :value="this.email"/>
      </van-cell-group>
      <van-cell-group inset>
        <van-cell title="学习日历" is-link to="calendar"/>
      </van-cell-group>
    </van-row>
  </div>
</template>
<script>

export default {
  name: 'Me',
  data() {
    return {
      nickname: '',
      email: ''
    }
  },
  setup() {

  },
  created() {
    this.nickname = window.localStorage.getItem('nickname')
    this.email = window.localStorage.getItem('email')
  },
  methods: {}
}
</script>
<style scoped>

</style>
