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
  mounted() {
    this.startReading()
  },
  methods: {
    startReading() {
      const baseUrl = process.env.VUE_APP_API_URL + 'article/generate'
      const eventFetch = new FetchEventSource()
      const overItems = []
      eventFetch.stopFetchEvent()
      eventFetch.startFetchEvent(baseUrl, {}, res => {
        // console.log(res, typeof res)  string
        const items = this.decodeSSEString(res)

      }, () => {
        console.log('end')
      }, error => {
        console.log(error, 'error')
      })
    },
    decodeSSEString(sseString){
      // kv list
      const tmpItems = []
      const sseArray = sseString.split('\n')
      let eventV
      let dataV
      sseArray.forEach(function (line) {
        if(line.length > 0){
          console.log('line--->', line)
          const [key, value] = line.split(':')
          console.log(key, value)
          if(key.trim() === 'event') {
            eventV = value.trim()
          } else if(key.trim() === 'data') {
            dataV = value.trim()
          }
          if(eventV && dataV) {
            tmpItems.push({ event: eventV, data: dataV })
            eventV = dataV = null
          }
        }
      })
      return tmpItems
    },
    onClickLeft() {
      this.$router.push('/home')
    }
  }
}

/**
 * FetchEventSource 合并Post请求与Stream响应
 */
class FetchEventSource {
  constructor() {
    this.abortController = new AbortController() || null
  }

  startFetchEvent(url, body, onMessage, onEnd, onError, headers = {}) {
    const fetchOptions = {
      method: 'POST',
      body: body,
      headers: Object.assign({}, {
        'Content-Type': 'application/json',
        Authorization: localStorage.getItem('token')
      }),
      signal: this.abortController.signal
    }
    fetch(url, fetchOptions).then((response) => {
      const reader = response.body.getReader()
      reader.read().then(function processResult(result) {
        if (result.done) {
          onEnd()
          return
        }
        const decoder = new TextDecoder()
        const receivedString = decoder.decode(result.value, { stream: true })
        onMessage(receivedString)
        return reader.read().then(processResult)
      })
      return response
    }).catch(() => {
      this.eventController.abort()
      onError({ code: 201, message: '服务器异常' })
    })
  }

  stopFetchEvent() {
    if (this.eventController) {
      this.eventController.abort()
      this.eventController = null
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
