<template>
  <div>
    <van-nav-bar
        style="margin-top: 10px"
        title="学习日历"
        left-text="返回"
        right-text=""
        left-arrow
        @click-left="onClickLeft"
    />
    <van-row>
      <van-calendar
          title=" "
          :readonly="true"
          :poppable="false"
          :show-confirm="false"
          :style="{ height: '450px' }"
      />
    </van-row>
  </div>
</template>
<script>
import { Toast, Notify } from 'vant'
export default {
  name: 'StudyCalendar',
  data() {
    return {
    }
  },
  setup() {

  },
  created() {
  },
  methods: {
    onClickLeft() {
      // Toast('返回')
      this.$router.push('/me')
    }
  }
}
</script>
<style scoped>

</style>
