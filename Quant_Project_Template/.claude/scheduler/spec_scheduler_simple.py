#!/usr/bin/env python3
"""
簡化版規格調度器 - 更靈活的項目管理
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class SimpleSpecScheduler:
    def __init__(self):
        self.specs_dir = Path(".kiro/specs")
        self.complexity_thresholds = {
            "simple": 3,     # <= 3 個任務
            "medium": 8,     # 4-8 個任務
            "complex": 999   # > 8 個任務
        }
    
    def analyze_feature(self, feature_name: str) -> Dict:
        """分析功能複雜度並給出建議"""
        spec_path = self.specs_dir / feature_name / "spec.json"
        
        if not spec_path.exists():
            return {
                "status": "not_found",
                "message": f"功能 {feature_name} 未找到"
            }
        
        with open(spec_path, 'r', encoding='utf-8') as f:
            spec = json.load(f)
        
        # 分析複雜度
        task_count = len(spec.get('tasks', []))
        complexity = self._determine_complexity(task_count)
        
        # 生成建議
        recommendations = self._generate_recommendations(complexity, spec)
        
        return {
            "status": "success",
            "feature": feature_name,
            "complexity": complexity,
            "task_count": task_count,
            "current_phase": spec.get('status', 'unknown'),
            "recommendations": recommendations,
            "suggested_experts": self._suggest_experts(spec)
        }
    
    def _determine_complexity(self, task_count: int) -> str:
        """根據任務數量判斷複雜度"""
        if task_count <= self.complexity_thresholds["simple"]:
            return "simple"
        elif task_count <= self.complexity_thresholds["medium"]:
            return "medium"
        else:
            return "complex"
    
    def _generate_recommendations(self, complexity: str, spec: Dict) -> List[str]:
        """根據複雜度生成建議"""
        recommendations = []
        
        if complexity == "simple":
            recommendations.append("✅ 這是個簡單功能，可以直接開始實現")
            recommendations.append("💡 建議：快速完成 MVP，之後根據反饋迭代")
            
        elif complexity == "medium":
            recommendations.append("📋 中等複雜度功能，建議先做簡單設計")
            recommendations.append("💡 考慮諮詢相關專家的意見")
            recommendations.append("🎯 重點：確保核心功能正確實現")
            
        else:  # complex
            recommendations.append("⚠️ 複雜功能，建議使用完整的規格流程")
            recommendations.append("🏗️ 需要仔細的架構設計")
            recommendations.append("👥 建議多個專家協作")
            recommendations.append("📊 考慮分階段實施")
        
        # 添加基於當前狀態的建議
        status = spec.get('status', 'requirements')
        if status == 'requirements':
            recommendations.append(f"▶️ 下一步：澄清需求範圍")
        elif status == 'design':
            recommendations.append(f"▶️ 下一步：完成技術設計")
        elif status == 'implementation':
            recommendations.append(f"▶️ 下一步：開始編碼實現")
        
        return recommendations
    
    def _suggest_experts(self, spec: Dict) -> List[str]:
        """根據功能特徵建議需要諮詢的專家"""
        experts = []
        description = spec.get('description', '').lower()
        
        # 基於關鍵詞的智能推薦
        if any(word in description for word in ['架構', '設計', '重構', '需求', '用戶']):
            experts.append('architect-analyst')
        
        if any(word in description for word in ['算法', 'api', '性能', '優化', '數據']):
            experts.append('developer-specialist')
        
        if any(word in description for word in ['測試', '品質', '安全', '驗證']):
            experts.append('quality-engineer')
        
        if any(word in description for word in ['決策', '技術債', '重大']):
            experts.append('tech-lead')
        
        # 如果沒有明確匹配，根據複雜度推薦
        if not experts:
            task_count = len(spec.get('tasks', []))
            if task_count > 5:
                experts.append('architect-analyst')
        
        return experts
    
    def quick_report(self) -> str:
        """生成簡潔的項目進度報告"""
        if not self.specs_dir.exists():
            return "📂 尚未初始化任何功能"
        
        features = list(self.specs_dir.glob("*/spec.json"))
        if not features:
            return "📂 尚未創建任何功能規格"
        
        report_lines = ["# 📊 項目進度快報\n"]
        report_lines.append(f"生成時間：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        
        # 統計
        total = len(features)
        by_status = {"requirements": 0, "design": 0, "implementation": 0, "completed": 0}
        by_complexity = {"simple": 0, "medium": 0, "complex": 0}
        
        # 功能列表
        report_lines.append("## 功能概覽\n")
        
        for spec_path in features:
            with open(spec_path, 'r', encoding='utf-8') as f:
                spec = json.load(f)
            
            feature_name = spec_path.parent.name
            status = spec.get('status', 'unknown')
            task_count = len(spec.get('tasks', []))
            complexity = self._determine_complexity(task_count)
            
            # 更新統計
            if status in by_status:
                by_status[status] += 1
            by_complexity[complexity] += 1
            
            # 狀態圖標
            status_icon = {
                'requirements': '📝',
                'design': '🎨',
                'implementation': '🔨',
                'completed': '✅'
            }.get(status, '❓')
            
            # 複雜度標記
            complexity_mark = {
                'simple': '🟢',
                'medium': '🟡',
                'complex': '🔴'
            }.get(complexity, '')
            
            report_lines.append(f"{status_icon} **{feature_name}** {complexity_mark}")
            report_lines.append(f"   狀態：{status} | 任務數：{task_count}")
            
            # 完成的任務
            completed_tasks = len([t for t in spec.get('tasks', []) 
                                 if t.get('status') == 'completed'])
            if completed_tasks > 0:
                progress = f"{completed_tasks}/{task_count}"
                report_lines.append(f"   進度：{progress}")
            
            report_lines.append("")
        
        # 統計摘要
        report_lines.append("\n## 📈 統計摘要\n")
        report_lines.append(f"- 總功能數：{total}")
        report_lines.append(f"- 完成數：{by_status['completed']}")
        report_lines.append(f"- 進行中：{by_status['implementation']}")
        report_lines.append(f"- 設計中：{by_status['design']}")
        report_lines.append(f"- 需求階段：{by_status['requirements']}")
        
        report_lines.append("\n## 🎯 複雜度分布\n")
        report_lines.append(f"- 🟢 簡單：{by_complexity['simple']}")
        report_lines.append(f"- 🟡 中等：{by_complexity['medium']}")
        report_lines.append(f"- 🔴 複雜：{by_complexity['complex']}")
        
        # 行動建議
        if by_status['requirements'] > 0:
            report_lines.append("\n## 💡 建議\n")
            report_lines.append("- 有功能還在需求階段，建議優先澄清需求")
        
        if by_complexity['complex'] > 2:
            report_lines.append("- 複雜功能較多，考慮是否可以簡化或分階段實施")
        
        return '\n'.join(report_lines)


def main():
    """命令行入口"""
    import sys
    
    scheduler = SimpleSpecScheduler()
    
    if len(sys.argv) < 2:
        print("使用方式：")
        print("  python spec_scheduler_simple.py report - 生成進度報告")
        print("  python spec_scheduler_simple.py analyze <feature> - 分析特定功能")
        return
    
    command = sys.argv[1]
    
    if command == "report":
        print(scheduler.quick_report())
    
    elif command == "analyze" and len(sys.argv) > 2:
        feature = sys.argv[2]
        result = scheduler.analyze_feature(feature)
        
        if result['status'] == 'success':
            print(f"\n📊 功能分析：{result['feature']}")
            print(f"複雜度：{result['complexity']} ({result['task_count']} 個任務)")
            print(f"當前階段：{result['current_phase']}")
            
            print("\n💡 建議：")
            for rec in result['recommendations']:
                print(f"  {rec}")
            
            if result['suggested_experts']:
                print("\n👥 建議諮詢：")
                for expert in result['suggested_experts']:
                    print(f"  - {expert}")
        else:
            print(result['message'])
    
    else:
        print("未知命令或參數錯誤")


if __name__ == "__main__":
    main()