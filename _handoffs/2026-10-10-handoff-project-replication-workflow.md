---
layout: default
title: 交接文档 · Project Replication Workflow
date: 2026-10-13 23:30:00 +0800
---

# Project Replication Workflow

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\software-development\project-replication-workflow\SKILL.md

---
name: project-replication-workflow
description: "Project replication workflow for copying complete implementations from historical sessions to new dates, including Cloudflare D1 data migration"
version: "1.0.0"
tags: ["project", "replication", "migration", "cloudflare", "d1"]
---

# Project Replication Workflow

## Overview

This skill provides a complete workflow for replicating project implementations from historical sessions to new dates, including Cloudflare D1 database migration.

## When to Use

Use this workflow when:
- Need to copy a complete working project from a previous session
- Need to migrate existing data (SQL files, databases) to a new project
- Need to maintain consistency across project versions
- Need to replicate proven implementations quickly

## Quick Start

### Basic Replication

1. **Identify source project**
   ```bash
   ls -la "D:\AI work\workbuddy\2026-07-19-09-49-20\yunnan-housing"
   ```

2. **Create target structure**
   ```bash
   mkdir -p "2026-07-24-11-46-09\yunnan-housing-new\{src,dashboard,local-crawler,backup}"
   ```

3. **Copy files**
   ```bash
   # Copy configuration
   cp "源路径/wrangler.toml" "目标路径/"
   cp "源路径/schema.sql" "目标路径/"
   cp "源路径/README.md" "目标路径/"
   
   # Copy code
   cp -r "源路径/src" "目标路径/"
   cp -r "源路径/dashboard" "目标路径/"
   cp -r "源路径/local-crawler" "目标路径/"
   ```

4. **Update configuration**
   ```bash
   # Edit wrangler.toml
   # Update database_name, database_id, etc.
   ```

5. **Migrate data**
   ```bash
   # Copy SQL files
   cp "源路径/local-crawler/import_data.sql" "目标路径/local-crawler/"
   ```

## Cloudflare D1 Upload

### Direct Upload with Authorization (User Preference)

**Based on your feedback, this is now the PRIMARY method:**

When you want to upload the 7/19 yunnan-housing data to Cloudflare D1, here's the enhanced workflow that meets your requirement of "直接上传, 你给我授权, 需要我登陆, 你弹出网页就行" (Direct upload, give me authorization, need login, you open the webpage):

#### Step 1: Automated Browser Authorization

This script handles the exact workflow you prefer:

```bash
# This is what you want - direct operation after authorization
cd yunnan-housing-new
python scripts/browser-auth.py
```

**The script does EXACTLY what you asked for:**
1. **Automatically opens** Cloudflare login page
2. **Waits for your authorization** (you login manually)
3. **Proceeds with direct upload** once you confirm
4. **Does all the technical work** - no need for manual wrangler commands

#### Step 2: Enhanced Browser Auth Script

Here's the enhanced `scripts/browser-auth.py` that implements your preferred workflow:

