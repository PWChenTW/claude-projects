#!/usr/bin/env python3
"""
記憶清理腳本 - Memory Cleanup Script
用於清理和維護專案記憶系統
"""

import os
import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple

class MemoryCleanup:
    """記憶清理管理器"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.memory_base = self.project_root / ".kiro" / "memory"
        self.session_memory = self.memory_base / "session"
        self.archive_dir = self.project_root / ".kiro" / "archive"
        self.research_dir = self.project_root / ".kiro" / "research"
        
        # 確保歸檔目錄存在
        self.archive_dir.mkdir(parents=True, exist_ok=True)
    
    def clean_session_memory(self, archive: bool = True) -> Dict:
        """清理會話記憶"""
        result = {
            "cleaned_files": 0,
            "archived_files": 0,
            "freed_space": 0
        }
        
        if not self.session_memory.exists():
            print("ℹ️  會話記憶目錄不存在")
            return result
        
        print("🧹 清理會話記憶...")
        
        # 計算原始大小
        original_size = sum(
            f.stat().st_size for f in self.session_memory.rglob("*") if f.is_file()
        )
        
        if archive:
            # 創建歸檔
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_path = self.archive_dir / f"session_{timestamp}"
            archive_path.mkdir(parents=True, exist_ok=True)
            
            # 移動文件到歸檔
            for file_path in self.session_memory.rglob("*"):
                if file_path.is_file():
                    rel_path = file_path.relative_to(self.session_memory)
                    target_path = archive_path / rel_path
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(file_path), str(target_path))
                    result["archived_files"] += 1
            
            print(f"📦 已歸檔 {result['archived_files']} 個文件到: {archive_path.name}")
        else:
            # 直接刪除
            for file_path in self.session_memory.rglob("*"):
                if file_path.is_file():
                    file_path.unlink()
                    result["cleaned_files"] += 1
            
            print(f"🗑️  已刪除 {result['cleaned_files']} 個文件")
        
        # 清理空目錄
        for dir_path in list(self.session_memory.rglob("*")):
            if dir_path.is_dir() and not any(dir_path.iterdir()):
                dir_path.rmdir()
        
        result["freed_space"] = original_size
        print(f"💾 釋放空間: {original_size / 1024:.2f} KB")
        
        return result
    
    def clean_old_research(self, days: int = 30, archive: bool = True) -> Dict:
        """清理舊的研究文檔"""
        result = {
            "cleaned_dirs": 0,
            "cleaned_files": 0,
            "freed_space": 0
        }
        
        if not self.research_dir.exists():
            print("ℹ️  研究目錄不存在")
            return result
        
        print(f"🧹 清理超過 {days} 天的研究文檔...")
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for date_dir in self.research_dir.iterdir():
            if date_dir.is_dir():
                try:
                    # 解析目錄名為日期
                    dir_date = datetime.strptime(date_dir.name, "%Y-%m-%d")
                    
                    if dir_date < cutoff_date:
                        # 計算目錄大小
                        dir_size = sum(
                            f.stat().st_size for f in date_dir.rglob("*") if f.is_file()
                        )
                        file_count = sum(1 for f in date_dir.rglob("*") if f.is_file())
                        
                        if archive:
                            # 歸檔到 archive/research/
                            archive_path = self.archive_dir / "research" / date_dir.name
                            archive_path.parent.mkdir(parents=True, exist_ok=True)
                            shutil.move(str(date_dir), str(archive_path))
                            print(f"📦 歸檔: {date_dir.name} ({file_count} 個文件)")
                        else:
                            # 直接刪除
                            shutil.rmtree(date_dir)
                            print(f"🗑️  刪除: {date_dir.name} ({file_count} 個文件)")
                        
                        result["cleaned_dirs"] += 1
                        result["cleaned_files"] += file_count
                        result["freed_space"] += dir_size
                
                except ValueError:
                    # 不是日期格式的目錄，跳過
                    continue
        
        if result["cleaned_dirs"] > 0:
            print(f"✅ 清理了 {result['cleaned_dirs']} 個目錄，"
                  f"{result['cleaned_files']} 個文件")
            print(f"💾 釋放空間: {result['freed_space'] / (1024*1024):.2f} MB")
        else:
            print("ℹ️  沒有需要清理的舊研究文檔")
        
        return result
    
    def clean_duplicate_decisions(self) -> Dict:
        """清理重複的決策記錄"""
        result = {
            "duplicates_found": 0,
            "duplicates_removed": 0
        }
        
        global_decisions = list(self.memory_base.glob("global/decisions_*.md"))
        
        if len(global_decisions) <= 1:
            print("ℹ️  沒有重複的決策記錄")
            return result
        
        print(f"🔍 發現 {len(global_decisions)} 個決策記錄文件")
        
        # 按修改時間排序，保留最新的
        global_decisions.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # 保留最新的，刪除其餘的
        for old_decision in global_decisions[1:]:
            print(f"🗑️  刪除舊決策記錄: {old_decision.name}")
            old_decision.unlink()
            result["duplicates_removed"] += 1
        
        result["duplicates_found"] = len(global_decisions) - 1
        
        return result
    
    def clean_empty_directories(self) -> int:
        """清理空目錄"""
        empty_dirs_count = 0
        
        # 遞迴清理空目錄
        for root, dirs, files in os.walk(self.memory_base, topdown=False):
            root_path = Path(root)
            if not files and not dirs:
                if root_path != self.memory_base:  # 不刪除根目錄
                    print(f"🗑️  刪除空目錄: {root_path.relative_to(self.project_root)}")
                    root_path.rmdir()
                    empty_dirs_count += 1
        
        return empty_dirs_count
    
    def analyze_memory_usage(self) -> Dict:
        """分析記憶使用情況"""
        usage = {
            "total_size": 0,
            "by_type": {},
            "large_files": [],
            "old_files": []
        }
        
        # 統計各類型記憶使用
        for memory_type in ["global", "project", "session"]:
            memory_path = self.memory_base / memory_type
            if memory_path.exists():
                type_size = 0
                file_count = 0
                
                for file_path in memory_path.rglob("*"):
                    if file_path.is_file():
                        file_size = file_path.stat().st_size
                        type_size += file_size
                        file_count += 1
                        
                        # 記錄大文件（> 100KB）
                        if file_size > 100 * 1024:
                            usage["large_files"].append({
                                "path": str(file_path.relative_to(self.project_root)),
                                "size": f"{file_size / 1024:.2f} KB"
                            })
                        
                        # 記錄舊文件（> 30天）
                        file_age = datetime.now() - datetime.fromtimestamp(
                            file_path.stat().st_mtime
                        )
                        if file_age.days > 30:
                            usage["old_files"].append({
                                "path": str(file_path.relative_to(self.project_root)),
                                "age_days": file_age.days
                            })
                
                usage["by_type"][memory_type] = {
                    "size": type_size,
                    "files": file_count
                }
                usage["total_size"] += type_size
        
        return usage
    
    def auto_cleanup(self, session_days: int = 0, research_days: int = 30) -> Dict:
        """自動清理（根據策略）"""
        print("🤖 開始自動清理...\n")
        
        total_result = {
            "session_cleaned": False,
            "research_cleaned": 0,
            "duplicates_removed": 0,
            "empty_dirs_removed": 0,
            "total_freed_space": 0
        }
        
        # 1. 分析使用情況
        print("📊 分析記憶使用情況...")
        usage = self.analyze_memory_usage()
        print(f"   總大小: {usage['total_size'] / (1024*1024):.2f} MB")
        for mem_type, info in usage["by_type"].items():
            print(f"   {mem_type}: {info['size'] / 1024:.2f} KB ({info['files']} 個文件)")
        
        # 2. 清理會話記憶（如果指定）
        if session_days == 0:
            print(f"\n1️⃣  清理會話記憶...")
            session_result = self.clean_session_memory(archive=True)
            total_result["session_cleaned"] = True
            total_result["total_freed_space"] += session_result["freed_space"]
        
        # 3. 清理舊研究文檔
        print(f"\n2️⃣  清理超過 {research_days} 天的研究文檔...")
        research_result = self.clean_old_research(research_days, archive=True)
        total_result["research_cleaned"] = research_result["cleaned_dirs"]
        total_result["total_freed_space"] += research_result["freed_space"]
        
        # 4. 清理重複決策
        print(f"\n3️⃣  清理重複決策記錄...")
        duplicate_result = self.clean_duplicate_decisions()
        total_result["duplicates_removed"] = duplicate_result["duplicates_removed"]
        
        # 5. 清理空目錄
        print(f"\n4️⃣  清理空目錄...")
        empty_dirs = self.clean_empty_directories()
        total_result["empty_dirs_removed"] = empty_dirs
        
        # 顯示清理摘要
        print("\n" + "="*50)
        print("📋 清理摘要:")
        print(f"   會話記憶: {'已清理' if total_result['session_cleaned'] else '未清理'}")
        print(f"   研究文檔: 清理了 {total_result['research_cleaned']} 個目錄")
        print(f"   重複決策: 移除了 {total_result['duplicates_removed']} 個")
        print(f"   空目錄: 移除了 {total_result['empty_dirs_removed']} 個")
        print(f"   釋放空間: {total_result['total_freed_space'] / (1024*1024):.2f} MB")
        
        return total_result


def main():
    """主函數"""
    import argparse
    
    parser = argparse.ArgumentParser(description="記憶系統清理工具")
    parser.add_argument(
        "action",
        choices=["session", "research", "duplicates", "empty", "analyze", "auto"],
        help="清理類型"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="清理N天前的內容（用於research，預設: 30）"
    )
    parser.add_argument(
        "--no-archive",
        action="store_true",
        help="直接刪除而不歸檔"
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="專案根目錄（預設: 當前目錄）"
    )
    
    args = parser.parse_args()
    
    cleaner = MemoryCleanup(args.project_root)
    archive = not args.no_archive
    
    if args.action == "session":
        result = cleaner.clean_session_memory(archive=archive)
        print(f"\n✅ 會話記憶清理完成")
    
    elif args.action == "research":
        result = cleaner.clean_old_research(days=args.days, archive=archive)
        print(f"\n✅ 研究文檔清理完成")
    
    elif args.action == "duplicates":
        result = cleaner.clean_duplicate_decisions()
        print(f"\n✅ 重複決策清理完成")
    
    elif args.action == "empty":
        count = cleaner.clean_empty_directories()
        print(f"\n✅ 清理了 {count} 個空目錄")
    
    elif args.action == "analyze":
        usage = cleaner.analyze_memory_usage()
        
        print("\n📊 記憶系統使用分析")
        print("="*50)
        print(f"總大小: {usage['total_size'] / (1024*1024):.2f} MB\n")
        
        print("按類型統計:")
        for mem_type, info in usage["by_type"].items():
            print(f"  {mem_type:10} {info['size']/1024:8.2f} KB  ({info['files']} 個文件)")
        
        if usage["large_files"]:
            print("\n大文件 (>100KB):")
            for file in usage["large_files"][:5]:
                print(f"  {file['size']:>10} - {file['path']}")
        
        if usage["old_files"]:
            print("\n舊文件 (>30天):")
            for file in usage["old_files"][:5]:
                print(f"  {file['age_days']:>3}天 - {file['path']}")
    
    elif args.action == "auto":
        result = cleaner.auto_cleanup(
            session_days=0,  # 清理所有會話記憶
            research_days=args.days
        )
        print(f"\n✅ 自動清理完成")
    
    print("\n✨ 操作完成！")


if __name__ == "__main__":
    main()