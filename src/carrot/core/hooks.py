import json
import threading
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

"""
HOOKS注册调用和日志保存
"""

class Hooks:
    def __init__(self):
        self._handlers: dict[str, list[Callable]] = defaultdict(list)
        self.errors: list[str] = []

    def on(self,event: str,callback: Callable) -> None:
        self._handlers[event].append(callback)

    def emit(self,event: str,**payload) -> None:
        for callback in [*self._handlers[event],*self._handlers['*']]:
            try:
                callback({"event":event,**payload})
            except Exception as exc:
                self.errors.append(f"{event}:{type(exc).__name__}:{exc}")


class JsonlAudit:
    def __init__(self,path:Path):
        self.path = path
        path.parent.mkdir(parents=True,exist_ok=True)
        self._lock = threading.Lock()

    def __call__(self,event: dict) -> None:
        safe = {
            k: v
            for k,v in event.items()
            if k in {"event", "tool", "call_id", "ok", "turn", "reason"}
        }
        safe["time"] = datetime.now(timezone.utc).isoformat()
        with self._lock, self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(safe, ensure_ascii=False) + "\n")












