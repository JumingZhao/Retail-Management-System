<template>
  <div class="sales-record" :style="{width: '100%', height: '100%'}">
    <div class="month-search-box">
      <DatePicker type="month" v-model="date" placement="bottom-end" placeholder="选择月份"
                  style="width: 200px"></DatePicker>
      <Button @click.native="searchByMonth" type="primary" icon="search">搜索</Button>
    </div>
    <div id="monthly-chart" :style="{width: '100%', height: '80%'}"></div>

  </div>
</template>

<script>

export default {
  data() {
    return {
      date: new Date(),
      monthlyChart: null,
      option: null,
      noData: true,
    }
  },
  created() {
    this.option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {type: 'cross'}
      },
      xAxis: {
        name: '销售经理',
        data: []
      },
      yAxis: {
        name: '销售额'
      },
      series: [
        {
          data: [],
          type: 'bar'
        }
      ]
    }
  },
  mounted() {
    this.initSalesChart();
  },
  methods: {
    initSalesChart() {
      this.monthlyChart = this.$echarts.init(document.getElementById('monthly-chart'))
    },
    searchByMonth() {
      let param = {};
      if (this.date!== null) {
        param['date'] = this.date.getFullYear() + '-' + (this.date.getMonth() + 1)
      } else {
        this.date = new Date()
        param['date'] = this.date.getFullYear() + '-' + (this.date.getMonth() + 1)
      }

      this.option.xAxis.data = []
      this.option.series[0].data = []
      this.$http.get('http://127.0.0.1:8000/managersales/',{params: param})
          .then((response) => {
            let res = JSON.parse(response.bodyText)
            let jsonObj = JSON.parse(res)
              for (let key in jsonObj) {
                this.option.xAxis.data.push(key)
                this.option.series[0].data.push(jsonObj[key])
              }
              this.monthlyChart.setOption(this.option)
            this.noData = false
          },response => {
              this.$Message.error('查询失败')
            })
    }
  }
}

</script>

<style>
.month-search-box {
  padding: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.month-search-box > div {
  margin-right: 2em;
}
</style>
