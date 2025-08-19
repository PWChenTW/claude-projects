#!/usr/bin/env python3
"""
記憶備份腳本 - Memory Backup Script
用於備份和恢復專案記憶系統
"""

import os
import json
import shutil
import tarfile
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict

class MemoryBackup:
    """記憶備份管理器"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.memory_base = self.project_root / ".kiro" / "memory"
        self.backup_dir = self.project_root / ".kiro" / "backups"
        
        # 確保備份目錄存在
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def create_backup(self, backup_name: Optional[str] = None) -> Path:
        """創建記憶系統備份"""
        if not backup_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"memory_backup_{timestamp}"
        
        backup_file = self.backup_dir / f"{backup_name}.tar.gz"
        
        print(f"📦 創建備份: {backup_file.name}")
        
        # 創建備份元數據
        metadata = {
            "created": datetime.now().isoformat(),
            "backup_name": backup_name,
            "source": str(self.memory_base.relative_to(self.project_root)),
            "files_count": 0,
            "directories": []
        }
        
        # 統計文件
        for root, dirs, files in os.walk(self.memory_base):
            root_path = Path(root)
            rel_path = root_path.relative_to(self.memory_base)
            metadata["directories"].append(str(rel_path))
            metadata["files_count"] += len(files)
        
        # 創建臨時元數據文件
        metadata_file = self.backup_dir / f"{backup_name}_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # 創建壓縮備份
        with tarfile.open(backup_file, "w:gz") as tar:
            # 添加記憶目錄
            tar.add(
                self.memory_base,
                arcname="memory",
                recursive=True
            )
            # 添加元數據
            tar.add(
                metadata_file,
                arcname="metadata.json"
            )
        
        # 清理臨時元數據文件
        metadata_file.unlink()
        
        print(f"✅ 備份完成:")
        print(f"   - 文件數: {metadata['files_count']}")
        print(f"   - 目錄數: {len(metadata['directories'])}")
        print(f"   - 大小: {backup_file.stat().st_size / 1024:.2f} KB")
        
        return backup_file
    
    def list_backups(self) -> List[Dict]:
        """列出所有備份"""
        backups = []
        
        for backup_file in self.backup_dir.glob("memory_backup_*.tar.gz"):
            # 提取元數據
            try:
                with tarfile.open(backup_file, "r:gz") as tar:
                    # 嘗試讀取元數據
                    try:
                        metadata_info = tar.getmember("metadata.json")
                        f = tar.extractfile(metadata_info)
                        if f:
                            metadata = json.load(f)
                        else:
                            metadata = {}
                    except KeyError:
                        metadata = {}
                
                backups.append({
                    "file": backup_file.name,
                    "size": f"{backup_file.stat().st_size / 1024:.2f} KB",
                    "created": metadata.get("created", "unknown"),
                    "files_count": metadata.get("files_count", "unknown")
                })
            except Exception as e:
                print(f"⚠️  無法讀取備份 {backup_file.name}: {e}")
        
        return sorted(backups, key=lambda x: x["file"], reverse=True)
    
    def restore_backup(self, backup_name: str, target_dir: Optional[Path] = None):
        """恢復備份"""
        # 查找備份文件
        if not backup_name.endswith(".tar.gz"):
            backup_name += ".tar.gz"
        
        backup_file = self.backup_dir / backup_name
        
        if not backup_file.exists():
            print(f"❌ 備份文件不存在: {backup_file}")
            return False
        
        if target_dir is None:
            target_dir = self.memory_base
        
        print(f"📂 恢復備份: {backup_file.name}")
        print(f"📍 目標位置: {target_dir}")
        
        # 創建恢復前備份
        if target_dir.exists():
            print("⚠️  目標目錄已存在，創建恢復前備份...")
            pre_restore_backup = f"pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.create_backup(pre_restore_backup)
        
        # 清空目標目錄
        if target_dir.exists():
            shutil.rmtree(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # 解壓備份
        with tarfile.open(backup_file, "r:gz") as tar:
            # 提取記憶目錄內容
            for member in tar.getmembers():
                if member.name.startswith("memory/"):
                    # 調整路徑
                    member.name = member.name[7:]  # 移除 "memory/" 前綴
                    if member.name:  # 確保不是空路徑
                        tar.extract(member, target_dir)
        
        print(f"✅ 備份恢復完成！")
        return True
    
    def auto_backup(self, max_backups: int = 7):
        """自動備份（保留最近N個備份）"""
        print(f"🔄 執行自動備份 (保留最近 {max_backups} 個)")
        
        # 創建新備份
        new_backup = self.create_backup()
        
        # 清理舊備份
        backups = list(self.backup_dir.glob("memory_backup_*.tar.gz"))
        backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        if len(backups) > max_backups:
            for old_backup in backups[max_backups:]:
                print(f"🗑️  刪除舊備份: {old_backup.name}")
                old_backup.unlink()
        
        print(f"✅ 自動備份完成，當前保留 {min(len(backups), max_backups)} 個備份")
    
    def export_memory(self, export_path: Path):
        """導出記憶系統為可讀格式"""
        export_path.mkdir(parents=True, exist_ok=True)
        
        print(f"📤 導出記憶系統到: {export_path}")
        
        # 複製所有記憶文件
        for memory_type in ["global", "project", "session"]:
            source = self.memory_base / memory_type
            if source.exists():
                target = export_path / memory_type
                shutil.copytree(source, target, dirs_exist_ok=True)
                print(f"   ✓ 導出 {memory_type} 記憶")
        
        # 生成索引文件
        index_content = ["# 記憶系統導出索引\n"]
        index_content.append(f"導出時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        for root, dirs, files in os.walk(export_path):
            level = root.replace(str(export_path), '').count(os.sep)
            indent = ' ' * 2 * level
            root_path = Path(root)
            index_content.append(f"{indent}- {root_path.name}/")
            
            sub_indent = ' ' * 2 * (level + 1)
            for file in files:
                index_content.append(f"{sub_indent}- {file}")
        
        index_file = export_path / "INDEX.md"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(index_content))
        
        print(f"✅ 記憶系統導出完成！")
        print(f"📋 索引文件: {index_file}")


def main():
    """主函數"""
    import argparse
    
    parser = argparse.ArgumentParser(description="記憶系統備份工具")
    parser.add_argument(
        "action",
        choices=["backup", "restore", "list", "auto", "export"],
        help="操作類型"
    )
    parser.add_argument(
        "--name",
        help="備份名稱（用於備份或恢復）"
    )
    parser.add_argument(
        "--target",
        help="恢復目標目錄或導出目錄"
    )
    parser.add_argument(
        "--max-backups",
        type=int,
        default=7,
        help="自動備份保留數量（預設: 7）"
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="專案根目錄（預設: 當前目錄）"
    )
    
    args = parser.parse_args()
    
    backup_manager = MemoryBackup(args.project_root)
    
    if args.action == "backup":
        backup_manager.create_backup(args.name)
    
    elif args.action == "restore":
        if not args.name:
            print("❌ 請指定要恢復的備份名稱 (--name)")
        else:
            target = Path(args.target) if args.target else None
            backup_manager.restore_backup(args.name, target)
    
    elif args.action == "list":
        backups = backup_manager.list_backups()
        if backups:
            print("\n📚 可用備份:")
            print("-" * 60)
            for backup in backups:
                print(f"📦 {backup['file']}")
                print(f"   大小: {backup['size']}")
                print(f"   創建: {backup['created']}")
                print(f"   文件: {backup['files_count']}")
                print()
        else:
            print("ℹ️  沒有發現備份")
    
    elif args.action == "auto":
        backup_manager.auto_backup(args.max_backups)
    
    elif args.action == "export":
        if not args.target:
            print("❌ 請指定導出目錄 (--target)")
        else:
            backup_manager.export_memory(Path(args.target))
    
    print("\n✨ 操作完成！")


if __name__ == "__main__":
    main()