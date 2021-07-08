import {
  AfterViewInit,
  Component,
  ElementRef,
  HostListener,
  OnInit,
  ViewChild,
} from '@angular/core';

export interface Position {
  x: number;
  y: number;
}

@Component({
  selector: 'app-matrix-board',
  templateUrl: './matrix-board.component.html',
  styleUrls: ['./matrix-board.component.scss'],
})
export class MatrixBoardComponent implements OnInit, AfterViewInit {
  width: number[] = [].constructor(10);
  height: number[] = [].constructor(10);
  cellWidth: number = 0;
  cellHeight: number = 0;
  selectedAreaStartPosition: Position | null = null;
  selectedAreaEndPosition: Position | null = null;

  @ViewChild('mainContainer', { static: true })
  mainContainer!: ElementRef<HTMLDivElement>;

  @ViewChild('canvas', { static: true })
  canvasArea!: ElementRef<HTMLCanvasElement>;
  canvasCtx: CanvasRenderingContext2D | null = null;
  isMouseDown: boolean = false;

  minMaxXYs: number[] = [];

  constructor() {}

  ngAfterViewInit(): void {
    this.canvasCtx = this.canvasArea.nativeElement.getContext('2d')!;
    this.cellWidth =
      this.mainContainer.nativeElement.offsetWidth / this.width.length;
    this.cellHeight =
      this.mainContainer.nativeElement.offsetHeight / this.height.length;
    this.onResizeCanvas();
  }

  ngOnInit(): void {}

  @HostListener('mouseup', ['$event'])
  onHostMouseUp(event: MouseEvent): void {
    this.resetCanvas();
    this.isMouseDown = false;
  }

  @HostListener('mousedown', ['$event'])
  onHostMouseDown(event: MouseEvent): void {
    this.selectedAreaStartPosition = {
      x: event.offsetX,
      y: event.offsetY,
    };
    this.selectedAreaEndPosition = null;
    this.isMouseDown = true;
    this.updateMinMaxXY();
  }

  @HostListener('mousemove', ['$event'])
  onHostMouseMove(event: MouseEvent): void {
    if (this.isMouseDown == false || this.selectedAreaStartPosition == null) {
      return;
    }
    this.selectedAreaEndPosition = {
      x: event.offsetX,
      y: event.offsetY,
    };
    this.updateMinMaxXY();

    this.resetCanvas();
    const [minX, maxX, minY, maxY] = [...this.minMaxXYs];
    this.canvasCtx!.beginPath();
    this.canvasCtx!.rect(minX, minY, maxX - minX, maxY - minY);
    this.canvasCtx!.stroke();
  }

  isSelectedCell(position: Position) {
    if (this.minMaxXYs.length === 0) {
      return false;
    }
    const [minX, maxX, minY, maxY] = [...this.minMaxXYs];
    if (
      ((position.x + this.cellWidth <= maxX &&
        position.x + this.cellWidth >= minX) ||
        (position.x <= maxX && position.x >= minX)) &&
      ((position.y + this.cellHeight <= maxY &&
        position.y + this.cellHeight >= minY) ||
        (position.y <= maxY && position.y >= minY))
    ) {
      return true;
    }
    return false;
  }

  updateMinMaxXY() {
    if (
      this.selectedAreaStartPosition == null ||
      this.selectedAreaEndPosition == null
    ) {
      this.minMaxXYs = [];
      return;
    }
    const minX = Math.min(
      this.selectedAreaStartPosition!.x,
      this.selectedAreaEndPosition!.x
    );
    const maxX = Math.max(
      this.selectedAreaStartPosition!.x,
      this.selectedAreaEndPosition!.x
    );
    const minY = Math.min(
      this.selectedAreaStartPosition!.y,
      this.selectedAreaEndPosition!.y
    );
    const maxY = Math.max(
      this.selectedAreaStartPosition!.y,
      this.selectedAreaEndPosition!.y
    );
    this.minMaxXYs = [minX, maxX, minY, maxY];
  }

  onResizeCanvas() {
    this.canvasCtx!.canvas.width =
      this.mainContainer!.nativeElement.offsetWidth;
    this.canvasCtx!.canvas.height =
      this.mainContainer!.nativeElement.offsetHeight;
  }

  resetCanvas() {
    this.canvasCtx!.clearRect(
      0,
      0,
      this.canvasArea.nativeElement.width,
      this.canvasArea.nativeElement.height
    );
  }
}
