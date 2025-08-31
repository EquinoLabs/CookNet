let listeners = [];

export function subscribe(listener) {
  listeners.push(listener);
  return () => {
    listeners = listeners.filter((l) => l !== listener);
  };
}

export function emitToast(title, message, type = "error") {
  listeners.forEach((l) => l(title, message, type));
}
