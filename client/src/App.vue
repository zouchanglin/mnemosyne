<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import { Dialog } from 'vant'

export default {
  name: 'App',
  created() {

  },
  mounted() {
    // Dialog.confirm({
    //   title: '全屏模式',
    //   message: '是否需要进入全屏沉浸式体验?'
    // })
    //     .then(() => {
    //       this.allScreen()
    //     })
    //     .catch(() => {
    //       // on cancel
    //     })
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

<style>

</style>
