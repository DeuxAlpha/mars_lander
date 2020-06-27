import * as D3 from 'd3';

export class MarsLanderMapController {
  constructor(element: SVGSVGElement) {
    this.map = D3.select(element);
    this.buildSvg();
  }

  private readonly map!: D3.Selection<SVGSVGElement, any, null, undefined>;

  private buildSvg() {
    this.map.append('svg')
      .attr('width', '100%')
      .attr('height', '100%');
  }

  public GenerateBoundaries(x: number, y: number) {

  }
}