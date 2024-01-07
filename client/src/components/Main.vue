<template>
  <div @touchmove.prevent @mousewheel.prevent>
    <van-nav-bar
        left-text=""
        right-text=""
        fixed="fixed"
        :placeholder="false"
        :left-arrow="false"
        style="background-color: #00bdff"
        :safe-area-inset-top="true"
    >
      <template #title>
        <span></span>
      </template>
    </van-nav-bar>
    <div style="width: 100vw; height: 46px"/>
    <van-grid square :gutter="10" :column-num="3">
      <van-grid-item icon="flag-o" text="学新单词" to="/word-study" />
      <van-grid-item icon="certificate" text="复习单词" to="/word-revise" />
      <van-grid-item icon="notes-o" text="单词阅读" to="/ai-reading"/>
      <van-grid-item icon="down" text="导入单词" to="/import-content"/>
    </van-grid>
    <van-cell-group inset>
      <van-cell title="今日待复习" value="0个单词"/>
    </van-cell-group>
    <van-row>
      <van-col span="24" style="text-align: center">
<!--        <iframe src="https://youdao.com/result?word=novel&lang=en" style="border: 0; width: 100%; height: 500px">-->
<!--        </iframe>-->

      </van-col>
    </van-row>
  </div>
</template>
<script>
import { Dialog } from 'vant'

export default {
  name: 'Main',
  created() {

  },
  mounted(){

  },
  data() {
    return {
    }
  },
  methods: {
    allScreen() {
      const domElement = document.documentElement
      if (domElement.requestFullscreen) {
        domElement.requestFullscreen()
      } else if (domElement.mozRequestFullScreen) {
        domElement.mozRequestFullScreen()
      } else if (domElement.webkitRequestFullScreen) {
        domElement.webkitRequestFullScreen()
      }
    }
  }
}
</script>
<style scoped>

</style>
