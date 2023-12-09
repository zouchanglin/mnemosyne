<template>
    <div>
      <van-overlay :show="show" @click="show = false" :lock-scroll="false">
        <div class="wrapper" @click.stop>
          <div class="block">
            <!-- 两端对齐 -->
            <van-row type="flex" justify="space-between">
              <van-col span="3"></van-col>
              <van-col span="18" style="text-align: center; margin-top: 10px">
                <span style="font-size: 24px;">{{ word_detail.word }}</span>
              </van-col>
              <van-col span="3" style="text-align: right">
                <van-icon name="close" size="30" @click="show = false" style="margin-right: 10px; margin-top: 10px"/>
              </van-col>
            </van-row>
            <van-row style="text-align: center; margin-top: 10px; margin-left: 10px; margin-right: 10px">
              <span style="font-size: 14px; color: #505050;">{{ word_detail.trans }}</span>
              <van-divider />
            </van-row>
            <van-row>
              <van-tabs v-model="activeName" ref="tabs">
                <van-tab title="语意关联词" name="word">
                  <van-list
                      style="overflow: auto; height: 30vh; padding-left: 30px"
                      v-model="loading"
                      :finished="finished"
                      finished-text="没有更多了"
                  >
                    <van-cell v-for="w in vector_link_words" :key="w.id" :title="w.word" :label="w.trans" @click="get_word_detail(w.id)"/>
                  </van-list>
                </van-tab>
                <van-tab title="网络释义" name="youdao">
                  <iframe :src="word_url" style="border: 0; width: 100%; height: 30vh">
                  </iframe>
                </van-tab>
              </van-tabs>
            </van-row>
          </div>
        </div>
      </van-overlay>
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
            activeName: 'word',
            show: false,
            audio: new Audio(),
            word_detail: {
                word: '',
                error_count: 0,
                pitch_count: 0,
                learned: false,
                killed: false,
                usphone: '',
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
        word_id(newVal) {
            if(newVal === -1){
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
                search_limit: 15
            }
            const { data: ret } = await this.$http.post('/vector/search', params)
            if (ret.code !== 0) {
                Toast.fail(ret.msg)
                return
            }
            // console.log('vector->', ret.data)
            // 展示出关联词
            this.vector_link_words = ret.data
            this.finished = true
        },
        async get_word_detail(id) {
            const params = { id: id }
            const { data: ret } = await this.$http.post('/word/detail', params)
            if (ret.code !== 0) {
                Toast.fail(ret.msg)
                return
            }
            // 展示单词详情页
            this.word_detail = ret.data
            if (ret.data.usspeech.length === 0) {
                // 没有发音就手动拼接一个发音
                ret.data.usspeech = ret.data.word + '&type=2'
            } else {
                this.audio.src = 'https://dict.youdao.com/dictvoice?audio=' + ret.data.usspeech
            }
            this.word_url = 'https://youdao.com/result?word=' + this.word_detail.word + '&lang=en'
            await this.audio.play()
            await this.get_vector_word()
        },
        async click_voice() {
            if (this.word_detail.usspeech.length === 0) {
                // 没有发音就手动拼接一个发音
                this.word_detail.usspeech = this.word_detail.word + '&type=2'
            } else {
                this.audio.src = 'https://dict.youdao.com/dictvoice?audio=' + this.word_detail.usspeech
            }
            await this.audio.play()
        }
    },
    props: {
        word_id: {
            type: Number,
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
  width: 80%;
  height: 50vh;
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
