import * as D3 from 'd3';

export class MarsLanderMapController {
  private wrapper!: HTMLElement;
  private map!: D3.Selection<SVGSVGElement, any, null, undefined>;

  public Init(element: HTMLElement) {
    this.wrapper = element;
  }

  public GenerateBoundaries(x: number, y: number) {
    console.dir(this.wrapper);
    this.map = D3.select(this.wrapper)
      .append('svg')
      .attr('width', '100%')
      .attr('height', '100%')
      .attr('viewBox', '0 0 7000 3000')

    const data = [{x: 0, y: 20}, {x: 150, y: 150}, {x: 300, y: 100}, {x: 450, y: 20}, {x: 600, y: 130}]

    this.map.append('path')
      .datum(data)
      .attr('d', D3.line<{x: number, y: number}>()
        .x(d => d.x)
        .y(d => d.y))
      .attr('stroke', 'black')
      .attr('fill', 'none');
  }
}