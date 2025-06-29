#!/usr/bin/env python3
"""
会议纪要提取工具打包脚本
支持Windows、macOS和Linux跨平台打包
使用PyInstaller构建独立可执行文件
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path
from typing import List, Optional


class BuildConfig:
    """构建配置类"""
    
    def __init__(self):
        self.platform_name = self.get_platform_name()
        self.output_name = f"meeting_extractor_{self.platform_name}"
        self.source_file = "meeting_extractor.py"
        self.build_dir = Path("build")
        self.dist_dir = Path("dist")
        
    @staticmethod
    def get_platform_name() -> str:
        """获取平台名称"""
        system = platform.system().lower()
        platform_map = {
            "darwin": "macos",
            "windows": "windows", 
            "linux": "linux"
        }
        return platform_map.get(system, system)
    
    def get_pyinstaller_args(self) -> List[str]:
        """获取PyInstaller命令参数"""
        args = [
            "pyinstaller",
            "--onefile",                    # 单文件模式
            "--name", self.output_name,     # 输出文件名
            "--clean",                      # 清理临时文件
            "--noconfirm",                  # 不询问覆盖
            "--console",                    # 控制台应用
            "--optimize", "2",              # 字节码优化级别
            "--add-data", "env_template:.", # 包含环境变量模板
            self.source_file               # 源文件
        ]
        
        # 平台特定配置
        if self.platform_name == "windows":
            args.extend([
                "--icon", "NONE",           # 无图标
                "--version-file", "NONE"    # 无版本信息文件
            ])
        elif self.platform_name == "macos":
            args.extend([
                "--osx-bundle-identifier", "com.meetingextractor.app"
            ])
        
        return args


def check_dependencies() -> bool:
    """检查构建依赖"""
    print("🔍 检查构建依赖...")
    
    # 检查PyInstaller
    try:
        result = subprocess.run(
            ["pyinstaller", "--version"], 
            check=True, 
            capture_output=True, 
            text=True
        )
        print(f"   ✅ PyInstaller: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("   ❌ PyInstaller未安装")
        print("   💡 安装方法: uv add pyinstaller")
        return False
    
    # 检查Python版本
    version = sys.version_info
    if version.major != 3 or version.minor < 10:
        print(f"   ❌ Python版本过低: {version.major}.{version.minor}")
        print("   💡 需要Python 3.10+")
        return False
    
    print(f"   ✅ Python: {version.major}.{version.minor}.{version.micro}")
    return True


def check_source_files(config: BuildConfig) -> bool:
    """检查源文件"""
    print("📁 检查源文件...")
    
    if not Path(config.source_file).exists():
        print(f"   ❌ 源文件不存在: {config.source_file}")
        return False
    
    print(f"   ✅ 源文件: {config.source_file}")
    
    # 检查环境变量模板
    if not Path("env_template").exists():
        print("   ⚠️  环境变量模板不存在: env_template")
        print("   💡 建议创建env_template文件")
    else:
        print("   ✅ 环境变量模板: env_template")
    
    return True


def build_executable(config: BuildConfig) -> bool:
    """构建可执行文件"""
    print(f"🔨 开始构建 ({config.platform_name})...")
    print(f"   输出文件: {config.output_name}")
    
    # 获取构建命令
    cmd = config.get_pyinstaller_args()
    print(f"   命令: {' '.join(cmd)}")
    
    try:
        # 执行构建
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            text=True,
            universal_newlines=True
        )
        
        # 实时显示输出
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output and "--debug" in sys.argv:
                print(f"   {output.strip()}")
        
        # 检查构建结果
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, cmd)
        
        print("   ✅ 构建成功!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"   ❌ 构建失败: 退出码 {e.returncode}")
        return False
    except Exception as e:
        print(f"   ❌ 构建过程出错: {e}")
        return False


def post_build_info(config: BuildConfig) -> None:
    """显示构建后信息"""
    print("📊 构建结果...")
    
    # 查找生成的可执行文件
    exe_files = list(config.dist_dir.glob(f"{config.output_name}*"))
    
    if not exe_files:
        print("   ❌ 未找到生成的可执行文件")
        return
    
    exe_file = exe_files[0]
    file_size = exe_file.stat().st_size / 1024 / 1024
    
    print(f"   📦 可执行文件: {exe_file}")
    print(f"   📏 文件大小: {file_size:.1f} MB")
    
    # 使用说明
    print("\n=== 使用说明 ===")
    print("1. 将可执行文件复制到目标机器")
    print("2. 创建 .env 文件，配置 ARK_API_KEY")
    print("3. 准备会议记录文本文件")
    if config.platform_name == "windows":
        print(f"4. 运行: {exe_file.name} meeting_notes.txt")
    else:
        print(f"4. 运行: ./{exe_file.name} meeting_notes.txt")


def clean_build_files(config: BuildConfig) -> None:
    """清理构建文件"""
    print("🧹 清理构建文件...")
    
    cleanup_items = [
        config.build_dir,
        config.dist_dir,
        Path("__pycache__"),
        *Path(".").glob("*.spec")
    ]
    
    for item in cleanup_items:
        if item.exists():
            if item.is_dir():
                shutil.rmtree(item)
                print(f"   🗑️  删除目录: {item}")
            else:
                item.unlink()
                print(f"   🗑️  删除文件: {item}")
    
    print("   ✅ 清理完成")


def print_help():
    """显示帮助信息"""
    print("""
=== 会议纪要提取工具 - 构建脚本 ===

用法:
  python build.py              # 构建可执行文件
  python build.py clean        # 清理构建文件
  python build.py --debug      # 显示详细构建日志
  python build.py --help       # 显示帮助

支持平台:
  - Windows (exe)
  - macOS (可执行文件)
  - Linux (可执行文件)

构建要求:
  - Python 3.10+
  - PyInstaller
  - 项目依赖已安装

""")


def main():
    """主函数"""
    # 处理参数
    if "--help" in sys.argv or "-h" in sys.argv:
        print_help()
        return
    
    if "clean" in sys.argv:
        config = BuildConfig()
        clean_build_files(config)
        return
    
    # 开始构建
    print("=== 会议纪要提取工具 - 构建工具 ===")
    
    config = BuildConfig()
    print(f"🖥️  目标平台: {config.platform_name}")
    print()
    
    # 检查依赖和源文件
    if not check_dependencies():
        sys.exit(1)
    
    if not check_source_files(config):
        sys.exit(1)
    
    print()
    
    # 构建可执行文件
    if build_executable(config):
        post_build_info(config)
        print("\n🎉 构建完成!")
        print("\n💡 如需清理构建文件，运行: python build.py clean")
    else:
        print("\n💥 构建失败!")
        print("💡 尝试运行: python build.py --debug 查看详细日志")
        sys.exit(1)


if __name__ == "__main__":
    main() 