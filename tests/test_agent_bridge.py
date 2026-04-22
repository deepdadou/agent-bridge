"""
Agent Bridge 测试套件
"""

import pytest
from pathlib import Path
import tempfile
import json


class TestTool:
    """测试工具定义"""
    
    def test_tool_creation(self):
        """测试工具创建"""
        from agent_bridge import Tool
        
        @Tool(
            name="test_tool",
            description="A test tool",
            parameters={"param1": {"type": "string", "required": True}}
        )
        def test_func(param1: str) -> str:
            return param1
        
        assert test_func.tool.name == "test_tool"
        assert test_func.tool.description == "A test tool"
        assert "param1" in test_func.tool.parameters
    
    def test_tool_execution(self):
        """测试工具执行"""
        from agent_bridge import Tool
        
        @Tool(
            name="add_tool",
            description="Add two numbers",
            parameters={
                "a": {"type": "number", "required": True},
                "b": {"type": "number", "required": True}
            }
        )
        def add(a: float, b: float) -> float:
            return a + b
        
        result = add(2, 3)
        assert result == 5
    
    def test_tool_to_dict(self):
        """测试工具字典转换"""
        from agent_bridge import Tool
        
        @Tool(
            name="test_tool",
            description="Test",
            tags=["test", "example"],
            category="testing"
        )
        def test_func():
            pass
        
        d = test_func.to_dict()
        assert d["name"] == "test_tool"
        assert d["tags"] == ["test", "example"]
        assert d["category"] == "testing"


class TestConverter:
    """测试格式转换器"""
    
    def test_convert_to_openclaw(self):
        """测试转换为 OpenClaw 格式"""
        from agent_bridge import Tool, Converter
        
        @Tool(
            name="test_skill",
            description="A test skill",
            parameters={"query": {"type": "string", "required": True}}
        )
        def test_func(query: str) -> str:
            return query
        
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_path = Converter.to_openclaw(test_func, tmpdir)
            
            assert Path(skill_path).exists()
            assert (Path(skill_path) / "SKILL.md").exists()
            assert (Path(skill_path) / "scripts").exists()
    
    def test_convert_to_hermes(self):
        """测试转换为 Hermes 格式"""
        from agent_bridge import Tool, Converter
        
        @Tool(
            name="test_tool",
            description="A test tool",
        )
        def test_func():
            pass
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tool_path = Converter.to_hermes(test_func, tmpdir)
            
            assert Path(tool_path).exists()
            assert (Path(tool_path) / "test_tool.py").exists()
            assert (Path(tool_path) / "__init__.py").exists()


class TestToolRegistry:
    """测试工具注册表"""
    
    def test_registry_add_get(self):
        """测试添加和获取工具"""
        from agent_bridge import Tool, ToolRegistry
        
        registry = ToolRegistry()
        
        @Tool(name="tool1", description="First tool")
        def tool1():
            pass
        
        tool1.register(registry)
        
        retrieved = registry.get("tool1")
        assert retrieved is not None
        assert retrieved.tool.name == "tool1"
    
    def test_registry_list(self):
        """测试列出工具"""
        from agent_bridge import Tool, ToolRegistry
        
        registry = ToolRegistry()
        
        @Tool(name="tool1", description="First", category="cat1", tags=["a"])
        def tool1():
            pass
        
        @Tool(name="tool2", description="Second", category="cat2", tags=["b"])
        def tool2():
            pass
        
        tool1.register(registry)
        tool2.register(registry)
        
        all_tools = registry.list()
        assert len(all_tools) == 2
        
        cat1_tools = registry.list(category="cat1")
        assert len(cat1_tools) == 1
        
        tag_a_tools = registry.list(tags=["a"])
        assert len(tag_a_tools) == 1


class TestOpenClawAdapter:
    """测试 OpenClaw 适配器"""
    
    def test_adapter_init(self):
        """测试适配器初始化"""
        from agent_bridge import OpenClawAdapter
        
        with tempfile.TemporaryDirectory() as tmpdir:
            adapter = OpenClawAdapter(tmpdir)
            assert adapter.workspace == Path(tmpdir)
            assert adapter.skills_dir.exists()


class TestHermesAdapter:
    """测试 Hermes 适配器"""
    
    def test_adapter_init(self):
        """测试适配器初始化"""
        from agent_bridge import HermesAdapter
        
        with tempfile.TemporaryDirectory() as tmpdir:
            adapter = HermesAdapter(tmpdir)
            assert adapter.tools_dir == Path(tmpdir)
            assert adapter.tools_dir.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
