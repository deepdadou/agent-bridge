"""
Agent Bridge - 让 OpenClaw 和 Hermes Agent 共享技能/工具的统一桥接器

Usage:
    from agent_bridge import Tool, convert_to_openclaw, convert_to_hermes
"""

__version__ = "0.1.0"
__author__ = "大豆 <soad666p>"
__license__ = "MIT"

from .tool import Tool, ToolRegistry
from .converter import Converter, convert_to_openclaw, convert_to_hermes
from .openclaw import OpenClawAdapter
from .hermes import HermesAdapter
from .cli import main as cli_main

__all__ = [
    "Tool",
    "ToolRegistry", 
    "Converter",
    "convert_to_openclaw",
    "convert_to_hermes",
    "OpenClawAdapter",
    "HermesAdapter",
    "cli_main",
]
