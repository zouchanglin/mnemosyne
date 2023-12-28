<template>
  <!-- 页面局中 -->
  <div class="fullscreen-container">
    <van-form @submit="login" v-model="loginForm" style="width: 90%">
        <van-field
            v-model="loginForm.email"
            name="email"
            label="Email"
            placeholder="E-Mail"
            type="email"
            :rules="[{ required: true, message: '请填写E-Mail' }]"
        />
        <van-field
            v-model="loginForm.password"
            type="password"
            name="Password"
            label="Password"
            placeholder="密码"
            :rules="[{ required: true, message: '请填写密码' }]"
        />
      <van-button round block type="primary" native-type="submit">
        提交
      </van-button>
      <van-button round block type="default" style="margin-top: 10px" @click="restLoginForm">重置</van-button>
    </van-form>
  </div>

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
        // Notify('登录失败，请检查用户名和密码')
        Toast.fail('登录失败')
        return
      }
      Toast.success('登录成功')
      window.localStorage.setItem('token', ret.data.token)
      window.localStorage.setItem('email', ret.data.email)
      window.localStorage.setItem('nickname', ret.data.nickname)
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
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

.fullscreen-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>
