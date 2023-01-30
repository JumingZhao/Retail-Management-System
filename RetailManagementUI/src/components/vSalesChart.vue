<template>
  <div id="sales-chart" :style="{width: '100%', height: '100%', margin: '20px'}"></div>
</template>

<script>

export default {
  data() {
    return {
      salesChart: null,
      option: null,
      categoryList: null,
    }
  },
  created() {
    this.option = {
      tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'cross' }
  },
        xAxis: {
          name: '时间',
          data: []
        },
        yAxis: {
          name: '销售额'
        },
        series: [
          {
            data: [],
            type: 'line'
          }
        ]
      }
  },
  mounted() {
    this.initSalesChart();
    this.loadSalesChart();
  },
  methods: {
    initSalesChart() {
      this.salesChart = this.$echarts.init(document.getElementById('sales-chart'))
      this.salesChart.setOption(this.option)
    },
    loadSalesChart() {
      this.option.xAxis.data = []
      this.option.series[0].data = []
      this.$http.get('http://127.0.0.1:8000/salesbymonth/')
            .then((response) => {
              let res = JSON.parse(response.bodyText)
              if (response.status === 200) {
                let jsonObj = JSON.parse(res)
                for(let key in jsonObj){
                  this.option.xAxis.data.push(key)
                  this.option.series[0].data.push(jsonObj[key])
                }
                this.salesChart.setOption(this.option)
              } else {
                this.$Message.error('查询失败')
              }})

    }
  }
}

</script>

<style scoped>
</style>
