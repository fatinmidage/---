# 构建和发布指南

本文档说明如何使用GitHub Actions自动构建和发布多平台的会议侠可执行程序。

## 🚀 自动化工作流

### 1. 持续集成 (CI)

**文件**: `.github/workflows/ci.yml`

**触发条件**:
- 推送到 `main` 或 `develop` 分支
- 创建针对 `main` 或 `develop` 分支的Pull Request

**功能**:
- ✅ 代码格式检查 (black, isort)
- ✅ 代码质量检查 (flake8)
- ✅ 语法检查
- ✅ 多平台构建测试 (Windows, macOS, Linux)
- ✅ 依赖安全检查

### 2. 构建和发布 (Build & Release)

**文件**: `.github/workflows/build-release.yml`

**触发条件**:
- 推送Git标签 (如 `v1.0.0`)
- 手动触发 (workflow_dispatch)

**功能**:
- 🔨 多平台构建 (Windows/macOS/Linux)
- 📦 生成可执行文件
- 🚀 创建GitHub Release
- 📝 自动生成更新日志

## 📋 发布流程

### 方法1: 使用Git标签触发 (推荐)

1. **更新版本号**
   ```bash
   # 在pyproject.toml中更新version字段
   vim pyproject.toml
   ```

2. **提交更改**
   ```bash
   git add .
   git commit -m "chore: bump version to v1.0.0"
   git push origin main
   ```

3. **创建并推送标签**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

4. **自动构建和发布**
   - GitHub Actions会自动开始构建
   - 构建完成后会创建GitHub Release
   - 用户可以从Release页面下载对应平台的可执行文件

### 方法2: 手动触发

1. **访问GitHub Actions页面**
   - 进入项目的GitHub页面
   - 点击 "Actions" 标签页
   - 选择 "构建和发布多平台可执行程序" 工作流

2. **手动触发**
   - 点击 "Run workflow" 按钮
   - 输入版本号 (如 `v1.0.0`)
   - 点击绿色的 "Run workflow" 按钮

## 🔧 本地构建

如果您需要在本地进行构建测试：

### 环境准备

```bash
# 安装uv包管理器
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装项目依赖
uv sync --dev
```

### 构建命令

```bash
# 构建当前平台的可执行文件
uv run python build.py

# 显示构建帮助
uv run python build.py --help

# 清理构建文件
uv run python build.py clean

# 显示详细构建日志
uv run python build.py --debug
```

## 📦 构建产物

构建完成后，会在 `dist/` 目录下生成对应平台的可执行文件：

- **Windows**: `meeting_extractor_windows.exe`
- **macOS**: `meeting_extractor_macos`
- **Linux**: `meeting_extractor_linux`

## 🎯 发布内容

GitHub Release会包含：

### 可执行文件
- Windows版本 (.exe)
- macOS版本 (可执行文件)
- Linux版本 (可执行文件)

### 发布说明
- 📦 下载链接
- 🚀 使用方法
- 📋 功能特性
- 🔧 技术信息 (Python版本、构建时间、提交哈希)

## ⚙️ 工作流配置

### 环境变量

- `PYTHON_VERSION`: Python版本 (默认: 3.11)

### 矩阵构建

支持的操作系统：
- `ubuntu-latest` → Linux版本
- `windows-latest` → Windows版本  
- `macos-latest` → macOS版本

### 构建步骤

1. **检出代码** - 获取源代码
2. **设置Python环境** - 安装指定版本的Python
3. **安装uv包管理器** - 安装快速的Python包管理器
4. **安装项目依赖** - 安装所有必需的依赖包
5. **运行构建脚本** - 使用PyInstaller构建可执行文件
6. **验证构建产物** - 检查生成的文件
7. **上传构建产物** - 保存构建结果
8. **创建GitHub Release** - 发布新版本

## 🐛 故障排除

### 构建失败

1. **检查依赖**
   - 确保所有依赖都在`pyproject.toml`中正确配置
   - 检查`uv.lock`文件是否是最新的

2. **检查构建脚本**
   - 确保`build.py`可以在本地正常运行
   - 检查PyInstaller相关配置

3. **检查平台特定问题**
   - **Windows**: 路径分隔符、可执行文件扩展名、包构建问题
   - **macOS**: 权限问题、签名问题
   - **Linux**: 动态库依赖

#### Windows平台特殊问题

如果遇到`volcengine-python-sdk`构建失败的错误：

**错误症状**:
```
x Failed to build `volcengine-python-sdk==4.0.2`
系统找不到指定的文件。 (os error 2)
```

**解决方案**:

1. **使用自动化脚本** (推荐)
   ```bash
   # 双击运行
   install-windows.bat
   
   # 或者PowerShell中运行
   .\scripts\install-windows.ps1
   ```

2. **手动解决**
   ```bash
   # 清理缓存
   uv cache clean
   
   # 删除锁定文件
   rm uv.lock
   
   # 重新安装
   uv sync --dev
   ```

3. **使用固定版本**
   - 项目已经固定`volcengine-python-sdk`版本为`3.0.155`
   - 如果仍有问题，可尝试手动安装：
   ```bash
   pip install "volcengine-python-sdk[ark]==3.0.155" --force-reinstall
   uv sync --dev --no-build-isolation
   ```

### 发布失败

1. **权限问题**
   - 确保`GITHUB_TOKEN`有足够的权限
   - 检查仓库设置中的Actions权限

2. **标签问题**
   - 确保标签格式正确 (如`v1.0.0`)
   - 避免重复的标签名

## 📚 相关资源

- [GitHub Actions文档](https://docs.github.com/en/actions)
- [PyInstaller文档](https://pyinstaller.readthedocs.io/)
- [uv包管理器](https://docs.astral.sh/uv/)
- [Python项目配置](https://packaging.python.org/en/latest/specifications/pyproject-toml/) 