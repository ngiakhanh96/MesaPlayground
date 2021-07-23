import {
  AfterViewInit,
  ChangeDetectionStrategy,
  ChangeDetectorRef,
  ContentChild,
  Directive,
  Input,
  TemplateRef,
} from '@angular/core';
import { Component, OnInit } from '@angular/core';
import { NotificationService } from 'src/app/services/notification.service';

export interface Config {
  id: string;
  textTitle: string;
  description: string;
  buttonText?: string;
  buttonFn: () => void;
}

@Directive({ selector: '[appConfigPanelTableTmp]' })
export class ConfigPanelTableTemplateDirective {
  @Input() public id: string = '';
  constructor(public template: TemplateRef<unknown>) {}
}

@Component({
  selector: 'app-config-panel',
  templateUrl: './config-panel.component.html',
  styleUrls: ['./config-panel.component.scss'],
})
export class ConfigPanelComponent implements OnInit, AfterViewInit {
  @Input() configs: Config[] = [];
  @Input() set triggerChangeDetector(v: boolean) {}
  _triggerChangeDetector: boolean = false;
  @ContentChild(ConfigPanelTableTemplateDirective)
  configPanelTableDirective: ConfigPanelTableTemplateDirective | null = null;

  get configPanelTableId(): string | null {
    return this.configPanelTableDirective?.id ?? null;
  }

  get configPanelTableTmp(): TemplateRef<unknown> | null {
    return this.configPanelTableDirective?.template ?? null;
  }

  constructor(
    private cdr: ChangeDetectorRef,
    private notificationService: NotificationService
  ) {}

  ngAfterViewInit(): void {
    this.cdr.detach();
  }

  ngOnInit() {
    this.notificationService
      .getNotification()
      .subscribe((x) => this.cdr.detectChanges());
  }

  onClick(config: Config) {
    config.buttonFn();
    this.cdr.detectChanges();
  }
}