```python
#!/usr/bin/env python3
"""
浏览器授权与自动上传工具

此脚本直接响应用户需求："我给你授权, 需要我登陆, 你弹出网页就行"

功能:
1. 打开Cloudflare登录页面
2. 等待用户完成登录授权
3. 自动执行上传任务
4. 无需用户手动执行wrangler命令

使用方法:
cd yunnan-housing-new
python scripts/browser-auth.py
"""

import subprocess
import time
import os
import sys
from datetime import datetime

def log_status(message, status="INFO"):
    """打印状态信息"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{status}] {message}")

def open_browser_and_wait():
    """打开浏览器并等待用户授权登录"""
    log_status("🚀 启动Cloudflare浏览器授权流程")
    log_status("📋 正在打开Cloudflare登录页面...")
    
    try:
        # 在Windows上使用start命令
        subprocess.run(['start', 'https://dash.cloudflare.com/'], 
                      shell=True, check=True)
        log_status("✅ 浏览器已打开: https://dash.cloudflare.com/")
    except Exception as e:
        log_status(f"❌ 无法自动打开浏览器: {e}", "ERROR")
        log_status("💡 请手动访问: https://dash.cloudflare.com/", "WARNING")
        return False
    
    log_status("⏳ 请在浏览器中完成Cloudflare登录授权...")
    log_status("🔑 请确保您已登录到Cloudflare账户")
    log_status("📝 登录完成后，请按Enter键继续自动上传")
    
    try:
        # 等待用户按回车键确认登录
        input("✅ 登录完成请按Enter键继续... ")
        log_status("🎯 检测到用户授权完成，开始执行上传...")
        return True
    except KeyboardInterrupt:
        log_status("⚠️ 用户取消操作", "WARNING")
        return False
    except Exception as e:
        log_status(f"❌ 等待授权时出错: {e}", "ERROR")
        return False

def check_wrangler_availability():
    """检查wrangler的可用性"""
    log_status("🔍 检查wrangler可用性...")
    
    # 尝试使用wrangler命令
    try:
        result = subprocess.run(['wrangler', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            log_status(f"✅ wrangler可用: {result.stdout.strip()}")
            return True
        else:
            log_status("⚠️ wrangler存在但可能配置不正确", "WARNING")
            return False
    except Exception as e:
        log_status(f"❌ wrangler不可用: {e}", "ERROR")
        log_status("💡 请确保wrangler已安装或使用备用方法", "WARNING")
        return False

def execute_upload():
    """执行数据上传"""
    log_status("📤 开始直接上传数据到Cloudflare D1...")
    
    work_dir = os.getcwd()
    sql_file = os.path.join(work_dir, "local-crawler", "import_data.sql")
    
    if not os.path.exists(sql_file):
        log_status(f"❌ 未找到SQL文件: {sql_file}", "ERROR")
        return False
    
    file_size = os.path.getsize(sql_file)
    log_status(f"📋 文件: {sql_file}")
    log_status(f"📊 文件大小: {file_size:,} 字节 ({file_size/1024/1024:.1f} MB)")
    
    try:
        # 执行wrangler上传命令 - 这就是你想要的“直接上传”
        cmd = ['wrangler', 'd1', 'execute', 'yunnan-housing-new-db', 
               '--file', sql_file]
        
        log_status("🔄 正在执行wrangler上传命令...")
        log_status("注意: 这可能需要几分钟时间...")
        
        result = subprocess.run(cmd, capture_output=True, text=True, 
                              timeout=300, cwd=work_dir)
        
        if result.returncode == 0:
            log_status("✅ 数据上传成功！")
            print(result.stdout)
            return True
        else:
            log_status("❌ 数据上传失败:", "ERROR")
            log_status(f"错误代码: {result.returncode}")
            if result.stderr:
                log_status(f"错误信息:\n{result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        log_status("❌ 上传超时，请重试", "ERROR")
        return False
    except Exception as e:
        log_status(f"❌ 上传过程中出现错误: {e}", "ERROR")
        return False

def verify_upload():
    """验证上传结果"""
    log_status("🔍 验证上传结果...")
    
    try:
        # 检查关键表
        tables = ['cities', 'districts', 'communities', 'price_records', 'listing_snapshots']
        
        for table in tables:
            cmd = ['wrangler', 'd1', 'execute', 'yunnan-housing-new-db',
                   '--command', f'SELECT COUNT(*) as count FROM {table};']
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                count = result.stdout.strip()
                log_status(f"✅ {table}: {count} 记录")
            else:
                log_status(f"⚠️ 无法验证 {table}: {result.stderr}", "WARNING")
        
        log_status("✅ 验证完成！")
        return True
        
    except Exception as e:
        log_status(f"⚠️ 验证过程中出现错误: {e}", "WARNING")
        return False

def main():
    """主函数 - 执行完整的上传流程"""
    log_status("=" * 70)
    log_status("🎯 云南旅居房数据直连上传工具")
    log_status("📝 根据用户需求实现: 直接上传 + 授权登录 + 自动上传")
    log_status("=" * 70)
    
    work_dir = r"D:\AI work\workbuddy\2026-07-24-11-46-09\yunnan-housing-new"
    os.chdir(work_dir)
    
    # 检查wrangler可用性
    if not check_wrangler_availability():
        log_status("⚠️ wrangler不可用，但将继续尝试...")
    
    # 打开浏览器并等待授权
    if open_browser_and_wait():
        # 执行上传
        if execute_upload():
            # 验证结果
            verify_upload()
            
            log_status("=" * 70)
            log_status("🎉 直接上传流程全部完成！")
            log_status("=" * 70)
            log_status("✅ 用户授权获取成功")
            log_status("✅ 数据自动上传成功") 
            log_status("✅ 验证检查完成")
            log_status("\n📋 上传完成，可选操作:")
            log_status("1. 部署Worker: npx wrangler deploy")
            log_status("2. 部署Dashboard: 上传 dashboard/ 目录")
            log_status("3. 访问Dashboard: https://yunnan-housing-new-dashboard.pages.dev")
            
            return True
        else:
            log_status("❌ 上传失败", "ERROR")
            log_status("💡 建议: 手动使用浏览器访问https://dash.cloudflare.com/然后执行上传")
            return False
    else:
        log_status("❌ 用户取消或授权流程失败", "ERROR")
        log_status("💡 请运行脚本并确保完成Cloudflare登录")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        log_status("\n⚠️ 用户中断操作", "WARNING")
        sys.exit(1)
    except Exception as e:
        log_status(f"\n❌ 严重错误: {e}", "ERROR")
        sys.exit(1)
```

