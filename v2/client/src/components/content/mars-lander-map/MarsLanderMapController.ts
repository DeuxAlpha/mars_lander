import * as ECharts from 'echarts';

export class MarsLanderMapController {
  constructor() {
  }

  private chart?: ECharts.ECharts;

  public InitializeChart(wrapper: HTMLDivElement) {
    this.chart = ECharts.init(wrapper);
  }

  public LoadData() {
    const option: ECharts.EChartOption = {
      title: {
        text: 'Mars Lander',
        left: 'center'
      },
      tooltip: {},
      xAxis: {
        min: 0,
        max: 7000
      },
      yAxis: {
        min: 0,
        max: 3000
      },
      series: [{
        name: 'Ground',
        type: 'line',
        data: [
          [0, 100],
          [1000, 500],
          [1500, 1500],
          [3000, 1000],
          [4000, 150],
          [5500, 150],
          [6999, 800]
        ]
      }]
    };

    this.chart?.setOption(option);

    window.addEventListener('resize', () => {
      this.chart?.resize();
    })
  }
}