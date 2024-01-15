<template>
    <div>
      <van-popup v-model="show"
                 style="border-radius: 10px; width: 90vw; height: 40vh">
        <van-cell-group inset style="margin-top: 10px">
          <van-cell :title="word_detail.word">
            <template #label>
              <div style="width: 80%">{{truncatedText(word_detail.trans)}}</div>
            </template>
            <template #default>
              <van-button type="default" icon="volume" @click="playWord(word_detail.word)">发音</van-button>
            </template>
          </van-cell>
          <van-divider>以下为关联词</van-divider>
          <van-cell v-for="(item, index) in vector_link_words" :key="index"
                    :title="item.word" :label="truncatedText(item.trans, 20)">
            <template #default>
              <van-button type="default" icon="volume" @click="playWord(item.word)">发音</van-button>
            </template>
          </van-cell>
        </van-cell-group>
      </van-popup>
    </div>
</template>

<script>
import { Toast } from 'vant'

export default {
  name: 'WordCard',
  setup() {

  },
  data() {
    return {
      loading: false,
      finished: false,
      word_url: '',
      show: false,
      audio: new Audio(),
      word_detail: {
        id: -1,
        word: '',
        trans: ''
      },
      // 向量关联词
      vector_link_words: []
    }
  },
  created() {
    this.audio.autoplay = true
  },
  watch: {
    word(newVal) {
      if (newVal === '') {
        this.show = false
        return
      }
      this.get_word_detail(newVal)
      this.show = true
    }
  },
  methods: {
    async playWord(word) {
      this.audio.src = 'https://dict.youdao.com/dictvoice?audio=' + word + '&type=2'
      await this.audio.play()
    },
    async get_vector_word() {
      // 只搜索这一个
      const params = {
        word: this.word
      }
      const { data: ret } = await this.$http.post('/vector/search', params)
      if (ret.code !== 0) {
        Toast.fail(ret.msg)
        return
      }
      console.log(ret.data)
      this.vector_link_words = ret.data
      this.finished = true
    },
    async get_word_detail(txt) {
      const params = { word: txt }
      const { data: ret } = await this.$http.post('/word/get', params)
      if (ret.code !== 0) {
        Toast.fail(ret.msg)
        return
      }
      console.log(ret.data)
      // 展示单词详情页
      this.word_detail = ret.data
      this.audio.src = 'https://dict.youdao.com/dictvoice?audio=' + ret.data.word + '&type=2'
      await this.audio.play()
      await this.get_vector_word()
    },
    truncatedText(text, maxLength = 16) {
      if (text.length > maxLength) {
        return text.substring(0, maxLength) + '...'
      }
      return text
    }
  },
  props: {
    word: {
      type: String,
      required: true
    }
  }
}
</script>
<style scoped>
.van-overlay {
  z-index: 8;
}
</style>
