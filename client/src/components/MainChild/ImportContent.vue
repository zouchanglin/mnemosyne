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
        <span>导入单词</span>
      </template>
    </van-nav-bar>
    <van-notice-bar color="#1989fa" background="#ecf9ff" left-icon="info-o" scrollable>
      通过其他平台的学习截图，直接通过OCR导入所学单词，简单快捷！
    </van-notice-bar>
    <van-row>
      <van-form @submit="startOCRWord">
        <van-field name="uploader" label="照片/截图">
          <template #input>
            <van-uploader v-model="fileList" multiple :max-count="6"
                          :max-size="5000 * 1024" @oversize="onOversize"
                          :after-read="afterRead"/>
          </template>
        </van-field>
        <div style="margin: 16px;">
          <van-button round block :loading="buttonLoading" :disabled="fileNameList.length <= 0"
                      v-if="ocr_words.length === 0 " type="info" native-type="submit">开始上传</van-button>
        </div>
      </van-form>
    </van-row>
    <van-row>
      <van-list
          v-if="ocr_words.length > 0"
          style="overflow: auto; height: 60vh;"
          v-model="loading"
          :finished="finished"
          finished-text="没有更多了"
      >
        <van-row v-for="w in ocr_words" :key="w.id">
          <van-col span="20">
            <van-cell :title="w.word" :label="truncatedText(w.trans)" @click="click_word(w.id)"/>
          </van-col>
          <van-col span="4">
            <van-button icon="close" block @click="deleteWord(w.id)"></van-button>
          </van-col>
        </van-row>
      </van-list>
    </van-row>

    <word-card :word_id="word_id" @close_word_card="word_id=-1">
    </word-card>

    <!-- 底部固定按钮 -->
    <van-button class="fixed-bottom" v-if="ocr_words.length > 0" type="info" native-type="submit" icon="down"
               round @click="importWords">确认导入已学习</van-button>
  </div>
</template>
<script>
import { Notify, Toast } from 'vant'
import WordCard from '@/components/ChildComponent/WordCard.vue'
export default {
  name: 'ImportContent',
  components: { WordCard },
  data() {
    return {
      buttonLoading: false,
      loading: false,
      finished: false,
      word_id: 0,
      audio: new Audio(),
      ocr_words: [],
      fileList: [
      ],
      fileNameList: []
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
    async importWords(){
      const params = {
        word_ids: this.ocr_words.map(w => w.id)
      }
      const { data: ret } = await this.$http.post('/ebbinghaus/import', params)
      if (ret.code !== 0) {
        Notify('导入失败，请联系管理员处理!')
      }else{
        Toast.success('导入成功')
        console.log('ret.data--->', ret.data)
        await this.$router.push('/ai-reading')
        console.log('跳转到AI阅读')
      }
    },
    async startOCRWord() {
      console.log('StartOcr')
      this.loading = true
      this.buttonLoading = true
      const params = {
        files: this.fileNameList
      }
      const { data: ret } = await this.$http.post('/ocr/exec', params)
      // this.fileList = []
      if (ret.code !== 0) {
        Notify('OCR识别失败，请检查图片是否清晰')
      }else {
        Notify({ message: 'OCR识别成功!', type: 'success' })
        console.log('ret.data--->', ret.data)
        this.ocr_words = ret.data.words
      }
      this.loading = false
      this.buttonLoading = false
      this.finished = true
    },
    onClickLeft() {
      this.$router.push('/home')
    },
    onOversize(file) {
      console.log(file)
      Toast('文件大小不能超过 5M')
    },
    async afterRead(file) {
      file.status = 'uploading'
      file.message = '上传中...'

      // console.log('file->', file.file)
      const formData = new FormData()
      formData.append('file', file.file)

      const { data: ret } = await this.$http.post('/file/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      if (ret.code === 0) {
          file.status = 'done'
          file.message = '上传成功'
          Toast.success('上传成功')
          this.fileNameList.push(ret.data.name)
      }else {
          file.status = 'failed'
          file.message = '上传失败'
      }
    },
    truncatedText(text, maxLength = 16) {
      if (text.length > maxLength) {
        return text.substring(0, maxLength) + '...'
      }
      return text
    },
    deleteWord(id) {
      console.log('deleteWord', id)
      this.ocr_words = this.ocr_words.filter(w => w.id !== id)
    }
  }
}
</script>
<style scoped>
.fixed-bottom {
  position: fixed;
  bottom: 0;
  width: 95%;
  margin-bottom: 10px;
}
</style>
