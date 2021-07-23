import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class NotificationService {
  private notification = new Subject<boolean>();
  constructor() {}

  getNotification(): Observable<boolean> {
    return this.notification;
  }

  notify(value: boolean) {
    this.notification.next(value);
  }
}
