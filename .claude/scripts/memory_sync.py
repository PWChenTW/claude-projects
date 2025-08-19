#!/usr/bin/env python3
"""
記憶同步腳本 - Memory Sync Script
用於同步和更新專案記憶系統
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class MemorySync:
    """記憶同步管理器"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.memory_base = self.project_root / ".kiro" / "memory"
        self.global_memory = self.memory_base / "global"
        self.project_memory = self.memory_base / "project"
        self.session_memory = self.memory_base / "session"
        
        # 確保目錄結構存在
        self._ensure_directory_structure()
    
    def _ensure_directory_structure(self):
        """確保記憶目錄結構存在"""
        for path in [self.global_memory, self.project_memory, self.session_memory]:
            path.mkdir(parents=True, exist_ok=True)
    
    def sync_from_research(self):
        """從研究文檔同步重要發現到記憶系統"""
        research_dir = self.project_root / ".kiro" / "research"
        if not research_dir.exists():
            print(f"⚠️  研究目錄不存在: {research_dir}")
            return
        
        # 獲取今天的研究文檔
        today = datetime.now().strftime("%Y-%m-%d")
        today_research = research_dir / today
        
        if today_research.exists():
            findings = []
            for md_file in today_research.glob("*.md"):
                print(f"📖 處理研究文檔: {md_file.name}")
                findings.append({
                    "file": md_file.name,
                    "date": today,
                    "path": str(md_file.relative_to(self.project_root))
                })
            
            # 更新 session memory
            session_findings = self.session_memory / "research_findings.json"
            existing_findings = []
            if session_findings.exists():
                with open(session_findings, 'r', encoding='utf-8') as f:
                    existing_findings = json.load(f)
            
            existing_findings.extend(findings)
            
            with open(session_findings, 'w', encoding='utf-8') as f:
                json.dump(existing_findings, f, indent=2, ensure_ascii=False)
            
            print(f"✅ 同步了 {len(findings)} 個研究文檔到會話記憶")
        else:
            print(f"ℹ️  今天沒有研究文檔")
    
    def sync_progress(self):
        """同步進度更新到記憶系統"""
        progress_file = self.project_memory / "enhancement-progress.md"
        
        if not progress_file.exists():
            print(f"⚠️  進度文件不存在: {progress_file}")
            return
        
        # 讀取進度文件並提取關鍵信息
        with open(progress_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 統計完成狀態
        completed_count = content.count("✅")
        in_progress_count = content.count("🚧")
        pending_count = content.count("⏳")
        
        summary = {
            "last_updated": datetime.now().isoformat(),
            "statistics": {
                "completed": completed_count,
                "in_progress": in_progress_count,
                "pending": pending_count
            },
            "progress_file": str(progress_file.relative_to(self.project_root))
        }
        
        # 保存摘要
        summary_file = self.project_memory / "progress_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 進度同步完成:")
        print(f"   - 已完成: {completed_count}")
        print(f"   - 進行中: {in_progress_count}")
        print(f"   - 待處理: {pending_count}")
    
    def sync_decisions(self):
        """同步決策記錄到全局記憶"""
        decisions_file = self.project_memory / "decisions.md"
        
        if not decisions_file.exists():
            print(f"ℹ️  決策文件尚未創建")
            return
        
        # 複製決策文件到全局記憶（保留歷史）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        global_decisions = self.global_memory / f"decisions_{timestamp}.md"
        
        shutil.copy2(decisions_file, global_decisions)
        
        # 創建最新鏈接
        latest_link = self.global_memory / "decisions_latest.md"
        if latest_link.exists():
            latest_link.unlink()
        
        with open(latest_link, 'w', encoding='utf-8') as f:
            f.write(f"# 最新決策記錄\n\n")
            f.write(f"查看: [decisions_{timestamp}.md](./decisions_{timestamp}.md)\n")
            f.write(f"更新時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print(f"✅ 決策記錄已同步到全局記憶")
    
    def sync_specs(self):
        """同步功能規格狀態"""
        specs_dir = self.project_root / ".kiro" / "specs"
        
        if not specs_dir.exists():
            print(f"ℹ️  規格目錄尚未創建")
            return
        
        specs_status = []
        for spec_dir in specs_dir.iterdir():
            if spec_dir.is_dir():
                spec_json = spec_dir / "spec.json"
                if spec_json.exists():
                    with open(spec_json, 'r', encoding='utf-8') as f:
                        spec_data = json.load(f)
                        specs_status.append({
                            "feature": spec_dir.name,
                            "status": spec_data.get("status", "unknown"),
                            "created": spec_data.get("created", "unknown")
                        })
        
        if specs_status:
            status_file = self.session_memory / "specs_status.json"
            with open(status_file, 'w', encoding='utf-8') as f:
                json.dump(specs_status, f, indent=2, ensure_ascii=False)
            
            print(f"✅ 同步了 {len(specs_status)} 個功能規格狀態")
        else:
            print(f"ℹ️  沒有發現功能規格")
    
    def generate_memory_report(self) -> str:
        """生成記憶系統報告"""
        report = []
        report.append("# 記憶系統狀態報告")
        report.append(f"\n生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 統計各層記憶
        for memory_type, path in [
            ("全局記憶", self.global_memory),
            ("專案記憶", self.project_memory),
            ("會話記憶", self.session_memory)
        ]:
            files = list(path.glob("*"))
            report.append(f"\n## {memory_type}")
            report.append(f"- 文件數量: {len(files)}")
            if files:
                report.append("- 包含文件:")
                for f in files[:5]:  # 只顯示前5個
                    report.append(f"  - {f.name}")
                if len(files) > 5:
                    report.append(f"  - ... 還有 {len(files) - 5} 個文件")
        
        return "\n".join(report)
    
    def sync_all(self):
        """執行完整同步"""
        print("\n🔄 開始記憶系統同步...\n")
        
        print("1️⃣  同步研究文檔...")
        self.sync_from_research()
        
        print("\n2️⃣  同步進度狀態...")
        self.sync_progress()
        
        print("\n3️⃣  同步決策記錄...")
        self.sync_decisions()
        
        print("\n4️⃣  同步規格狀態...")
        self.sync_specs()
        
        print("\n5️⃣  生成報告...")
        report = self.generate_memory_report()
        report_file = self.project_memory / "memory_report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✅ 記憶系統同步完成！")
        print(f"📊 報告已保存到: {report_file.relative_to(self.project_root)}")


def main():
    """主函數"""
    import argparse
    
    parser = argparse.ArgumentParser(description="記憶系統同步工具")
    parser.add_argument(
        "--type",
        choices=["all", "research", "progress", "decisions", "specs"],
        default="all",
        help="同步類型 (預設: all)"
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="專案根目錄 (預設: 當前目錄)"
    )
    
    args = parser.parse_args()
    
    syncer = MemorySync(args.project_root)
    
    if args.type == "all":
        syncer.sync_all()
    elif args.type == "research":
        syncer.sync_from_research()
    elif args.type == "progress":
        syncer.sync_progress()
    elif args.type == "decisions":
        syncer.sync_decisions()
    elif args.type == "specs":
        syncer.sync_specs()
    
    print("\n✨ 操作完成！")


if __name__ == "__main__":
    main()