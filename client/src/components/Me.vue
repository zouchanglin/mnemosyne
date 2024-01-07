<template>
  <div @touchmove.prevent @mousewheel.prevent>
    <van-row>
      <div style="height: 100px; text-align: center">
      </div>
    </van-row>

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
