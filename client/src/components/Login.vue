<template>
  <!-- 页面局中 -->

  <van-form @submit="login" class="login-box" v-model="loginForm">
    <van-cell-group inset>
      <van-field
          v-model="loginForm.email"
          name="email"
          label="Email"
          placeholder="E-Mail"
          type="email"
          :rules="[{ required: true, message: '请填写E-Mail' },
          {}]"
      />
      <van-field
          v-model="loginForm.password"
          type="password"
          name="密码"
          label="密码"
          placeholder="密码"
          :rules="[{ required: true, message: '请填写密码' }]"
      />
    </van-cell-group>
    <div style="margin: 16px;">
      <van-button round block type="primary" native-type="submit">
        提交
      </van-button>
      <van-button round block type="default" style="margin-top: 10px" @click="restLoginForm">重置</van-button>
    </div>
  </van-form>
</template>

<script>
import { Toast, Notify } from 'vant'

export default {
  name: 'Login',
  data() {
    return {
      loginForm: {
        email: '',
        password: ''
      }
    }
  },
  methods: {
    async login() {
      // md5加密处理下
      const params = {
        email: this.loginForm.email,
        password: this.$md5(this.loginForm.password)
      }
      const { data: ret } = await this.$http.post('/auth/login', params)
      console.log('login -> ret', ret)
      if (ret.code !== 0) {
        Notify('登录失败，请检查用户名和密码')
        // Toast.fail('用户名和密码错误')
        return
      }
      Toast.success('登录成功')
      // Notify('登录成功')
      window.localStorage.setItem('token', ret.data.token)
      window.localStorage.setItem('user_name', ret.data.user_name)
      window.localStorage.setItem('user_email', ret.data.user_email)
      await this.$router.push('/home')
    },
    restLoginForm() {
      console.log(this)
      this.loginForm.email = ''
      this.loginForm.password = ''
    }
  }
}
</script>

<style lang="less" scoped>
.login-box {
  align-self: center;
  margin-top: 80px;
}
</style>
