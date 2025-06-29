# Windows环境依赖安装脚本
# 解决volcengine-python-sdk在Windows上的构建问题

Write-Host "🔧 Windows环境依赖安装脚本" -ForegroundColor Green
Write-Host "正在解决volcengine-python-sdk构建问题..." -ForegroundColor Yellow

# 检查Python版本
$pythonVersion = python --version
Write-Host "Python版本: $pythonVersion" -ForegroundColor Cyan

# 方案1: 清理缓存
Write-Host "`n📁 清理uv缓存..." -ForegroundColor Yellow
try {
    uv cache clean
    Write-Host "✅ 缓存清理成功" -ForegroundColor Green
} catch {
    Write-Host "⚠️ 缓存清理失败，继续尝试其他方案" -ForegroundColor Yellow
}

# 方案2: 删除锁定文件
if (Test-Path "uv.lock") {
    Write-Host "`n🗑️ 删除现有锁定文件..." -ForegroundColor Yellow
    Remove-Item "uv.lock" -Force
    Write-Host "✅ 锁定文件已删除" -ForegroundColor Green
}

# 方案3: 使用特定的环境变量
Write-Host "`n🔧 设置构建环境变量..." -ForegroundColor Yellow
$env:SETUPTOOLS_USE_DISTUTILS = "stdlib"
$env:DISTUTILS_USE_SDK = "1"

# 方案4: 尝试安装特定版本
Write-Host "`n📦 安装项目依赖..." -ForegroundColor Yellow
try {
    # 先尝试安装volcengine-python-sdk的特定版本
    Write-Host "正在安装volcengine-python-sdk..." -ForegroundColor Cyan
    uv add "volcengine-python-sdk[ark]==3.0.155" --force-reinstall
    
    # 再安装其他依赖
    Write-Host "正在同步其他依赖..." -ForegroundColor Cyan  
    uv sync --dev
    
    Write-Host "✅ 依赖安装成功!" -ForegroundColor Green
    
} catch {
    Write-Host "❌ 标准安装失败，尝试备用方案..." -ForegroundColor Red
    
    # 备用方案: 使用pip安装有问题的包
    Write-Host "`n🔄 使用pip安装volcengine-python-sdk..." -ForegroundColor Yellow
    try {
        pip install "volcengine-python-sdk[ark]==3.0.155" --force-reinstall
        uv sync --dev --no-build-isolation
        Write-Host "✅ 备用安装方案成功!" -ForegroundColor Green
    } catch {
        Write-Host "❌ 所有安装方案都失败" -ForegroundColor Red
        Write-Host "请尝试以下手动解决方案:" -ForegroundColor Yellow
        Write-Host "1. 更新uv: curl -LsSf https://astral.sh/uv/install.sh | sh" -ForegroundColor White
        Write-Host "2. 重启PowerShell" -ForegroundColor White
        Write-Host "3. 运行: uv --version 检查版本" -ForegroundColor White
        Write-Host "4. 重新运行此脚本" -ForegroundColor White
        exit 1
    }
}

# 验证安装
Write-Host "`n🧪 验证安装..." -ForegroundColor Yellow
try {
    uv run python -c "import volcenginesdkarkruntime; print('✅ volcengine-python-sdk导入成功')"
    uv run python -c "import pydantic; print('✅ pydantic导入成功')"
    uv run python -c "import dotenv; print('✅ python-dotenv导入成功')"
    uv run python -c "import openpyxl; print('✅ openpyxl导入成功')"
    
    Write-Host "`n🎉 所有依赖安装和验证成功!" -ForegroundColor Green
    Write-Host "现在您可以运行: uv run python meeting_extractor.py --help" -ForegroundColor Cyan
    
} catch {
    Write-Host "❌ 依赖验证失败" -ForegroundColor Red
    Write-Host "请检查错误信息并重试" -ForegroundColor Yellow
}

Write-Host "`n📝 如果问题持续存在，请查看 docs/BUILD_AND_RELEASE.md 中的故障排除部分" -ForegroundColor Cyan 