### Quick Start Commands

**For immediate operation (exactly what you want):**

```bash
# This is exactly your request - direct upload after authorization
cd yunnan-housing-new
python scripts/browser-auth.py
```

**For backup manual method (if script fails):**

```bash
# Manual method - open browser and login yourself
cd yunnan-housing-new
wrangler d1 execute yunnan-housing-new-db --file=local-crawler/import_data.sql
```

### User Experience Flow

**User's exact desired workflow:**

1. **You ask**: "给我上传数据, 你给我授权, 需要我登陆, 你弹出网页就行"

2. **I respond**: Runs `python scripts/browser-auth.py`

3. **Browser opens automatically** to Cloudflare login

4. **You login** (you provide the authorization)

5. **You press Enter** to confirm

6. **I automatically proceed** with the upload

7. **Upload completes** - you're done!

**This is the direct operation you preferred!**

### Key Enhancements for User Experience

1. **Minimal user intervention** - just press Enter after login
2. **Clear status messages** - shows exactly what's happening
3. **Error handling** - graceful fallbacks if things go wrong
4. **Verification included** - checks upload results automatically
5. **Consistent with your preferences** - matches your communication style

### Why This Works Better

- **No need for manual wrangler commands** - I handle all the technical details
- **Browser automation** - opens and waits for your authorization
- **Direct feedback** - you know exactly what's happening
- **Robust error handling** - provides helpful guidance if something goes wrong
- **Follows your preferred workflow** - matches your "直接上传 + 授权" pattern

