<template>
    <div>
<!--        <van-overlay :show="show" @click="show = false" :lock-scroll="false">-->
<!--            <div class="wrapper" @click.stop>-->
<!--                <div class="block">-->
<!--                    &lt;!&ndash; 两端对齐 &ndash;&gt;-->
<!--                    <van-row type="flex" justify="space-between">-->
<!--                        <van-col span="3"></van-col>-->
<!--                        <van-col span="18" style="text-align: center; margin-top: 10px">-->
<!--                            <span style="font-size: 24px;">{{ word_detail.word }}</span>-->
<!--                        </van-col>-->
<!--                        <van-col span="3" style="text-align: right">-->
<!--                            <van-icon name="close" size="30" @click="show = false"-->
<!--                                      style="margin-right: 10px; margin-top: 10px"/>-->
<!--                        </van-col>-->
<!--                    </van-row>-->
<!--                    <van-row style="text-align: center; margin-top: 10px; margin-left: 10px; margin-right: 10px;">-->
<!--                    <span style="font-size: 14px; color: #505050; overflow: hidden; text-overflow: ellipsis">{{-->
<!--                        this.truncatedText(word_detail.trans)-->
<!--                    }}</span>-->
<!--                        <van-divider/>-->
<!--                    </van-row>-->
<!--                    <van-row>-->
<!--                        <van-tabs v-model="activeName" ref="tabs">-->
<!--                            <van-tab title="网络释义" name="youdao">-->
<!--&lt;!&ndash;                                <iframe :src="word_url" style="border: 0; width: 100%; height: 30vh">&ndash;&gt;-->
<!--&lt;!&ndash;                                </iframe>&ndash;&gt;-->
<!--                            </van-tab>-->
<!--                            <van-tab title="语意关联词" name="word">-->
<!--                                <van-list-->
<!--                                    style="overflow: auto; margin-left: 10px; margin-right: 10px"-->
<!--                                    v-model="loading"-->
<!--                                    :finished="finished"-->
<!--                                    finished-text="没有更多了"-->
<!--                                >-->
<!--                                    <van-cell v-for="w in vector_link_words" :key="w.id" :title="w.word"-->
<!--                                              :label="w.trans"-->
<!--                                              @click="get_word_detail(w.word)"/>-->
<!--                                </van-list>-->
<!--                            </van-tab>-->
<!--                        </van-tabs>-->
<!--                    </van-row>-->
<!--                    <van-row style="padding-bottom: 50px">-->
<!--                        <van-grid clickable :column-num="3">-->
<!--                            <van-grid-item text="加入生词本" icon="like-o" @click="start"/>-->
<!--                            <van-grid-item text="近期复习" icon="fire-o" @click="pause"/>-->
<!--                            <van-grid-item text="非常熟悉" icon="passed" @click="reset"/>-->
<!--                        </van-grid>-->
<!--                    </van-row>-->
<!--                </div>-->
<!--            </div>-->
<!--        </van-overlay>-->
      <van-popup v-model="show">
        <div style="width: 90vw; border: #525252;">
          <van-row type="flex" justify="space-between">
            <van-col span="3"></van-col>
            <van-col span="18" style="text-align: center; margin-top: 10px">
              <span style="font-size: 24px;">{{ word_detail.word }}</span>
            </van-col>
            <van-col span="3" style="text-align: right">
              <van-icon name="close" size="30" @click="show = false"
                        style="margin-right: 10px; margin-top: 10px"/>
            </van-col>

          </van-row>
        </div>
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
      activeName: 'youdao',
      show: false,
      audio: new Audio(),
      word_detail: {
        id: -1,
        word: '',
        trans: ''
      },
      height: '28%',
      vector_words_height: '0px',
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
      this.$refs.tabs.resize()
    }
  },
  methods: {
    async get_vector_word() {
      console.log('get_vector_word')
      this.height = '75%'
      this.vector_words_height = '50px'
      // 只搜索这一个
      const params = {
        word_ids: [this.word_id],
        search_limit: 6,
        search_by_embeddings: true
      }
      const { data: ret } = await this.$http.post('/vector/search', params)
      if (ret.code !== 0) {
        Toast.fail(ret.msg)
        return
      }
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
      this.word_url = 'https://youdao.com/result?word=' + this.word_detail.word + '&lang=en'
      await this.audio.play()
      // await this.get_vector_word()
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
.child {
  width: 50px;
  height: 35px;
  background: #d0d0d0;
  border-radius: 4px;
}

.block {
  width: 90%;
  height: 450px;
  background-color: #fff;
  border-radius: 10px;
}

.wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.van-overlay {
  z-index: 8;
}

</style>
