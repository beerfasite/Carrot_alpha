"""工作区进程锁，防止多个交互会话同时修改本地执行状态。"""

import fcntl
from pathlib import Path


class WorkspaceLock:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self._file = path.open("a+b")
        try:
            fcntl.flock(self._file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            self._file.close()
            raise RuntimeError(
                "该工作区已有 Carrot 会话运行；退出已有会话，或使用其他工作区。"
            ) from None

    def close(self):
        if not self._file.closed:
            fcntl.flock(self._file.fileno(), fcntl.LOCK_UN)
            self._file.close()
