# 贡献指南

欢迎为 **Agent Bridge** 贡献代码！🎉

## 快速开始

### 1. Fork 项目

```bash
# 在 GitHub 上 Fork 本项目
# 然后克隆你的 Fork
git clone https://github.com/YOUR_USERNAME/agent-bridge.git
cd agent-bridge
```

### 2. 设置开发环境

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装开发依赖
pip install -e ".[dev]"
```

### 3. 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_agent_bridge.py -v

# 查看测试覆盖率
pytest --cov=agent_bridge --cov-report=html
```

### 4. 代码格式化

```bash
# 格式化代码
black src/ tests/

# 代码检查
ruff check src/ tests/

# 类型检查
mypy src/
```

## 贡献流程

### 提交 Issue

- 报告 Bug：提供详细的复现步骤
- 功能建议：说明使用场景和期望行为
- 问题咨询：尽量提供上下文信息

### 提交 PR

1. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **编写代码**
   - 遵循现有代码风格
   - 添加必要的测试
   - 更新文档

3. **提交代码**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

4. **推送并创建 PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## 提交信息规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码格式（不影响功能）
- `refactor:` 重构
- `test:` 测试相关
- `chore:` 构建/工具相关

示例：
```
feat: add SearXNG search tool converter
fix: resolve parameter parsing issue in Hermes adapter
docs: update README with installation instructions
```

## 开发新工具

### 使用 CLI 创建模板

```bash
agent-bridge create my_tool --template=search
```

### 手动创建

1. 在 `examples/` 目录下创建新文件
2. 使用 `@Tool` 装饰器定义工具
3. 添加测试到 `tests/`
4. 更新文档

### 工具定义示例

```python
from agent_bridge import Tool

@Tool(
    name="my_awesome_tool",
    description="Does something awesome",
    parameters={
        "input": {"type": "string", "required": True}
    },
    tags=["awesome", "utility"],
)
def my_tool(input: str) -> dict:
    """实现你的逻辑"""
    return {"result": f"Processed: {input}"}
```

## 添加新框架支持

要添加对新 Agent 框架的支持：

1. 在 `src/agent_bridge/` 创建新适配器 `newframework.py`
2. 实现 `NewFrameworkAdapter` 类
3. 在 `converter.py` 添加转换方法
4. 在 `cli.py` 添加命令行支持
5. 添加测试和文档

## 文档

- README.md - 项目主文档
- docs/ - 详细文档
- 代码注释 - 使用 docstring

更新文档后，运行：
```bash
# 如果有 MkDocs 配置
mkdocs serve
```

## 发布流程

1. 更新版本号 (`pyproject.toml`)
2. 更新 CHANGELOG.md
3. 创建 Git Tag
4. 发布到 PyPI

```bash
# 构建
python -m build

# 发布到 PyPI
twine upload dist/*
```

## 社区准则

- 🤝 保持友好和尊重
- 💬 用中文或英文交流
- 🐛 报告 Bug 时提供详细信息
- ✨ 欢迎新功能建议
- 📖 文档同样重要

## 许可证

MIT License - 贡献即表示你同意你的代码在此许可证下发布。

---

感谢你的贡献！🌉
