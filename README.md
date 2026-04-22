# 🌉 Agent Bridge

**让 OpenClaw 和 Hermes Agent 共享技能/工具的统一桥接器**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-compatible-green)](https://github.com/openclaw/openclaw)
[![Hermes Compatible](https://img.shields.io/badge/Hermes-compatible-purple)](https://github.com/NousResearch/Hermes-Agent)
[![GitHub Stars](https://img.shields.io/github/stars/deepdadou/agent-bridge?style=flat-square)](https://github.com/deepdadou/agent-bridge/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/deepdadou/agent-bridge?style=flat-square)](https://github.com/deepdadou/agent-bridge/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/deepdadou/agent-bridge?style=flat-square)](https://github.com/deepdadou/agent-bridge/issues)
[![Last Commit](https://img.shields.io/github/last-commit/deepdadou/agent-bridge?style=flat-square)](https://github.com/deepdadou/agent-bridge/commits/main)

---

## 🎯 项目目标

**Agent Bridge** 是一个开源工具桥接器，旨在：

1. **统一技能格式** - 让 OpenClaw Skills 和 Hermes Agent 工具可以互相转换
2. **一次编写，多处运行** - 写一个工具，同时在 OpenClaw 和 Hermes 中使用
3. **简化开发流程** - 提供统一的 SDK 和模板
4. **促进生态互通** - 打破框架壁垒，共享社区成果

---

## 🚀 快速开始

### 安装

```bash
# 从 GitHub 安装
pip install git+https://github.com/soad666p/agent-bridge.git

# 或者克隆后本地安装
git clone https://github.com/soad666p/agent-bridge.git
cd agent-bridge
pip install -e .
```

### 基础用法

```python
from agent_bridge import Tool, convert_to_openclaw, convert_to_hermes

# 定义一个通用工具
@Tool(
    name="weather_check",
    description="Get current weather for a location",
    parameters={
        "location": {"type": "string", "required": True}
    }
)
def check_weather(location: str) -> dict:
    """获取天气信息"""
    import requests
    response = requests.get(f"https://wttr.in/{location}?format=j1")
    return response.json()

# 转换为 OpenClaw Skill 格式
openclaw_skill = convert_to_openclaw(check_weather)
print(openclaw_skill)

# 转换为 Hermes Agent 工具格式
hermes_tool = convert_to_hermes(check_weather)
print(hermes_tool)
```

---

## 📦 核心功能

### 1. 工具定义统一化

使用统一的装饰器定义工具，自动适配不同框架：

```python
from agent_bridge import Tool

@Tool(
    name="web_search",
    description="Search the web using Brave Search API",
    parameters={
        "query": {"type": "string", "required": True, "description": "Search query"},
        "count": {"type": "integer", "required": False, "default": 10}
    },
    tags=["search", "web"]
)
def search_web(query: str, count: int = 10) -> list:
    """执行网络搜索"""
    # 你的实现
    pass
```

### 2. 格式转换

```python
from agent_bridge import Converter

# OpenClaw → Hermes
hermes_format = Converter.openclaw_to_hermes(openclaw_skill_path)

# Hermes → OpenClaw
openclaw_format = Converter.hermes_to_openclaw(hermes_tool_path)

# 批量转换
Converter.batch_convert(source_dir, target_dir, format="openclaw")
```

### 3. 技能市场同步

```python
from agent_bridge import SkillMarket

# 从 ClawHub 同步技能
market = SkillMarket()
skills = market.sync_from_clawhub(category="search")

# 发布到多个平台
market.publish(skills, platforms=["clawhub", "hermes-hub"])
```

---

## 🛠️ CLI 工具

```bash
# 创建新工具模板
agent-bridge create my_tool --template=search

# 转换技能格式
agent-bridge convert ./skills --from openclaw --to hermes --output ./hermes_tools

# 验证工具兼容性
agent-bridge validate ./my_tool.py

# 发布技能
agent-bridge publish ./my_tool --platforms clawhub,hermes

# 同步技能库
agent-bridge sync --source clawhub --dest local
```

---

## 📁 项目结构

```
agent-bridge/
├── src/
│   └── agent_bridge/
│       ├── __init__.py
│       ├── tool.py          # 统一工具定义
│       ├── converter.py     # 格式转换器
│       ├── openclaw.py      # OpenClaw 适配器
│       ├── hermes.py        # Hermes 适配器
│       └── cli.py           # 命令行工具
├── tests/
├── examples/
│   ├── openclaw_skills/
│   └── hermes_tools/
├── docs/
├── pyproject.toml
└── README.md
```

---

## 🔌 支持的框架

| 框架 | 状态 | 版本 |
|------|------|------|
| OpenClaw | ✅ 支持 | v1.0+ |
| Hermes Agent | ✅ 支持 | v0.2+ |
| LangChain | 🔄 计划中 | - |
| LlamaIndex | 🔄 计划中 | - |

---

## 🤝 贡献

欢迎贡献！请查看 [贡献指南](docs/CONTRIBUTING.md)。

```bash
# 开发环境设置
git clone https://github.com/soad666p/agent-bridge.git
cd agent-bridge
pip install -e ".[dev]"

# 运行测试
pytest tests/

# 构建文档
mkdocs serve
```

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🙏 致谢

- [OpenClaw](https://github.com/openclaw/openclaw) - 本地 AI 自动化平台
- [Hermes Agent](https://github.com/NousResearch/Hermes-Agent) - Nous Research 的开源 Agent 框架

---

**让 AI Agent 生态更加开放和互通！** 🌉
