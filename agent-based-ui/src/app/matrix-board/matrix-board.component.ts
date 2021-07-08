import { KeyValue } from '@angular/common';
import {
  AfterViewInit,
  Component,
  ElementRef,
  OnInit,
  ViewChild,
} from '@angular/core';
import {
  FormArray,
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';
import { AgentType } from '../enums/AgentType.enum';
import { Utils } from '../utils/utils';

export interface Position {
  x: number;
  y: number;
}
export interface Cell {
  isSelecting: boolean;
  responsible: AgentType;
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

  cellDict: Dictionary<Cell> = {};

  AgentType: typeof AgentType = AgentType;

  form = this.fb.group({
    agvLoadingTime: ['1', Validators.min(1)],
    agvFillingTime: ['1', Validators.min(1)],
    processingTimes: this.fb.group({}),
  });

  constructor(private fb: FormBuilder) {}

  ngAfterViewInit(): void {
    this.onResizeCanvas();
  }

  ngOnInit(): void {
    this.canvasCtx = this.canvasArea.nativeElement.getContext('2d')!;
    this.cellWidth =
      this.mainContainer.nativeElement.offsetWidth / this.width.length;
    this.cellHeight =
      this.mainContainer.nativeElement.offsetHeight / this.height.length;
    this.onResizeCanvas();
  }

  onSubmit() {
    if (this.form.invalid) {
      // stop here if it's invalid
      alert('Invalid input');
      return;
    }
    console.log(this.form.getRawValue());
  }

  onMouseUp(event: Event): void {
    if (!this.isMouseDown || this.selectedAreaStartPosition == null) {
      return;
    }
    this.selectedAreaEndPosition = {
      x: (<MouseEvent>event).offsetX,
      y: (<MouseEvent>event).offsetY,
    };
    this.updateMinMaxXY();
    this.resetCanvas();
    this.isMouseDown = false;
  }

  onMouseDown(event: Event): void {
    event = event as MouseEvent;
    this.selectedAreaStartPosition = {
      x: (<MouseEvent>event).offsetX,
      y: (<MouseEvent>event).offsetY,
    };
    this.selectedAreaEndPosition = null;
    this.isMouseDown = true;
    this.updateMinMaxXY();
  }

  onMouseMove(event: Event): void {
    if (!this.isMouseDown || this.selectedAreaStartPosition == null) {
      return;
    }
    this.selectedAreaEndPosition = {
      x: (<MouseEvent>event).offsetX,
      y: (<MouseEvent>event).offsetY,
    };
    this.updateMinMaxXY();

    this.resetCanvas();
    const [minX, maxX, minY, maxY] = [...this.minMaxXYs];
    this.canvasCtx!.beginPath();
    this.canvasCtx!.rect(minX, minY, maxX - minX, maxY - minY);
    this.canvasCtx!.stroke();
  }

  getCellClass(position: Position, cellKey: string): string {
    const isSelectedCell = this.isSelectedCell(position);
    if (this.cellDict[cellKey] == null) {
      this.cellDict[cellKey] = {
        isSelecting: false,
        responsible: AgentType.Unknown,
      } as Cell;
    }
    this.cellDict[cellKey].isSelecting = isSelectedCell;
    if (isSelectedCell) {
      return 'cell--selected';
    }
    switch (this.cellDict[cellKey].responsible) {
      case AgentType.SpotAgent:
        return 'cell--spot-agent';
      case AgentType.WorkerMovingArea:
        return 'cell--worker-moving-area';
      case AgentType.AgvStationAgent:
        return 'cell--agv-station-agent';
      case AgentType.PersonAgent:
        return 'cell--person-agent';
      case AgentType.AgvMovingArea:
        return 'cell--agv-moving-area';
      default:
        return 'cell--unknown';
    }
  }

  get processingTimeFormGroup() {
    return this.form.get('processingTimes') as FormGroup;
  }

  trackByFn(index: number, cellFormControlObj: any) {
    return cellFormControlObj.key;
  }

  onMake(agentType: AgentType) {
    Object.values(this.cellDict)
      .filter((cell) => cell.isSelecting)
      .forEach((cell) => (cell.responsible = agentType));
    if (agentType === AgentType.SpotAgent) {
      const oldValues = this.processingTimeFormGroup.value;
      const spotCellKeys = Object.keys(this.cellDict).filter(
        (cellKey) => this.cellDict[cellKey].responsible === AgentType.SpotAgent
      );

      const spotCellFormControlDict: Dictionary<FormControl> = {};
      spotCellKeys.forEach(
        (cellKey) =>
          (spotCellFormControlDict[cellKey] = this.fb.control(
            '1',
            Validators.required
          ))
      );
      const spotCellFormGroup = this.fb.group(spotCellFormControlDict);
      spotCellFormGroup.patchValue(oldValues);
      this.form.setControl('processingTimes', spotCellFormGroup);
    }
  }

  isSelectedCell(position: Position) {
    if (this.minMaxXYs.length === 0) {
      return false;
    }
    const [minX, maxX, minY, maxY] = [...this.minMaxXYs];
    if (
      ((position.x + this.cellWidth <= maxX &&
        position.x + this.cellWidth >= minX) ||
        (position.x <= maxX && position.x >= minX) ||
        (position.x < minX && position.x + this.cellWidth > maxX)) &&
      ((position.y + this.cellHeight <= maxY &&
        position.y + this.cellHeight >= minY) ||
        (position.y <= maxY && position.y >= minY) ||
        (position.y < minY && position.y + this.cellHeight > maxY))
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
