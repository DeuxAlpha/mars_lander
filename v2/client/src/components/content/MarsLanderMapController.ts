export class MarsLanderMapController {
  private map: SVGElement | null = null;

  public Build(map: SVGSVGElement) {
    this.map = map;
  }
}