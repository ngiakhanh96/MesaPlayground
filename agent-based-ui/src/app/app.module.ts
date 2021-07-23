import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import {
  ConfigPanelComponent,
  ConfigPanelTableTemplateDirective,
} from './matrix-board/config-panel/config-panel.component';
import { MatrixBoardComponent } from './matrix-board/matrix-board.component';

@NgModule({
  declarations: [
    AppComponent,
    MatrixBoardComponent,
    ConfigPanelComponent,
    ConfigPanelTableTemplateDirective,
  ],
  imports: [BrowserModule, ReactiveFormsModule],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
