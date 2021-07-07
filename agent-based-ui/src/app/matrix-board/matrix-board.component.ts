import { Component, OnInit } from '@angular/core';

export interface Position {
  x: number;
  y: number;
}

@Component({
  selector: 'app-matrix-board',
  templateUrl: './matrix-board.component.html',
  styleUrls: ['./matrix-board.component.scss'],
})
export class MatrixBoardComponent implements OnInit {
  width: number[] = [].constructor(10);
  height: number[] = [].constructor(10);
  selectedAreaStartPosition: Position | null = null;
  selectedAreaEndPosition: Position | null = null;

  constructor() {}

  ngOnInit(): void {}

  onMouseDown(position: Position) {
    this.selectedAreaStartPosition = position;
    this.selectedAreaEndPosition = null;
  }

  onMouseUp(position: Position) {
    this.selectedAreaEndPosition = position;
  }

  isSelectedCell(position: Position) {
    if (
      this.selectedAreaStartPosition == null ||
      this.selectedAreaEndPosition == null
    ) {
      return false;
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
    if (
      position.x <= maxX &&
      position.x >= minX &&
      position.y <= maxY &&
      position.y >= minY
    ) {
      return true;
    }
    return false;
  }
}
