<template>
  <div>
    <van-sticky>
      <van-search v-model="search_text" placeholder="搜索单词/中文" @input="search_word"/>
    </van-sticky>

    <van-row>
      <div style="height:4px"></div>
    </van-row>
    <van-row>
      <van-list
          :finished="finished"
          finished-text="没有更多了"
          :v-model="loading"
          @load="search_word">
        <van-swipe-cell v-for="(item, index) in list" :key="index" style="height: 100%">
          <template #left>
            <van-button square type="default" text="未学过"  style="height: 100%" @click="add_learn_word(item.id, false)"/>
            <van-button square type="warning" text="已忘记" style="height: 100%" @click="add_killed_word(item.id, false)"/>
          </template>
          <van-cell :border="true" clickable="clickable" @click="click_word(item.id)">
            <template #title>
              <span style="font-size: 18px">{{ item.word }}&emsp;</span><br>
              <span style="font-size: 13px; color: #505050">{{ limitWords(item.trans, 20) }}</span>
            </template>

            <template #right-icon>
              <van-tag plain type="primary" v-for="(tag, index) in item.tags"
                       size="medium"
                       :key="index" style="margin-right: 5px">{{tag}}</van-tag>
            </template>
          </van-cell>
          <template #right>
            <van-button square type="info" text="学过" style="height: 100%" @click="add_learn_word(item.id, true)"/>
            <van-button square type="primary" text="熟练" style="height: 100%" @click="add_killed_word(item.id, true)"/>
          </template>
        </van-swipe-cell>
      </van-list>
    </van-row>
    <word-card :word_id="word_id" @close_word_card="word_id=-1">
    </word-card>
  </div>
</template>
<script>
import { Toast } from 'vant'
import WordCard from '@/components/ChildComponent/WordCard.vue'
export default {
  name: 'WordList',
  components: { WordCard },
  data() {
    return {
      search_text: '',
      list: [],
      loading: false,
      finished: false,
      audio: new Audio(),
      word_id: 0
    }
  },
  setup() {
  },
  created() {
    this.audio.autoplay = true
  },
  methods: {
    click_word(id) {
      this.word_id = id
    },
    async add_learn_word(id, action) {
      const params = { id: id, action: action }
      const { data: ret } = await this.$http.post('/word/learned', params)
      if (ret.code !== 0) {
        Toast.fail(ret.msg)
        return
      }

      Toast.success({
        message: ret.msg,
        duration: 500
      })
    },
    async add_killed_word(id, action) {
      const params = { id: id, action: action }
      const { data: ret } = await this.$http.post('/word/killed', params)
      if (ret.code !== 0) {
        Toast.fail(ret.msg)
        return
      }
      Toast.success({
        message: ret.msg,
        duration: 500
      })
    },
    async search_word() {
      console.log(this.list.length)
      this.loading = true
      const params = {
        content: this.search_text,
        limit: 20,
        offset: this.list.length
      }
      console.log(params)
      const { data: ret } = await this.$http.post('/word/search', params)
      console.log('login -> ret', ret)
      if (ret.code !== 0) {
        console.log('请求发生错误!')
        return
      }

      if (this.search_text.length === 0) {
        this.list.push(...ret.data.list)
      } else {
        this.list = ret.data.list
      }

      this.loading = false
    },
    onClickLeft() {
      this.$router.push('/home')
    },
    limitWords(txt, length) {
      let str = txt
      if (txt.length <= length) {
        return txt
      } else {
        str = str.substr(0, length) + '..'
        return str
      }
    }
  }
}
</script>
<style scoped>

</style>
