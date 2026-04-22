"""
统一工具定义 - 让工具可以在 OpenClaw 和 Hermes 之间无缝迁移
"""

import inspect
import json
from typing import Any, Callable, Dict, List, Optional, get_type_hints
from dataclasses import dataclass, field
from functools import wraps
import re


@dataclass
class ParameterSchema:
    """参数定义"""
    name: str
    type: str
    required: bool = True
    description: str = ""
    default: Any = None
    enum: Optional[List[Any]] = None
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "type": self.type,
            "required": self.required,
            "description": self.description,
            "default": self.default,
            "enum": self.enum,
        }


@dataclass
class Tool:
    """
    统一工具定义装饰器
    
    Example:
        @Tool(
            name="weather_check",
            description="Get current weather for a location",
            parameters={
                "location": {"type": "string", "required": True}
            }
        )
        def check_weather(location: str) -> dict:
            return {"temp": 25, "condition": "sunny"}
    """
    name: str
    description: str
    parameters: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    category: str = "general"
    version: str = "1.0.0"
    author: str = ""
    
    def __call__(self, func: Callable) -> "ToolWrapper":
        return ToolWrapper(func, self)


@dataclass
class ToolWrapper:
    """工具包装器，保留原始函数功能"""
    func: Callable
    tool: Tool
    _registry: Optional["ToolRegistry"] = None
    
    def __post_init__(self):
        # 自动从函数签名提取参数信息
        self._extract_params_from_signature()
        # 复制函数元数据
        wraps(self.func)(self)
    
    def _extract_params_from_signature(self):
        """从函数签名自动提取参数"""
        sig = inspect.signature(self.func)
        type_hints = get_type_hints(self.func)
        
        for param_name, param in sig.parameters.items():
            if param_name in self.tool.parameters:
                # 合并用户定义和自动提取的信息
                existing = self.tool.parameters[param_name]
                if "type" not in existing and param_name in type_hints:
                    existing["type"] = self._python_type_to_string(type_hints[param_name])
                if "default" not in existing and param.default != inspect.Parameter.empty:
                    existing["default"] = param.default
            else:
                # 自动添加新参数
                param_type = type_hints.get(param_name, Any)
                self.tool.parameters[param_name] = {
                    "type": self._python_type_to_string(param_type),
                    "required": param.default == inspect.Parameter.empty,
                }
                if param.default != inspect.Parameter.empty:
                    self.tool.parameters[param_name]["default"] = param.default
    
    def _python_type_to_string(self, t) -> str:
        """Python 类型转字符串"""
        type_map = {
            str: "string",
            int: "integer",
            float: "number",
            bool: "boolean",
            list: "array",
            dict: "object",
            Any: "any",
        }
        return type_map.get(t, "string")
    
    def __call__(self, *args, **kwargs):
        """执行工具"""
        return self.func(*args, **kwargs)
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "name": self.tool.name,
            "description": self.tool.description,
            "parameters": self.tool.parameters,
            "tags": self.tool.tags,
            "category": self.tool.category,
            "version": self.tool.version,
            "author": self.tool.author,
        }
    
    def to_json(self, indent: int = 2) -> str:
        """转换为 JSON 字符串"""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
    
    def register(self, registry: "ToolRegistry"):
        """注册到工具注册表"""
        registry.add(self)
        self._registry = registry
        return self


class ToolRegistry:
    """工具注册表 - 管理所有已注册的工具"""
    
    def __init__(self, name: str = "default"):
        self.name = name
        self._tools: Dict[str, ToolWrapper] = {}
    
    def add(self, tool: ToolWrapper):
        """添加工具"""
        self._tools[tool.tool.name] = tool
    
    def get(self, name: str) -> Optional[ToolWrapper]:
        """获取工具"""
        return self._tools.get(name)
    
    def remove(self, name: str) -> bool:
        """移除工具"""
        if name in self._tools:
            del self._tools[name]
            return True
        return False
    
    def list(self, category: Optional[str] = None, tags: Optional[List[str]] = None) -> List[ToolWrapper]:
        """列出工具，支持过滤"""
        tools = list(self._tools.values())
        
        if category:
            tools = [t for t in tools if t.tool.category == category]
        
        if tags:
            tools = [t for t in tools if any(tag in t.tool.tags for tag in tags)]
        
        return tools
    
    def to_dict(self) -> dict:
        """导出为字典"""
        return {
            "name": self.name,
            "tools": {name: tool.to_dict() for name, tool in self._tools.items()},
        }
    
    def save(self, path: str):
        """保存到文件"""
        import json
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load(cls, path: str) -> "ToolRegistry":
        """从文件加载"""
        import json
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        registry = cls(name=data.get("name", "default"))
        # 注意：加载的工具无法恢复原始函数，只保留元数据
        return registry


# 快捷函数
def create_tool(
    name: str,
    description: str,
    func: Callable,
    parameters: Optional[Dict[str, Dict[str, Any]]] = None,
    tags: Optional[List[str]] = None,
) -> ToolWrapper:
    """快速创建工具"""
    tool = Tool(
        name=name,
        description=description,
        parameters=parameters or {},
        tags=tags or [],
    )
    return tool(func)
