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
        <span>AI Reading</span>
      </template>
    </van-nav-bar>

    <van-row>
      <van-steps direction="vertical" :active="step_active">
        <van-step>
          <p>检查向量词库</p>
        </van-step>
        <van-step>
          <p>检查网络连接</p>
        </van-step>
        <van-step>
          <p>已学词汇查询</p>
        </van-step>
        <van-step>
          <p>艾宾浩斯规则过滤</p>
        </van-step>
        <van-step>
          <p>开始生成内容</p>
        </van-step>
      </van-steps>
    </van-row>
    <van-row>

    </van-row>
    <van-row class="fixed-bottom">
      <van-col span="4"></van-col>
      <van-col span="16">
        <van-circle v-model="currentRate" :rate="85" :speed="100" text="进行中:85%" size="220px"/>
      </van-col>
      <van-col span="4"></van-col>
    </van-row>

    <van-popup v-model="word_card_show" position="bottom" :style="{ height: '35%' }" style="text-align: center;">
      <word-card :word_detail="word_detail">
      </word-card>
    </van-popup>
  </div>
</template>
<script>
import { Toast } from 'vant'
import WordCard from '@/components/ChildComponent/WordCard.vue'
export default {
  name: 'AIReading',
  components: { WordCard },
  data() {
    return {
      word_card_show: false,
      audio: new Audio(),
      word_detail: {},
      step_active: 0,
      step_show: true,
      currentRate: 0
    }
  },
  setup() {
  },
  created() {
    this.audio.autoplay = true
  },
  methods: {
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
