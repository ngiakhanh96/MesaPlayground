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
}
