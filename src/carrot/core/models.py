from dataclasses import dataclass, field
from typing import Any, Protocol


#消息列表
Message = dict[str,Any]



@dataclass(frozen=True)
class ToolCall:
    """
    call = ToolCall(
    id="call_001",
    name="read_file",
    arguments={"path": "README.md"},
)
    """
    name:str
    id:str
    argument:dict[str,Any]



@dataclass(frozen=True)
class ModelReply:
    """
    reply = ModelReply(
    text="我先读取项目说明。",
    calls=[call],
)
    """
    text: str = ""
    calls: list[ToolCall] = field(default_factory=list)

    def message(self) -> Message:
        """转换成可加入对话历史的助手消息。"""
        content: list[dict[str,Any]] = []

        if self.text:
            content.append({"type":"text","text":self.text})


        content.extend(
            {"type": "tool_use",
             "id": c.id,
             "name": c.name,
             "input": c.arguments
             }
            for c in self.calls
        )


        """
        {
            "role": "assistant",
            "content": 
            [
                {"type": "text", "text": "我先读取项目说明。"},
                {
                    "type": "tool_use",
                    "id": "call_001",
                    "name": "read_file",
                    "input": {"path": "README.md"},
                },
            ],
        }
        """
        return {"role": "assistant",
                "content": content or [{"type": "text", "text": "(空回复)"}]
                }



#规定 Carrot 使用的模型对象需要提供什么方法
class Model(Protocol):
    def complete(self,
                 system: str,
                 messages: list[Message],
                 tools: list[dict]
                 ) -> ModelReply: ...






