@echo off
chcp 65001 >nul
echo 🔧 会议侠 - Windows依赖安装工具
echo.

echo 📁 清理uv缓存...
uv cache clean

echo.
echo 🗑️ 删除锁定文件...
if exist "uv.lock" del /f "uv.lock"

echo.
echo 📦 安装项目依赖...
uv sync --dev

echo.
echo 🧪 验证安装...
uv run python -c "import volcenginesdkarkruntime; print('✅ volcengine-python-sdk导入成功')" 2>nul || (
    echo ❌ volcengine-python-sdk导入失败，尝试手动安装...
    pip install "volcengine-python-sdk[ark]==3.0.155" --force-reinstall
    uv sync --dev
)

uv run python -c "import pydantic; print('✅ pydantic导入成功')"
uv run python -c "import dotenv; print('✅ python-dotenv导入成功')"  
uv run python -c "import openpyxl; print('✅ openpyxl导入成功')"

echo.
echo 🎉 安装完成！
echo 现在您可以运行: uv run python meeting_extractor.py --help
echo.
pause 