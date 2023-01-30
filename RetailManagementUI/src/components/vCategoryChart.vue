<template>
  <div id="category-chart" :style="{width: '100%', height: '100%', margin: '20px'}"></div>
</template>

<script>
import 'echarts/lib/component/legend'

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
        trigger: 'item'
      },
      title: {
        text: '商品种类销量统计',
        left: 'center'
      },
      legend: {
        orient: 'vertical',
        left: 'left',
        data:[],
      },
      series: [
        {
          data: [],
          type: 'pie',
          radius: '50%',
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
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
      this.salesChart = this.$echarts.init(document.getElementById('category-chart'))
      this.salesChart.setOption(this.option)
    },
    loadSalesChart() {
      this.option.legend.data = []
      this.option.series[0].data = []
      this.$http.get('http://127.0.0.1:8000/categorystats/')
          .then((response) => {
            let res = JSON.parse(response.bodyText)
            if (response.status === 200) {
              let jsonObj = JSON.parse(res)
              for (let key in jsonObj) {
                this.option.legend.data.push(key)
                this.option.series[0].data.push({'name':key,'value':jsonObj[key]})
              }
              this.salesChart.setOption(this.option)
            } else {
              this.$Message.error('查询失败')
            }
          })

    }
  }
}

</script>

<style scoped>
</style>
