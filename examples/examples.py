"""
示例工具 - 展示如何使用 Agent Bridge

这些示例展示了如何定义工具并转换为不同格式。
"""

from agent_bridge import Tool


# ========== 示例 1: 天气查询工具 ==========

@Tool(
    name="weather_check",
    description="Get current weather for a location using wttr.in",
    parameters={
        "location": {
            "type": "string",
            "required": True,
            "description": "City name or location"
        },
        "format": {
            "type": "string",
            "required": False,
            "default": "json",
            "description": "Output format (json/text)"
        }
    },
    tags=["weather", "api"],
    category="utility",
    author="Agent Bridge Examples",
)
def weather_check(location: str, format: str = "json") -> dict:
    """获取天气信息"""
    import requests
    
    if format == "text":
        url = f"https://wttr.in/{location}"
    else:
        url = f"https://wttr.in/{location}?format=j1"
    
    response = requests.get(url)
    response.raise_for_status()
    
    if format == "text":
        return {"text": response.text}
    else:
        return response.json()


# ========== 示例 2: 网络搜索工具 ==========

@Tool(
    name="web_search",
    description="Search the web using SearXNG or Brave Search",
    parameters={
        "query": {
            "type": "string",
            "required": True,
            "description": "Search query"
        },
        "count": {
            "type": "integer",
            "required": False,
            "default": 10,
            "description": "Number of results (1-10)"
        },
        "engine": {
            "type": "string",
            "required": False,
            "default": "searxng",
            "description": "Search engine (searxng/brave)"
        }
    },
    tags=["search", "web"],
    category="search",
    author="Agent Bridge Examples",
)
def web_search(query: str, count: int = 10, engine: str = "searxng") -> list:
    """执行网络搜索"""
    if engine == "brave":
        # Brave Search API
        import os
        api_key = os.environ.get("BRAVE_API_KEY")
        if not api_key:
            return {"error": "BRAVE_API_KEY not set"}
        
        import requests
        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {"X-Subscription-Token": api_key}
        params = {"q": query, "count": min(count, 10)}
        
        response = requests.get(url, headers=headers, params=params)
        results = response.json().get("web", {}).get("results", [])
        
        return [{"title": r["title"], "url": r["url"], "snippet": r["description"]} for r in results[:count]]
    
    else:
        # SearXNG (local)
        import subprocess
        searxng_url = os.environ.get("SEARXNG_URL", "http://localhost:8080")
        
        result = subprocess.run(
            ["curl", "-s", f"{searxng_url}/search?q={query}&format=json"],
            capture_output=True,
            text=True
        )
        
        data = result.stdout
        import json
        results = json.loads(data).get("results", [])
        
        return [{"title": r["title"], "url": r["url"], "snippet": r["content"]} for r in results[:count]]


# ========== 示例 3: 文件操作工具 ==========

@Tool(
    name="file_operations",
    description="Read, write, and manage files in the workspace",
    parameters={
        "action": {
            "type": "string",
            "required": True,
            "description": "Action to perform (read/write/list)"
        },
        "path": {
            "type": "string",
            "required": True,
            "description": "File or directory path"
        },
        "content": {
            "type": "string",
            "required": False,
            "description": "Content to write (for write action)"
        }
    },
    tags=["files", "workspace"],
    category="utility",
    author="Agent Bridge Examples",
)
def file_operations(action: str, path: str, content: str = None) -> dict:
    """文件操作"""
    from pathlib import Path
    
    file_path = Path(path)
    
    if action == "read":
        if not file_path.exists():
            return {"error": f"File not found: {path}"}
        return {"content": file_path.read_text(encoding="utf-8")}
    
    elif action == "write":
        if content is None:
            return {"error": "Content required for write action"}
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return {"success": True, "path": str(file_path)}
    
    elif action == "list":
        if not file_path.is_dir():
            return {"error": f"Not a directory: {path}"}
        files = [str(f) for f in file_path.iterdir()]
        return {"files": files}
    
    else:
        return {"error": f"Unknown action: {action}"}


# ========== 示例 4: 代码执行工具 ==========

@Tool(
    name="code_runner",
    description="Execute Python code safely in a sandbox",
    parameters={
        "code": {
            "type": "string",
            "required": True,
            "description": "Python code to execute"
        },
        "timeout": {
            "type": "integer",
            "required": False,
            "default": 30,
            "description": "Execution timeout in seconds"
        }
    },
    tags=["code", "execution"],
    category="development",
    author="Agent Bridge Examples",
)
def code_runner(code: str, timeout: int = 30) -> dict:
    """执行 Python 代码"""
    import subprocess
    import tempfile
    import json
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        temp_path = f.name
    
    try:
        # 执行代码
        result = subprocess.run(
            ["python3", temp_path],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"error": f"Execution timeout after {timeout} seconds"}
    finally:
        import os
        os.unlink(temp_path)


# ========== 测试运行 ==========

if __name__ == "__main__":
    print("🧪 Testing Agent Bridge Examples\n")
    
    # 测试天气工具
    print("1. Weather Check:")
    try:
        result = weather_check(location="Beijing")
        print(f"   {result}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # 测试文件操作
    print("\n2. File Operations:")
    try:
        result = file_operations(action="list", path=".")
        print(f"   Files: {len(result.get('files', []))} found")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n✅ All examples loaded successfully!")
