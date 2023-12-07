<template>
  <div style="padding: 10px">
    <van-nav-bar
        left-text="返回"
        right-text=""
        left-arrow
        fixed="fixed"
        placeholder="placeholder"
        :safe-area-inset-top="true"
        @click-left="onClickLeft"
        >
      <template #title>
        <span>WordRevise</span>
      </template>
    </van-nav-bar>
    <van-row style="margin-top: 50px">
      <van-col span="4"></van-col>
      <van-col span="16" style="text-align: center">
        <van-circle v-model="currentRate" :rate="100" :speed="25" text="进行中:25%" size="220px"/>
        <van-cell title="" label="正在计算艾宾浩斯数据" style="text-align: center"/>
      </van-col>
      <van-col span="4"></van-col>
    </van-row>
  </div>
</template>
<script>
import { Toast } from 'vant'
import WordCard from '@/components/ChildComponent/WordCard.vue'
export default {
  name: 'WordRevise',
  data() {
    return {
      audio: new Audio(),
        currentRate: 0
    }
  },
  setup() {
  },
  created() {
    this.audio.autoplay = true
      this.get_today_revise_word()
  },
  methods: {
    async get_today_revise_word(){
      // const baseUrl = 'http://127.0.0.1:5005/api/ebbinghaus/revise'
      // this.$sse.create(baseUrl)
      //     .on('ping', (msg) => {
      //         this.ping = JSON.parse(msg)
      //     })
      //     .on('error', (err) => console.error('Failed to parse or lost connection:', err))
      //     .connect()
      //     .catch((err) => console.error('Failed make initial connection:', err))
        const params = { }
        const { data: ret } = await this.$http.post('/ebbinghaus/revise', params)
        if (ret.code !== 0) {
            Toast.fail(ret.msg)
        }
        console.log(ret.data)
    },
    onClickLeft() {
      this.$router.push('/home')
    }
  }
}
</script>
<style scoped>
.fixed-bottom {
  position: fixed;
  bottom: 0;
  width: 100%;
  margin-bottom: 80px;
}
</style>
