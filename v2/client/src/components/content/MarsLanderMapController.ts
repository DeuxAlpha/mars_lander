import * as ECharts from 'echarts';

export class MarsLanderMapController {
  constructor() {
  }

  private chart?: ECharts.ECharts;

  public InitializeChart(wrapper: HTMLDivElement) {
    this.chart = ECharts.init(wrapper);
  }

  public LoadData() {
    const option: ECharts.EChartsResponsiveOption = {
      baseOption: {
        title: {
          text: 'ECharts entry example'
        },
        tooltip: {},
        legend: {
          data: ['Sales']
        },
        xAxis: {
          data: ["shirt", "cardign", "chiffon shirt", "pants", "heels", "socks"]
        },
        yAxis: {},
        series: [{
          name: 'Sales',
          type: 'bar',
          data: [5, 20, 36, 10, 10, 20]
        }]
      },
      media: [{
        query: {},
        option: {
          series: [{center: ['50%', '50%']}]
        }
      }]
    };

    this.chart?.setOption(option);
  }
}