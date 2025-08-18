#!/usr/bin/env python3
"""
記憶自動更新腳本 - Memory Auto Update Script
整合所有記憶管理功能，提供自動化更新機制
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List

class MemoryAutoUpdater:
    """記憶自動更新管理器"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.scripts_dir = self.project_root / ".claude" / "scripts"
        self.memory_base = self.project_root / ".kiro" / "memory"
        self.hooks_config = self.project_root / ".claude" / "settings.json"
        
        # Python 執行檔路徑
        self.python_exe = sys.executable
    
    def run_script(self, script_name: str, args: List[str] = None) -> bool:
        """執行記憶管理腳本"""
        script_path = self.scripts_dir / script_name
        
        if not script_path.exists():
            print(f"⚠️  腳本不存在: {script_path}")
            return False
        
        cmd = [self.python_exe, str(script_path)]
        if args:
            cmd.extend(args)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                print(f"✅ {script_name} 執行成功")
                if result.stdout:
                    print(result.stdout)
                return True
            else:
                print(f"❌ {script_name} 執行失敗")
                if result.stderr:
                    print(result.stderr)
                return False
        
        except Exception as e:
            print(f"❌ 執行腳本時發生錯誤: {e}")
            return False
    
    def on_task_complete(self, task_name: str = None):
        """任務完成時的自動更新"""
        print("\n🎯 檢測到任務完成，執行記憶更新...")
        
        # 1. 同步進度
        self.run_script("memory_sync.py", ["--type", "progress"])
        
        # 2. 同步研究（如果有）
        self.run_script("memory_sync.py", ["--type", "research"])
        
        # 3. 創建快照備份（輕量）
        if task_name:
            backup_name = f"task_{task_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.run_script("memory_backup.py", ["backup", "--name", backup_name])
        
        print("✅ 任務完成更新完成\n")
    
    def on_spec_init(self, feature_name: str):
        """規格初始化時的自動更新"""
        print(f"\n📋 檢測到規格初始化: {feature_name}")
        
        # 1. 同步規格狀態
        self.run_script("memory_sync.py", ["--type", "specs"])
        
        # 2. 記錄到會話記憶
        session_log = self.memory_base / "session" / "active_specs.json"
        session_log.parent.mkdir(parents=True, exist_ok=True)
        
        active_specs = []
        if session_log.exists():
            with open(session_log, 'r', encoding='utf-8') as f:
                active_specs = json.load(f)
        
        active_specs.append({
            "feature": feature_name,
            "started": datetime.now().isoformat(),
            "status": "initialized"
        })
        
        with open(session_log, 'w', encoding='utf-8') as f:
            json.dump(active_specs, f, indent=2, ensure_ascii=False)
        
        print("✅ 規格初始化記錄完成\n")
    
    def on_git_commit(self):
        """Git 提交時的自動更新"""
        print("\n📦 檢測到 Git 提交，執行記憶同步...")
        
        # 1. 全面同步
        self.run_script("memory_sync.py", ["--type", "all"])
        
        # 2. 自動備份（保留最近 7 個）
        self.run_script("memory_backup.py", ["auto", "--max-backups", "7"])
        
        print("✅ Git 提交同步完成\n")
    
    def on_daily_cleanup(self):
        """每日自動清理"""
        print("\n🧹 執行每日清理任務...")
        
        # 1. 清理舊研究（超過 30 天）
        self.run_script("memory_cleanup.py", ["research", "--days", "30"])
        
        # 2. 清理空目錄
        self.run_script("memory_cleanup.py", ["empty"])
        
        # 3. 分析使用情況
        self.run_script("memory_cleanup.py", ["analyze"])
        
        print("✅ 每日清理完成\n")
    
    def on_session_end(self):
        """會話結束時的自動更新"""
        print("\n👋 檢測到會話結束，執行最終同步...")
        
        # 1. 同步所有記憶
        self.run_script("memory_sync.py", ["--type", "all"])
        
        # 2. 清理會話記憶（歸檔）
        self.run_script("memory_cleanup.py", ["session"])
        
        # 3. 生成記憶報告
        self.run_script("memory_query.py", ["map"])
        
        print("✅ 會話結束處理完成\n")
    
    def setup_hooks(self):
        """設置自動更新 hooks"""
        print("🔧 配置自動更新 hooks...\n")
        
        # 1. 更新 Claude settings.json
        settings_updated = self.update_claude_settings()
        
        # 2. 創建 Git hooks
        git_hooks_created = self.create_git_hooks()
        
        # 3. 創建定時任務腳本
        cron_script_created = self.create_cron_script()
        
        if settings_updated and git_hooks_created and cron_script_created:
            print("\n✅ 自動更新機制配置完成！")
            return True
        else:
            print("\n⚠️  部分配置可能需要手動完成")
            return False
    
    def update_claude_settings(self) -> bool:
        """更新 Claude 的 settings.json"""
        if not self.hooks_config.exists():
            # 創建新的 settings.json
            settings = {
                "hooks": {
                    "post-task": "python .claude/scripts/memory_auto_update.py task",
                    "post-spec-init": "python .claude/scripts/memory_auto_update.py spec-init",
                    "pre-session-end": "python .claude/scripts/memory_auto_update.py session-end"
                },
                "memory": {
                    "auto_sync": True,
                    "auto_backup": True,
                    "backup_retention": 7,
                    "research_retention_days": 30
                }
            }
            
            with open(self.hooks_config, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            
            print("✅ 創建了新的 settings.json")
            return True
        else:
            # 更新現有的 settings.json
            try:
                with open(self.hooks_config, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                # 添加或更新 hooks
                if "hooks" not in settings:
                    settings["hooks"] = {}
                
                settings["hooks"].update({
                    "post-task": "python .claude/scripts/memory_auto_update.py task",
                    "post-spec-init": "python .claude/scripts/memory_auto_update.py spec-init",
                    "pre-session-end": "python .claude/scripts/memory_auto_update.py session-end"
                })
                
                # 添加記憶配置
                if "memory" not in settings:
                    settings["memory"] = {}
                
                settings["memory"].update({
                    "auto_sync": True,
                    "auto_backup": True,
                    "backup_retention": 7,
                    "research_retention_days": 30
                })
                
                with open(self.hooks_config, 'w', encoding='utf-8') as f:
                    json.dump(settings, f, indent=2, ensure_ascii=False)
                
                print("✅ 更新了 settings.json")
                return True
            
            except Exception as e:
                print(f"❌ 更新 settings.json 失敗: {e}")
                return False
    
    def create_git_hooks(self) -> bool:
        """創建 Git hooks"""
        git_hooks_dir = self.project_root / ".git" / "hooks"
        
        if not git_hooks_dir.exists():
            print("⚠️  Git hooks 目錄不存在（可能不是 Git 倉庫）")
            return False
        
        # 創建 post-commit hook
        post_commit_hook = git_hooks_dir / "post-commit"
        hook_content = """#!/bin/sh
# Auto-update memory system after commit
python .claude/scripts/memory_auto_update.py git-commit
"""
        
        try:
            with open(post_commit_hook, 'w') as f:
                f.write(hook_content)
            
            # 設置執行權限
            os.chmod(post_commit_hook, 0o755)
            
            print("✅ 創建了 Git post-commit hook")
            return True
        
        except Exception as e:
            print(f"❌ 創建 Git hook 失敗: {e}")
            return False
    
    def create_cron_script(self) -> bool:
        """創建定時任務腳本"""
        cron_script = self.scripts_dir / "daily_maintenance.sh"
        
        script_content = f"""#!/bin/bash
# Daily memory maintenance script
# Add to crontab: 0 2 * * * /path/to/daily_maintenance.sh

cd "{self.project_root}"
{self.python_exe} .claude/scripts/memory_auto_update.py daily-cleanup
"""
        
        try:
            with open(cron_script, 'w') as f:
                f.write(script_content)
            
            # 設置執行權限
            os.chmod(cron_script, 0o755)
            
            print("✅ 創建了每日維護腳本")
            print(f"   提示：將以下行添加到 crontab 以啟用每日清理：")
            print(f"   0 2 * * * {cron_script}")
            return True
        
        except Exception as e:
            print(f"❌ 創建定時任務腳本失敗: {e}")
            return False
    
    def status(self):
        """檢查自動更新狀態"""
        print("📊 記憶自動更新系統狀態\n")
        print("="*50)
        
        # 檢查 settings.json
        if self.hooks_config.exists():
            with open(self.hooks_config, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            if "hooks" in settings:
                print("✅ Claude hooks 已配置")
                for hook, cmd in settings["hooks"].items():
                    print(f"   - {hook}: {cmd[:50]}...")
            else:
                print("❌ Claude hooks 未配置")
            
            if "memory" in settings:
                print("\n✅ 記憶配置:")
                for key, value in settings["memory"].items():
                    print(f"   - {key}: {value}")
        else:
            print("❌ settings.json 不存在")
        
        # 檢查 Git hooks
        git_post_commit = self.project_root / ".git" / "hooks" / "post-commit"
        if git_post_commit.exists():
            print("\n✅ Git hooks 已配置")
        else:
            print("\n❌ Git hooks 未配置")
        
        # 檢查腳本
        scripts = ["memory_sync.py", "memory_backup.py", "memory_query.py", "memory_cleanup.py"]
        all_exist = all((self.scripts_dir / script).exists() for script in scripts)
        
        if all_exist:
            print("\n✅ 所有記憶管理腳本就緒")
        else:
            print("\n⚠️  部分記憶管理腳本缺失")
            for script in scripts:
                exists = (self.scripts_dir / script).exists()
                status = "✅" if exists else "❌"
                print(f"   {status} {script}")
        
        print("\n" + "="*50)


def main():
    """主函數"""
    import argparse
    
    parser = argparse.ArgumentParser(description="記憶自動更新系統")
    parser.add_argument(
        "action",
        choices=["setup", "status", "task", "spec-init", "git-commit", 
                 "daily-cleanup", "session-end", "test"],
        help="操作類型"
    )
    parser.add_argument(
        "--feature",
        help="功能名稱（用於 spec-init）"
    )
    parser.add_argument(
        "--task",
        help="任務名稱（用於 task）"
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="專案根目錄（預設: 當前目錄）"
    )
    
    args = parser.parse_args()
    
    updater = MemoryAutoUpdater(args.project_root)
    
    if args.action == "setup":
        updater.setup_hooks()
    
    elif args.action == "status":
        updater.status()
    
    elif args.action == "task":
        updater.on_task_complete(args.task)
    
    elif args.action == "spec-init":
        feature = args.feature or "unknown"
        updater.on_spec_init(feature)
    
    elif args.action == "git-commit":
        updater.on_git_commit()
    
    elif args.action == "daily-cleanup":
        updater.on_daily_cleanup()
    
    elif args.action == "session-end":
        updater.on_session_end()
    
    elif args.action == "test":
        print("🧪 測試自動更新系統...\n")
        print("1. 測試任務完成更新:")
        updater.on_task_complete("test-task")
        
        print("\n2. 測試規格初始化:")
        updater.on_spec_init("test-feature")
        
        print("\n✅ 測試完成！")
    
    print("\n✨ 操作完成！")


if __name__ == "__main__":
    main()