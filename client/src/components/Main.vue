<template>
  <div>
    <van-sticky>
    </van-sticky>
    <van-grid square :gutter="10" :column-num="3">
      <van-grid-item icon="flag-o" text="学新单词" to="/word-study" />
      <van-grid-item icon="certificate" text="复习单词" to="/word-revise" />
      <van-grid-item icon="notes-o" text="单词阅读" to="/ai-reading"/>
    </van-grid>
    <van-cell-group inset>
      <van-cell title="今日待复习" value="72个单词"/>
    </van-cell-group>
    <div id="myChart" style="width: 100%;height:300px;"/>
    <div id="myChart2" style="width: 100%;height:300px;"/>
    <van-row>
<!--      <van-col span="12">-->
<!--        <div v-html="html"></div>-->
<!--      </van-col>-->
      <van-col span="12">

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
      html: 'hello'
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
