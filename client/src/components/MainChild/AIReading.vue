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

    <div class="container" @click="clickWord($event)" v-html="chContentSpan"></div>

    <word-card :word="word_txt" @close_word_card="word_txt=''">
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
      word_txt: '',
      audio: new Audio(),
      chContent: 'The philosophy of life is to find meaning in every substantial moment, but sometimes anxiety can stir in the chamber of our minds, making concentration difficult. There is controversy over what should constitute a true alliance, and some may pant for an incentive to join. However, any assault on our reservation can violate our trust and portray an ally in a negative light. It\'s important to incorporate good tactics and gear up for any word or penalty that may come our way. Just like a priest in battle, we must be ready to defend our beliefs and stand firm in our convictions.',
      chContentSpan: 'AAA'
    }
  },
  setup() {
  },
  created() {
    this.audio.autoplay = true
  },
  mounted() {
    // this.startReading()
    this.chContentSpan = this.addElementSpan(this.chContent)
    console.log(this.chContentSpan)
  },
  methods: {
    clickWord(event) {
      if(event.target.innerText.length < 50){
        console.log(event.target.innerText)
        this.word_txt = event.target.innerText
      }
    },
    startReading() {
      const baseUrl = process.env.VUE_APP_API_URL + 'article/generate'
      const eventFetch = new FetchEventSource()
      // this.chContent = ''
      eventFetch.stopFetchEvent()
      eventFetch.startFetchEvent(baseUrl, {}, res => {
        this.decodeSSEString(res, eventFetch, this.chContent)
      }, () => {
        console.log('end')
      }, error => {
        console.log(error, 'error')
      })
    },
    decodeSSEString(sseString, eventFetch){
      const sseArray = sseString.split('\n')
      let eventV
      let dataV
      sseArray.forEach((line) => {
        if(line.length > 0){
          const [key, value] = line.split(':')
          // console.log('KV->' + key + ':' + value)
          if(key.trim() === 'event') {
            if (value === 'over') {
              eventFetch.stopFetchEvent()
              eventV = dataV = null
              console.log(this.chContent)
              return
            }
            eventV = value
          } else if(key.trim() === 'data') {
            dataV = value
          }
          if(eventV !== null && dataV != null) {
            // dataV减去最前面的一个空格
            this.chContent += dataV.substring(1)
            eventV = dataV = null
          }
        }
      })
    },
    addElementSpan(str) {
      return str
          .split(' ')
          .map((item) => {
            const { start, word, end } = this.getWord(item)
            return `${start}<span>${word}</span>${end} `
          })
          .join('')
    },
    getWord(str) {
      let word = ''
      let start = ''
      let end = ''
      let j = str.length - 1
      let i = 0

      while (i < str.length) {
        if (/^[a-zA-Z]$/.test(str[i])) {
          break
        }
        start = start + str[i]
        i += 1
      }

      while (j >= 0) {
        if (/^[a-zA-Z]$/.test(str[j])) {
          break
        }
        end = str[j] + end
        j -= 1
      }

      word = str.slice(i, j + 1)

      // 处理数字
      if (!word && start === end) {
        start = ''
      }

      return {
        start,
        word,
        end
      }
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

.container {
  font-size: 20px;
  padding: 10px;
  line-height: 2.5;
}

</style>
