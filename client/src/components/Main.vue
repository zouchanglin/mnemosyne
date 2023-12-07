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
      <van-col span="12">
        <div v-html="html"></div>
      </van-col>
      <van-col span="12">

      </van-col>
    </van-row>
  </div>
</template>
<script>
export default {
  name: 'Main',
  created() {

  },
  mounted(){
    const myChartEl = document.getElementById('myChart')
    const myChartEl2 = document.getElementById('myChart2')
    console.log(this.$echarts)
    // 基于准备好的dom，初始化echarts实例
    const myChart = this.$echarts.init(myChartEl)
    const myChart2 = this.$echarts.init(myChartEl2)
    const option = {
      title: {
        text: ''
      },
      series: [
        {
          type: 'pie',
          data: [
            {
              value: 55,
              name: '记忆度>80'
            },
            {
              value: 234,
              name: '60<记忆度<80'
            },
            {
              value: 1548,
              name: '记忆度<60'
            }
          ]
        }
      ]
    }

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option)

    const option2 = {
      xAxis: {
        data: ['1', '2', '3', '4', '5', '6', '7']
      },
      yAxis: {},
      series: [
        {
          data: [10, 22, 28, 23, 19, 90, 30],
          type: 'line',
          smooth: true
        }
      ]
    }
    myChart2.setOption(option2)
    this.$http.get('youdao')
        .then(response => {
          this.html = response.data
        })
  },
  data() {
    return {
      html: 'hello'
    }
  }
}
</script>
<style scoped>

</style>
