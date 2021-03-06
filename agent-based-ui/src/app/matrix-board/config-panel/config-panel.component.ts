import { Utils } from './../../utils/utils';
import { ContentChild, Directive, Input, TemplateRef } from '@angular/core';
import { Component, OnInit } from '@angular/core';

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
export class ConfigPanelComponent implements OnInit {
  @Input() set configs(v: Config[]) {
    if (Utils.isEqual(v, this._configs)) {
      return;
    }
    this._configs = v;
    this.descriptionStateDict = {};
    this._configs.forEach((cfg) => (this.descriptionStateDict[cfg.id] = false));
  }
  get configs(): Config[] {
    return this._configs;
  }

  @ContentChild(ConfigPanelTableTemplateDirective)
  configPanelTableDirective: ConfigPanelTableTemplateDirective | null = null;

  get configPanelTableId(): string | null {
    return this.configPanelTableDirective?.id ?? null;
  }

  get configPanelTableTmp(): TemplateRef<unknown> | null {
    return this.configPanelTableDirective?.template ?? null;
  }

  descriptionStateDict: Dictionary<boolean> = {};
  _configs: Config[] = [];

  constructor() {}

  ngOnInit() {}

  onClick(config: Config) {
    config.buttonFn();
  }

  toggleDescription(configId: string) {
    this.descriptionStateDict[configId] = !this.descriptionStateDict[configId];
  }

  showDescription(configId: string): boolean {
    return false;
    //return this._descriptionStateDict[configId];
  }
}
