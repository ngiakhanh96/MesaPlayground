import {
  AfterViewInit,
  ChangeDetectorRef,
  ContentChild,
  Directive,
  Input,
  OnDestroy,
  TemplateRef,
} from '@angular/core';
import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { NotificationService } from 'src/app/services/notification.service';

export interface Config {
  id: string;
  textTitle: string;
  description: string;
  buttonText?: string;
  buttonFn: () => void;
  showDescription?: boolean;
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
export class ConfigPanelComponent implements OnInit, AfterViewInit, OnDestroy {
  @Input() set configs(v: Config[]) {
    this._configs = v;
    this._descriptionStateDict = {};
    this._configs.forEach(
      (cfg) => (this._descriptionStateDict[cfg.id] = false)
    );
    this.cdr.detectChanges();
  }
  get configs(): Config[] {
    return this._configs;
  }

  @ContentChild(ConfigPanelTableTemplateDirective)
  configPanelTableDirective: ConfigPanelTableTemplateDirective | null = null;

  _subscription: Subscription = new Subscription();
  _configs: Config[] = [];

  get configPanelTableId(): string | null {
    return this.configPanelTableDirective?.id ?? null;
  }

  get configPanelTableTmp(): TemplateRef<unknown> | null {
    return this.configPanelTableDirective?.template ?? null;
  }

  _descriptionStateDict: Dictionary<boolean> = {};

  constructor(
    private cdr: ChangeDetectorRef,
    private notificationService: NotificationService
  ) {}

  ngOnDestroy(): void {
    this._subscription.unsubscribe();
  }

  ngAfterViewInit(): void {
    this.cdr.detach();
  }

  ngOnInit() {
    this._subscription = this.notificationService
      .getNotification()
      .subscribe((x) => this.cdr.detectChanges());
  }

  onClick(config: Config) {
    config.buttonFn();
    this.cdr.detectChanges();
  }

  toggleDescription(configId: string) {
    this._descriptionStateDict[configId] =
      !this._descriptionStateDict[configId];
    this.cdr.detectChanges();
  }

  showDescription(configId: string): boolean {
    return this._descriptionStateDict[configId];
  }

  onClickTest() {
    console.log('Test');
  }
}
