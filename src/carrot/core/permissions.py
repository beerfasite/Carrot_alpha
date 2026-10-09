from pathlib import Path
from typing import Callable
"""
检查路径文件合法+工具使用合法
"""

class Workspace:

    def __init__(self,root:Path):
        self.root = root.resolve()
        self.root.mkdir(parents=True,exist_ok=True)

    def resolve(self,path:str,*,internal:bool = False) -> Path:
        """
        校验路径满足两个if
        """
        target = (self.root / path).resolve()
        if not target.is_relative_to(self.root):
            raise PermissionError("路径超出工作目录")
        relative = target.relative_to(self.root)

        if not internal and any(
            p in {".carrot",".git",".env"} or p.startswith(".env.")
            for p in relative.parts
        ):
            raise PermissionError("该路径属于内部状态或者敏感配置")
        return target



class PermissionPolicy:

    def __init__(self,
                 *,
                 readonly:bool = False,
                 allow_shell:bool = False,
                 approve: Callable[[str,dict],bool] | None = None
                 ):
        self.readonly = readonly
        self.allow_shell = allow_shell
        self.approve = approve

    def check(self,name:str,risk:str,arguments:dict) -> None:
        if risk == "read":
            return
        if self.readonly:
            raise PermissionError("子任务只读策略拒绝此操作")
        if risk == "write":
            return
        if risk == "shell" and not self.allow_shell:
            raise PermissionError("Shell默认关闭：设置CARROT_ALLOW_SHELL = true后逐步确认")
        if self.approve is None or not self.approve(name,arguments):
            raise PermissionError("该操作需要用户确认")











