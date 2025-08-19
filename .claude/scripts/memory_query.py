#!/usr/bin/env python3
"""
記憶查詢腳本 - Memory Query Script
用於查詢和搜索專案記憶系統
"""

import os
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from collections import defaultdict

class MemoryQuery:
    """記憶查詢管理器"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.memory_base = self.project_root / ".kiro" / "memory"
        self.global_memory = self.memory_base / "global"
        self.project_memory = self.memory_base / "project"
        self.session_memory = self.memory_base / "session"
        self.research_dir = self.project_root / ".kiro" / "research"
    
    def search_content(self, keyword: str, memory_type: str = "all") -> List[Dict]:
        """在記憶內容中搜索關鍵詞"""
        results = []
        
        # 確定搜索範圍
        if memory_type == "all":
            search_dirs = [self.global_memory, self.project_memory, self.session_memory]
        elif memory_type == "global":
            search_dirs = [self.global_memory]
        elif memory_type == "project":
            search_dirs = [self.project_memory]
        elif memory_type == "session":
            search_dirs = [self.session_memory]
        else:
            print(f"❌ 未知的記憶類型: {memory_type}")
            return results
        
        # 搜索文件
        for search_dir in search_dirs:
            if not search_dir.exists():
                continue
            
            for file_path in search_dir.rglob("*"):
                if file_path.is_file() and file_path.suffix in [".md", ".json", ".txt"]:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        # 搜索關鍵詞
                        if keyword.lower() in content.lower():
                            # 找出匹配的行
                            lines = content.split('\n')
                            matches = []
                            for i, line in enumerate(lines, 1):
                                if keyword.lower() in line.lower():
                                    matches.append({
                                        "line_no": i,
                                        "line": line.strip()[:100]  # 只顯示前100字符
                                    })
                            
                            results.append({
                                "file": str(file_path.relative_to(self.project_root)),
                                "memory_type": search_dir.name,
                                "matches_count": len(matches),
                                "matches": matches[:3]  # 只顯示前3個匹配
                            })
                    except Exception as e:
                        print(f"⚠️  無法讀取文件 {file_path}: {e}")
        
        return results
    
    def query_progress(self) -> Dict:
        """查詢專案進度"""
        progress_file = self.project_memory / "enhancement-progress.md"
        summary_file = self.project_memory / "progress_summary.json"
        
        result = {
            "has_progress_file": progress_file.exists(),
            "has_summary": summary_file.exists(),
            "statistics": {},
            "recent_updates": []
        }
        
        # 讀取進度摘要
        if summary_file.exists():
            with open(summary_file, 'r', encoding='utf-8') as f:
                summary = json.load(f)
                result["statistics"] = summary.get("statistics", {})
                result["last_updated"] = summary.get("last_updated", "unknown")
        
        # 分析進度文件
        if progress_file.exists():
            with open(progress_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 提取最近的更新
            for line in lines:
                if "✅" in line and "2025-" in line:  # 查找包含日期的完成項
                    result["recent_updates"].append(line.strip())
        
        return result
    
    def query_decisions(self) -> List[Dict]:
        """查詢決策記錄"""
        decisions_file = self.project_memory / "decisions.md"
        decisions = []
        
        if not decisions_file.exists():
            return decisions
        
        with open(decisions_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析決策（假設格式為 ### 決策 N：標題）
        pattern = r"### 決策 \d+：(.+?)(?=###|$)"
        matches = re.findall(pattern, content, re.DOTALL)
        
        for match in matches:
            lines = match.strip().split('\n')
            title = lines[0] if lines else "未命名決策"
            
            # 提取關鍵信息
            decision_info = {
                "title": title,
                "content": '\n'.join(lines[1:10])[:200]  # 前200字符
            }
            decisions.append(decision_info)
        
        return decisions
    
    def query_recent_research(self, days: int = 7) -> List[Dict]:
        """查詢最近的研究文檔"""
        research_items = []
        
        if not self.research_dir.exists():
            return research_items
        
        # 獲取日期範圍
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 查找日期目錄
        for date_dir in self.research_dir.iterdir():
            if date_dir.is_dir():
                try:
                    # 解析目錄名為日期
                    dir_date = datetime.strptime(date_dir.name, "%Y-%m-%d")
                    
                    if start_date <= dir_date <= end_date:
                        # 統計該日期的研究文檔
                        md_files = list(date_dir.glob("*.md"))
                        if md_files:
                            research_items.append({
                                "date": date_dir.name,
                                "files_count": len(md_files),
                                "files": [f.name for f in md_files]
                            })
                except ValueError:
                    # 不是日期格式的目錄，跳過
                    continue
        
        return sorted(research_items, key=lambda x: x["date"], reverse=True)
    
    def query_specs_status(self) -> List[Dict]:
        """查詢功能規格狀態"""
        specs_dir = self.project_root / ".kiro" / "specs"
        specs_info = []
        
        if not specs_dir.exists():
            return specs_info
        
        for spec_dir in specs_dir.iterdir():
            if spec_dir.is_dir():
                spec_json = spec_dir / "spec.json"
                
                info = {
                    "feature": spec_dir.name,
                    "has_spec": spec_json.exists(),
                    "files": []
                }
                
                # 讀取規格狀態
                if spec_json.exists():
                    with open(spec_json, 'r', encoding='utf-8') as f:
                        spec_data = json.load(f)
                        info["status"] = spec_data.get("status", "unknown")
                        info["created"] = spec_data.get("created", "unknown")
                
                # 統計文件
                for file_path in spec_dir.glob("*.md"):
                    info["files"].append(file_path.name)
                
                specs_info.append(info)
        
        return specs_info
    
    def generate_memory_map(self) -> str:
        """生成記憶系統地圖"""
        lines = ["# 記憶系統地圖\n"]
        lines.append(f"生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 統計各層記憶
        memory_stats = {}
        for memory_type, path in [
            ("全局記憶", self.global_memory),
            ("專案記憶", self.project_memory),
            ("會話記憶", self.session_memory)
        ]:
            if path.exists():
                files = list(path.glob("**/*"))
                file_count = sum(1 for f in files if f.is_file())
                total_size = sum(f.stat().st_size for f in files if f.is_file())
                
                memory_stats[memory_type] = {
                    "files": file_count,
                    "size": total_size
                }
        
        # 生成統計圖
        lines.append("## 記憶分布\n")
        lines.append("```")
        for mem_type, stats in memory_stats.items():
            size_mb = stats["size"] / (1024 * 1024)
            bar_length = int(stats["files"] / 2)  # 簡單的條形圖
            bar = "█" * min(bar_length, 30)
            lines.append(f"{mem_type:10} [{stats['files']:3}檔] {bar} ({size_mb:.2f}MB)")
        lines.append("```\n")
        
        # 最近活動
        lines.append("## 最近活動\n")
        
        # 查詢最近研究
        recent_research = self.query_recent_research(3)
        if recent_research:
            lines.append("### 最近研究")
            for research in recent_research[:3]:
                lines.append(f"- {research['date']}: {research['files_count']} 個文檔")
        
        # 查詢進度
        progress = self.query_progress()
        if progress["statistics"]:
            lines.append("\n### 進度統計")
            stats = progress["statistics"]
            lines.append(f"- 已完成: {stats.get('completed', 0)}")
            lines.append(f"- 進行中: {stats.get('in_progress', 0)}")
            lines.append(f"- 待處理: {stats.get('pending', 0)}")
        
        return "\n".join(lines)
    
    def smart_query(self, query: str) -> Dict:
        """智能查詢（根據查詢內容自動選擇查詢類型）"""
        result = {
            "query": query,
            "results": {}
        }
        
        # 判斷查詢類型
        if "進度" in query or "progress" in query.lower():
            result["results"]["progress"] = self.query_progress()
        
        if "決策" in query or "decision" in query.lower():
            result["results"]["decisions"] = self.query_decisions()
        
        if "研究" in query or "research" in query.lower():
            result["results"]["research"] = self.query_recent_research()
        
        if "規格" in query or "spec" in query.lower():
            result["results"]["specs"] = self.query_specs_status()
        
        # 如果沒有特定類型，進行內容搜索
        if not result["results"]:
            # 提取可能的關鍵詞
            keywords = [w for w in query.split() if len(w) > 2]
            for keyword in keywords[:3]:  # 最多搜索3個關鍵詞
                search_results = self.search_content(keyword)
                if search_results:
                    result["results"][f"search_{keyword}"] = search_results
        
        return result


def main():
    """主函數"""
    import argparse
    
    parser = argparse.ArgumentParser(description="記憶系統查詢工具")
    parser.add_argument(
        "query_type",
        choices=["search", "progress", "decisions", "research", "specs", "map", "smart"],
        help="查詢類型"
    )
    parser.add_argument(
        "keyword",
        nargs="?",
        help="搜索關鍵詞或智能查詢內容"
    )
    parser.add_argument(
        "--memory-type",
        choices=["all", "global", "project", "session"],
        default="all",
        help="記憶類型（用於搜索）"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="查詢最近N天的研究（預設: 7）"
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="專案根目錄（預設: 當前目錄）"
    )
    
    args = parser.parse_args()
    
    query_manager = MemoryQuery(args.project_root)
    
    if args.query_type == "search":
        if not args.keyword:
            print("❌ 請提供搜索關鍵詞")
        else:
            results = query_manager.search_content(args.keyword, args.memory_type)
            if results:
                print(f"\n🔍 找到 {len(results)} 個包含 '{args.keyword}' 的文件:\n")
                for result in results:
                    print(f"📄 {result['file']}")
                    print(f"   類型: {result['memory_type']}")
                    print(f"   匹配: {result['matches_count']} 處")
                    for match in result['matches']:
                        print(f"   L{match['line_no']}: {match['line']}")
                    print()
            else:
                print(f"ℹ️  沒有找到包含 '{args.keyword}' 的內容")
    
    elif args.query_type == "progress":
        progress = query_manager.query_progress()
        print("\n📊 專案進度查詢結果:\n")
        if progress["statistics"]:
            print("統計數據:")
            for key, value in progress["statistics"].items():
                print(f"  - {key}: {value}")
        if progress["recent_updates"]:
            print("\n最近更新:")
            for update in progress["recent_updates"][:5]:
                print(f"  {update}")
    
    elif args.query_type == "decisions":
        decisions = query_manager.query_decisions()
        if decisions:
            print(f"\n📋 找到 {len(decisions)} 個決策記錄:\n")
            for i, decision in enumerate(decisions, 1):
                print(f"{i}. {decision['title']}")
                print(f"   {decision['content'][:100]}...")
                print()
        else:
            print("ℹ️  沒有找到決策記錄")
    
    elif args.query_type == "research":
        research = query_manager.query_recent_research(args.days)
        if research:
            print(f"\n📚 最近 {args.days} 天的研究文檔:\n")
            for item in research:
                print(f"📅 {item['date']} ({item['files_count']} 個文檔)")
                for file in item['files']:
                    print(f"   - {file}")
                print()
        else:
            print(f"ℹ️  最近 {args.days} 天沒有研究文檔")
    
    elif args.query_type == "specs":
        specs = query_manager.query_specs_status()
        if specs:
            print(f"\n📦 功能規格狀態 ({len(specs)} 個):\n")
            for spec in specs:
                status = spec.get('status', 'unknown')
                print(f"🎯 {spec['feature']} [{status}]")
                if spec['files']:
                    print(f"   文件: {', '.join(spec['files'])}")
                print()
        else:
            print("ℹ️  沒有找到功能規格")
    
    elif args.query_type == "map":
        memory_map = query_manager.generate_memory_map()
        print(memory_map)
    
    elif args.query_type == "smart":
        if not args.keyword:
            print("❌ 請提供查詢內容")
        else:
            result = query_manager.smart_query(args.keyword)
            print(f"\n🤖 智能查詢: '{args.keyword}'\n")
            
            if result["results"]:
                for result_type, data in result["results"].items():
                    print(f"### {result_type}")
                    if isinstance(data, list):
                        for item in data[:3]:
                            print(f"  - {item}")
                    elif isinstance(data, dict):
                        for key, value in list(data.items())[:5]:
                            print(f"  - {key}: {value}")
                    print()
            else:
                print("ℹ️  沒有找到相關結果")
    
    print("\n✨ 查詢完成！")


if __name__ == "__main__":
    main()