This implementation directly addresses your signal about wanting direct upload with authorization, making the experience seamless and aligned with your preferences.

   ### Automation Script

   **For direct operation from the conversation's request**:

   ```python
   # browser-auth.py - Automatically handles authorization and upload
   import subprocess
   import time
   import os

   def main():
       print("🔐 Opening Cloudflare login page...")
    
       # Open browser for Cloudflare login
       subprocess.run(['start', 'https://dash.cloudflare.com/'], shell=True)
    
       print("⏳ Please log in to Cloudflare in the browser...")
       print("After logging in, press Enter to continue with upload.")
    
       # Wait for user to complete login
       input("✅ Login complete? (press Enter to continue): ")
    
       print("🚀 Starting data upload...")
    
       # Execute wrangler upload command
       os.chdir("yunnan-housing-new")
    
       result = subprocess.run([
           'wrangler', 'd1', 'execute', 
           'yunnan-housing-new-db', 
           '--file', 'local-crawler/import_data.sql'
       ], capture_output=True, text=True)
    
       if result.returncode == 0:
           print("✅ Data upload successful!")
           print(result.stdout)
        
           # Verify the upload
           verify_result = subprocess.run([
               'wrangler', 'd1', 'execute',
               'yunnan-housing-new-db',
               '--command', 'SELECT COUNT(*) FROM cities;'
           ], capture_output=True, text=True)
        
           cities_count = verify_result.stdout.strip()
           print(f"Cities: {cities_count}")
        
       else:
           print("❌ Data upload failed:")
           print(result.stderr)
           print("\n💡 Tip: Try using the Dashboard Method for reliable uploads.")

   if __name__ == "__main__":
       main()
   ```

   ### Quick Start Command

   **For immediate operation (as requested in the conversation)**:

   ```bash
   # This is what the user asked for - direct operation after authorization
   cd yunnan-housing-new
   python scripts/browser-auth.py
   ```

   ### Common Issues and Solutions

   #### Issue 1: wrangler CLI not available
   ```bash
   # Install wrangler
   npm install -g wrangler
   # or
   python -m pip install wrangler
   ```

   #### Issue 2: Browser automation doesn't work
   ```bash
   # Manual fallback
   start https://dash.cloudflare.com/
   # After login, run:
   cd yunnan-housing-new
   wrangler d1 execute yunnan-housing-new-db --file=local-crawler/import_data.sql
   ```

   #### Issue 3: Upload timeout or failure
   ```bash
   # Break into smaller chunks
   wrangler d1 execute yunnan-housing-new-db \
     --command="INSERT INTO cities SELECT * FROM temp_cities;"
   ```

   ### Verification Commands

   After any upload method, always verify:

   ```bash
   # Check all key tables
   cd yunnan-housing-new
   wrangler d1 execute yunnan-housing-new-db \
     --command="SELECT table_name, (SELECT COUNT(*) FROM table_name) as count FROM sqlite_master WHERE type='table' ORDER BY table_name;"
   ```

   Expected results:
   - **cities**: 16
   - **districts**: 10  
   - **communities**: 580
   - **price_records**: 17500
   - **listing_snapshots**: 17500
   ```

### Automation Script

**For direct operation from the conversation's request**:

```python
# browser-auth.py - Automatically handles authorization and upload
import subprocess
import time
import os

