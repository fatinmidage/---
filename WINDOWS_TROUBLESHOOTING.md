# Windows平台故障排除指南

## 🚨 常见问题：volcengine-python-sdk构建失败

### 错误症状
```
x Failed to build `volcengine-python-sdk==4.0.2`
系统找不到指定的文件。 (os error 2)
```

### 💡 快速解决方案

#### 方案1: 一键修复脚本 (推荐)

**双击运行**:
```
install-windows.bat
```

**或者在PowerShell中**:
```powershell
.\scripts\install-windows.ps1
```

#### 方案2: 手动命令

```bash
# 1. 清理缓存
uv cache clean

# 2. 删除锁定文件
del uv.lock

# 3. 重新安装
uv sync --dev
```

#### 方案3: 使用pip辅助安装

```bash
# 如果方案2仍然失败，先用pip安装问题包
pip install "volcengine-python-sdk[ark]==3.0.155" --force-reinstall

# 然后同步其他依赖
uv sync --dev --no-build-isolation
```

### 🔧 环境检查

运行以下命令检查环境：

```bash
# 检查Python版本 (需要3.10+)
python --version

# 检查uv版本
uv --version

# 检查是否在正确目录
ls pyproject.toml
```

### 📋 验证安装

安装完成后，运行以下命令验证：

```bash
# 验证依赖导入
uv run python -c "import volcenginesdkarkruntime; print('✅ volcengine-python-sdk导入成功')"
uv run python -c "import pydantic; print('✅ pydantic导入成功')"
uv run python -c "import dotenv; print('✅ python-dotenv导入成功')"
uv run python -c "import openpyxl; print('✅ openpyxl导入成功')"

# 测试主程序
uv run python meeting_extractor.py --help
```

### 🛠️ 高级故障排除

如果上述方案都无效，请尝试：

1. **更新uv到最新版本**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **检查Windows开发工具**:
   - 确保安装了Microsoft C++ Build Tools
   - 或者安装Visual Studio Community

3. **使用虚拟环境**:
   ```bash
   uv venv
   uv pip install -r requirements.txt
   ```

4. **联系支持**:
   - 在GitHub Issues中描述详细错误信息
   - 包含Windows版本和Python版本信息

### 📚 相关资源

- [详细构建指南](docs/BUILD_AND_RELEASE.md)
- [项目README](README.md)
- [GitHub Issues](https://github.com/你的用户名/会议侠/issues)

---

**💡 提示**: 这个问题主要是由于volcengine-python-sdk在Windows平台的构建兼容性问题。我们已经固定了一个稳定的版本(3.0.155)来解决这个问题。 