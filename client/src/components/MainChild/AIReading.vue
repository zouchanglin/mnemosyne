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
        <span>阅读记单词</span>
      </template>
    </van-nav-bar>

    <word-card :word_id="word_id" @close_word_card="word_id=-1">
    </word-card>
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
      word_id: 0,
      audio: new Audio()
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