def main():
    print("🔐 Opening Cloudflare login page...")
    
    # Open browser for Cloudflare login
    subprocess.run(['start', 'https://dash.cloudflare.com/'], shell=True)
    
    print("⏳ Please log in to Cloudflare in the browser...")
    print("After logging in, press Enter to continue with upload.")
    
    # Wait for user to complete login
    input("✅ Login complete? (press Enter to continue): ")
    
    print("🚀 Starting data upload...")
    
    # Execute wrangler upload command
    os.chdir("yunnan-housing-new")
    
    result = subprocess.run([
        'wrangler', 'd1', 'execute', 
        'yunnan-housing-new-db', 
        '--file', 'local-crawler/import_data.sql'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Data upload successful!")
        print(result.stdout)
        
        # Verify the upload
        verify_result = subprocess.run([
            'wrangler', 'd1', 'execute',
            'yunnan-housing-new-db',
            '--command', 'SELECT COUNT(*) FROM cities;'
        ], capture_output=True, text=True)
        
        cities_count = verify_result.stdout.strip()
        print(f"Cities: {cities_count}")
        
    else:
        print("❌ Data upload failed:")
        print(result.stderr)
        print("\n💡 Tip: Try using the Dashboard Method for reliable uploads.")

if __name__ == "__main__":
    main()
```

### Quick Start Command

**For immediate operation (as requested in the conversation)**:

```bash
# This is what the user asked for - direct operation after authorization
cd yunnan-housing-new
python scripts/browser-auth.py
```

### Common Issues and Solutions

#### Issue 1: wrangler CLI not available
```bash
# Install wrangler
npm install -g wrangler
# or
python -m pip install wrangler
```

#### Issue 2: Browser automation doesn't work
```bash
# Manual fallback
start https://dash.cloudflare.com/
# After login, run:
cd yunnan-housing-new
wrangler d1 execute yunnan-housing-new-db --file=local-crawler/import_data.sql
```

#### Issue 3: Upload timeout or failure
```bash
# Break into smaller chunks
wrangler d1 execute yunnan-housing-new-db \
  --command="INSERT INTO cities SELECT * FROM temp_cities;"
```

### Verification Commands

After any upload method, always verify:

```bash
# Check all key tables
cd yunnan-housing-new
wrangler d1 execute yunnan-housing-new-db \
  --command="SELECT table_name, (SELECT COUNT(*) FROM table_name) as count FROM sqlite_master WHERE type='table' ORDER BY table_name;"
```

Expected results:
- **cities**: 16
- **districts**: 10  
- **communities**: 580
- **price_records**: 17500
- **listing_snapshots**: 17500

## Common Pitfalls

### Windows Path Issues

**Problem**: Relative paths cause errors

**Solution**: Use absolute paths
```bash
set SQL_FILE="D:/AI work/workbuddy/2026-07-19-09-49-20/yunnan-housing/local-crawler/import_data.sql"
```

### Encoding Issues

**Problem**: Chinese characters garbled

**Solution**: Use UTF-8
```bash
chcp 65001 >nul
python -c "open('file.txt', 'w', encoding='utf-8').write('内容')"
```

### Permission Issues

**Problem**: Cannot write files

**Solution**: Fix permissions
```bash
chmod -R 755 ~/.hermes/
```

### Wrangler CLI Installation Issues

**Problem**: npm/wrangler CLI fails to install or run

**Solution**: Use Node.js binary directly
```bash
# Download Node.js
curl -o nodejs.zip https://nodejs.org/dist/v20.18.1/node-v20.18.1-win-x64.zip

# Extract and use directly
unzip nodejs.zip
cd nodejs/node-v20.18.1-win-x64
./node --version
./npm install -g wrangler
```

### Browser Authorization Pattern

**Problem**: Need user login authorization for Cloudflare

**Solution**: Automated browser opening with pause for manual login
```python
import subprocess
import os

# Open browser for login
subprocess.run(['start', 'https://dash.cloudflare.com'], shell=True)

print("Browser opened. Please complete login, then press Enter...")
input()  # Wait for user confirmation
```

### File Size Considerations

**Problem**: Large SQL files (14MB+) may timeout during upload

**Solution**: 
- Use Dashboard interface for large files
- Break into smaller chunks if needed
- Monitor upload progress in Cloudflare dashboard

## Session-Specific Learnings

### Browser Automation Pattern

**Key Discovery**: When user requests "直接上传 我给你授权 需要我登陆 你弹出网页就行", use:
1. `subprocess.run(['start', 'url'], shell=True)` to open browser
2. Pause for manual user login completion
3. Continue with automated upload after user confirmation

### Data Migration Verification

**Verification Pattern**: After upload, always check:
```sql
SELECT COUNT(*) FROM cities;        -- Should return 16
SELECT COUNT(*) FROM price_records; -- Should return ~17500
SELECT COUNT(*) FROM communities;   -- Should return ~580
```

### Project Structure Preservation

**Critical Pattern**: Maintain exact directory structure:
```
project-name/
├── wrangler.toml
├── package.json
├── schema.sql
├── README.md
├── src/
│   ├── index.js
│   ├── db.js
│   └── api.js
├── dashboard/
│   └── index.html
└── local-crawler/
    ├── crawler.py
    ├── import_data.sql
    └── upload_to_d1.bat
```

## References

For detailed guidance, see:
- `references/project-replication-workflow.md` - Complete step-by-step guide
- `references/cloudflare-d1-upload.md` - D1 specific procedures
- `references/troubleshooting.md` - Common issues and solutions
- `references/yunnan-housing-replication-case-study.md` - Real-world case study with 14MB data migration
- `references/browser-auth-pattern.md` - Browser authorization pattern for user login flows

## Scripts

- `scripts/browser-auth.py` - Browser automation for user login authorization
- `scripts/verify-upload.py` - Automated data verification after upload

---

*Version: 1.0.0*
*Created: 2026-07-24*
