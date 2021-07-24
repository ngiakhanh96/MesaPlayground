import * as _ from 'lodash';
export class Utils {
  static generateNewId(): string {
    return Date.now().toString();
  }

  static toDictionary<T>(
    array: T[],
    keySelector: (p: T) => string
  ): Dictionary<T> {
    const dict: Dictionary<T> = {};
    array.forEach((p) => {
      dict[keySelector(p)] = p;
    });
    return dict;
  }

  static isNullOrWhiteSpace(str: string): boolean {
    if (str && str.trim()) {
      return false;
    }
    return true;
  }

  static isEqual(x: unknown, y: unknown): boolean {
    return JSON.stringify(x) == JSON.stringify(y);
  }
}
