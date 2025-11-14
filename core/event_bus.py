# file: core/event_bus.py
from collections import defaultdict
from typing import Callable, Dict, List, Any


class EventBus:
    """
    Very simple publish/subscribe event bus.

    - subscribe(event_name, callback)
    - unsubscribe(event_name, callback)
    - publish(event_name, *args, **kwargs)
    """

    def __init__(self):
        self._listeners: Dict[str, List[Callable[..., Any]]] = defaultdict(list)

    def subscribe(self, event_name: str, callback: Callable[..., Any]) -> None:
        self._listeners[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable[..., Any]) -> None:
        if event_name in self._listeners:
            try:
                self._listeners[event_name].remove(callback)
            except ValueError:
                pass

    def publish(self, event_name: str, *args, **kwargs) -> None:
        for callback in list(self._listeners.get(event_name, [])):
            callback(*args, **kwargs)