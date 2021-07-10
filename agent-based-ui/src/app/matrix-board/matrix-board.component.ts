import { KeyValue } from '@angular/common';
import {
  AfterViewInit,
  Component,
  ElementRef,
  OnInit,
  ViewChild,
} from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  Validators,
} from '@angular/forms';
import { AgentType } from '../enums/AgentType.enum';

export interface Position {
  x: number;
  y: number;
}
export interface Cell {
  isSelecting: boolean;
  responsible: AgentType;
  modifiedDate: number;
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
      alert('Invalid input');
      return;
    }
    console.log(this.form.getRawValue());
    const formSettings = this.form.getRawValue();
    let exportDataString = '';

    exportDataString += `num_agv_loading_step_conf = ${formSettings.agvLoadingTime}\n`;
    exportDataString += `num_agv_filling_step_conf = ${formSettings.agvFillingTime}\n`;

    const numberOfPersonAgent = Object.keys(this.cellDict).filter(
      (key) => this.cellDict[key].responsible === AgentType.PersonAgent
    ).length;
    exportDataString += `num_person_agent_conf = ${numberOfPersonAgent}\n`;

    const agvStationKeys = Object.keys(this.cellDict).filter(
      (key) => this.cellDict[key].responsible === AgentType.AgvStationAgent
    );
    exportDataString += 'agv_station_pos_dict_conf = {';
    for (let index = 1; index < agvStationKeys.length + 1; index++) {
      exportDataString += `"${index}": (${agvStationKeys[index - 1]})`;
      if (index < agvStationKeys.length) {
        exportDataString += ', ';
      }
    }
    exportDataString += '} \n';

    const spotAgentKeys = Object.keys(this.cellDict)
      .filter((key) => this.cellDict[key].responsible === AgentType.SpotAgent)
      .sort(
        (a, b) =>
          formSettings.processingTimes[a].order -
          formSettings.processingTimes[b].order
      );
    const xPosList = spotAgentKeys.map((key) => +key.split(', ')[0]);
    const minX = Math.min(...xPosList);
    const maxX = Math.max(...xPosList);
    exportDataString += `left_x_pos_spot_column = ${minX}\n`;
    exportDataString += `right_x_pos_spot_column = ${maxX}\n`;

    exportDataString += 'spot_pos_dict_conf = {';
    for (let index = 1; index < spotAgentKeys.length + 1; index++) {
      const spotAgentPosition = spotAgentKeys[index - 1];
      exportDataString += `"${formSettings.processingTimes[spotAgentPosition].order}": (${spotAgentPosition})`;
      if (index < spotAgentKeys.length) {
        exportDataString += ', ';
      }
    }
    exportDataString += '} \n';

    exportDataString += 'product_processing_duration_dict_input_conf = {';
    for (let index = 1; index < spotAgentKeys.length + 1; index++) {
      const spotAgentPosition = spotAgentKeys[index - 1];
      exportDataString += `"${
        formSettings.processingTimes[spotAgentPosition].order
      }": {"A": [${this.getStringOrDefault(
        formSettings.processingTimes[spotAgentPosition].processingTimeA,
        '1'
      )}], "B": [${this.getStringOrDefault(
        formSettings.processingTimes[spotAgentPosition].processingTimeB,
        '1'
      )}]}`;
      if (index < spotAgentKeys.length) {
        exportDataString += ', ';
      }
    }
    exportDataString += '} \n';
    console.log(exportDataString);

    const file = new Blob([exportDataString]);
    const a = document.createElement('a'),
      url = URL.createObjectURL(file);
    a.href = url;
    a.download = 'configuration.py';
    document.body.appendChild(a);
    a.click();
    setTimeout(function () {
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    }, 0);
  }

  getStringOrDefault(str: string, defaultStr: string): string {
    return this.isNullOrWhiteSpace(str) ? defaultStr : str;
  }

  isNullOrWhiteSpace(str: string): boolean {
    if (str && str.trim()) {
      return false;
    }
    return true;
  }

  onMouseUp(event: Event) {
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

  onMouseDown(event: Event) {
    event = event as MouseEvent;
    this.selectedAreaStartPosition = {
      x: (<MouseEvent>event).offsetX,
      y: (<MouseEvent>event).offsetY,
    };
    this.selectedAreaEndPosition = null;
    this.isMouseDown = true;
    this.updateMinMaxXY();
  }

  onMouseMove(event: Event) {
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
        order: null,
        modifiedDate: Date.now(),
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

  get processingTimesFormGroup() {
    return this.form.get('processingTimes') as FormGroup;
  }

  trackByFn(
    index: number,
    cellFormControlObj: KeyValue<string, AbstractControl>
  ) {
    return cellFormControlObj.key;
  }

  keyValueSortFn(
    a: KeyValue<string, AbstractControl>,
    b: KeyValue<string, AbstractControl>
  ) {
    return 0;
  }

  onMake(agentType: AgentType) {
    Object.keys(this.cellDict)
      .filter((key) => this.cellDict[key].isSelecting)
      .forEach((key) => {
        const cell = this.cellDict[key];
        cell.responsible = agentType;
        cell.modifiedDate = Date.now();
      });
    const oldValues = this.processingTimesFormGroup.value;
    const spotCellKeys = Object.keys(this.cellDict)
      .filter(
        (cellKey) => this.cellDict[cellKey].responsible === AgentType.SpotAgent
      )
      .sort(
        (a, b) => this.cellDict[a].modifiedDate - this.cellDict[b].modifiedDate
      );

    const spotCellFormControlDict: Dictionary<FormGroup> = {};
    let defaultOrder = 1;
    spotCellKeys.forEach((cellKey) => {
      spotCellFormControlDict[cellKey] = this.fb.group({
        processingTimeA: this.fb.control('1'),
        processingTimeB: this.fb.control('1'),
        order: this.fb.control(defaultOrder, Validators.min(1)),
      });
      defaultOrder++;
    });
    const spotCellFormGroup = this.fb.group(spotCellFormControlDict);
    //spotCellFormGroup.patchValue(oldValues);
    this.form.setControl('processingTimes', spotCellFormGroup);
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
