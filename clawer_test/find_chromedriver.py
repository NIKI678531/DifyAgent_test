#!/usr/bin/env python3
"""
查找 ChromeDriver 在系统中的所有可能路径
"""

import os
import shutil
import subprocess
import glob

print("=" * 60)
print("查找 ChromeDriver 路径")
print("=" * 60)
print()

# 1. 检查常见安装路径
print("1️⃣  检查常见安装路径:")
possible_paths = [
    "/usr/local/bin/chromedriver",
    "/opt/homebrew/bin/chromedriver",
    "/usr/bin/chromedriver",
    os.path.expanduser("~/Downloads/chromedriver"),
    os.path.expanduser("~/bin/chromedriver"),
]

found_paths = []
for path in possible_paths:
    if os.path.exists(path):
        found_paths.append(path)
        print(f"   ✓ 找到：{path}")
        
        # 显示详细信息
        try:
            result = subprocess.run([path, "--version"], 
                                  capture_output=True, text=True, timeout=5)
            print(f"      版本：{result.stdout.strip()}")
            
            # 显示文件权限
            stat_info = os.stat(path)
            print(f"      权限：{oct(stat_info.st_mode)[-3:]}")
        except Exception as e:
            print(f"      ⚠ 无法获取版本信息：{e}")
    else:
        print(f"   ✗ 不存在：{path}")

print()

# 1.5 检查 Homebrew Caskroom
print("1️⃣.5  检查 Homebrew Caskroom:")
caskroom_pattern = "/opt/homebrew/Caskroom/chromedriver/*/chromedriver-mac-*/chromedriver"
caskroom_paths = glob.glob(caskroom_pattern)
if caskroom_paths:
    # 按版本排序，取最新的
    caskroom_paths.sort(reverse=True)
    latest_caskroom = caskroom_paths[0]
    if latest_caskroom not in found_paths:
        found_paths.append(latest_caskroom)
        print(f"   ✓ 找到：{latest_caskroom}")

        # 显示详细信息
        try:
            result = subprocess.run([latest_caskroom, "--version"],
                                  capture_output=True, text=True, timeout=5)
            print(f"      版本：{result.stdout.strip()}")

            # 显示文件权限
            stat_info = os.stat(latest_caskroom)
            print(f"      权限：{oct(stat_info.st_mode)[-3:]}")
        except Exception as e:
            print(f"      ⚠ 无法获取版本信息：{e}")
else:
    print(f"   ✗ 未在 Homebrew Caskroom 中找到 chromedriver")

print()

# 2. 检查 PATH 环境变量
print("2️⃣  检查 PATH 环境变量中的 chromedriver:")
chromedriver_in_path = shutil.which('chromedriver')
if chromedriver_in_path:
    print(f"   ✓ 在 PATH 中找到：{chromedriver_in_path}")
    
    # 尝试获取版本
    try:
        result = subprocess.run([chromedriver_in_path, "--version"], 
                              capture_output=True, text=True, timeout=5)
        print(f"      版本：{result.stdout.strip()}")
    except:
        pass
else:
    print(f"   ✗ PATH 中未找到 chromedriver")

print()

# 3. 使用 which/whereis 命令查找
print("3️⃣  使用系统命令查找:")
try:
    # which 命令
    result = subprocess.run(["which", "chromedriver"], 
                          capture_output=True, text=True)
    if result.stdout.strip():
        print(f"   which 命令结果：{result.stdout.strip()}")
    else:
        print(f"   which 命令：未找到")
except:
    print(f"   which 命令：执行失败")

try:
    # whereis 命令
    result = subprocess.run(["whereis", "chromedriver"], 
                          capture_output=True, text=True)
    if result.stdout.strip():
        print(f"   whereis 命令结果：{result.stdout.strip()}")
    else:
        print(f"   whereis 命令：未找到")
except:
    print(f"   whereis 命令：执行失败")

print()

# 4. 使用 find 命令搜索（较慢）
print("4️⃣  使用 find 命令搜索 /usr 和 /opt 目录 (可能需要几秒):")
try:
    result = subprocess.run(
        ["find", "/usr", "/opt", "-name", "chromedriver", "-type", "f"],
        capture_output=True, text=True, timeout=10
    )
    if result.stdout.strip():
        paths = result.stdout.strip().split('\n')
        for p in paths:
            print(f"   找到：{p}")
    else:
        print(f"   未找到其他 chromedriver 文件")
except subprocess.TimeoutExpired:
    print(f"   搜索超时...")
except Exception as e:
    print(f"   搜索失败：{e}")

print()

# 5. 总结
print("=" * 60)
print("总结:")
print("=" * 60)
if found_paths:
    print(f"✓ 共找到 {len(found_paths)} 个 ChromeDriver 文件:")
    for i, path in enumerate(found_paths, 1):
        print(f"   {i}. {path}")
    
    print(f"\n推荐使用的路径:")
    if chromedriver_in_path:
        print(f"   → {chromedriver_in_path} (在 PATH 中，优先级最高)")
    elif "/opt/homebrew/bin/chromedriver" in found_paths:
        print(f"   → /opt/homebrew/bin/chromedriver (Homebrew 安装)")
    elif "/usr/local/bin/chromedriver" in found_paths:
        print(f"   → /usr/local/bin/chromedriver (传统 macOS 路径)")
else:
    print("✗ 未在系统中找到 ChromeDriver")
    print("\n建议:")
    print("   1. 使用 Homebrew 安装：brew install --cask chromedriver")
    print("   2. 或手动下载并放到 /usr/local/bin/chromedriver")

print()
