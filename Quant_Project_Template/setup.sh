#!/bin/bash

# 量化交易AI協作開發模板 - 一鍵設置腳本
# 設置完整的AI協作開發環境

echo "🚀 量化交易AI協作開發模板一鍵設置"
echo "==============================="
echo "這將設置完整的AI協作開發環境，包括："
echo "• 規格驅動開發 (SDD) 框架"
echo "• 上下文工程 (Context Engineering) 原則"
echo "• 多實例協作支援"
echo "• Sub Agents 專業分工"
echo "• Hooks 自動化"
echo "• 代碼品質檢查"
echo "==============================="

# 檢查Python環境
if ! command -v python3 &> /dev/null; then
    echo "❌ 錯誤: 未找到Python3，請先安裝Python3"
    exit 1
fi

echo "✅ Python3環境檢查通過"

# 選擇框架版本
echo ""
echo "🔧 選擇框架版本"
echo "==============="
echo "1) 優化版框架 (推薦) - 靈活高效，適合快速策略開發"
echo "2) 原版框架 - 結構化流程，適合機構級交易系統"
echo ""
read -p "請選擇 (1 或 2，默認為 1): " framework_choice

# 設置默認值
if [ -z "$framework_choice" ]; then
    framework_choice="1"
fi

# 應用框架選擇
if [ "$framework_choice" = "1" ]; then
    echo "✅ 使用優化版框架"
    if [ -f "CLAUDE_OPTIMIZED.md" ]; then
        cp CLAUDE_OPTIMIZED.md CLAUDE.md
        echo "   已配置優化版 CLAUDE.md"
    fi
    FRAMEWORK_TYPE="optimized"
elif [ "$framework_choice" = "2" ]; then
    echo "✅ 使用原版框架"
    FRAMEWORK_TYPE="original"
else
    echo "⚠️  無效選擇，使用默認優化版框架"
    if [ -f "CLAUDE_OPTIMIZED.md" ]; then
        cp CLAUDE_OPTIMIZED.md CLAUDE.md
    fi
    FRAMEWORK_TYPE="optimized"
fi

echo ""

# 創建基本目錄結構
echo "📁 創建目錄結構..."
mkdir -p .claude/agents
mkdir -p .claude/commands  
mkdir -p .claude/scheduler/logs
mkdir -p .claude/scripts
mkdir -p .kiro/steering
mkdir -p .kiro/specs
mkdir -p .kiro/logs/archive
mkdir -p docs/quick_reference
mkdir -p docs/examples/code_patterns
mkdir -p docs/examples/feature_implementations
mkdir -p docs/examples/architectural_patterns
mkdir -p docs/examples/testing_patterns
mkdir -p docs/collaboration
mkdir -p docs/checklists
mkdir -p src/domain
mkdir -p tests/behavior
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p scripts/monitoring

echo "✅ 目錄結構創建完成"

# 創建知識庫文件
echo "📚 初始化項目知識庫..."

cat > .kiro/steering/product.md << 'EOF'
# 產品概述

## 項目目標
[請描述您的項目目標和願景]

## 核心功能
- [功能1]
- [功能2]
- [功能3]

## 目標用戶
[描述您的目標用戶群體]

## 成功標準
[定義項目成功的衡量標準]
EOF

cat > .kiro/steering/tech.md << 'EOF'
# 技術架構

## 技術棧
- 後端: [請填寫]
- 前端: [請填寫]
- 數據庫: [請填寫]
- 部署: [請填寫]

## 架構決策
[記錄重要的技術決策和原因]

## 性能要求
[定義性能指標和要求]
EOF

cat > .kiro/steering/methodology.md << 'EOF'
# 開發方法論

## Context Engineering (上下文工程)
本項目採用上下文工程原則，確保功能實作前有完整的上下文

### 核心原則
- 上下文為王：全面的上下文優於巧妙的提示
- 漸進式開發：從簡單開始，逐步增強
- 驗證驅動：明確的成功標準和驗證關卡

## SDD (規格驅動開發)
本項目使用SDD作為主要開發流程框架

## 階段說明
1. **上下文準備** - 生成實作藍圖和深度分析
2. **需求分析** (BDD) - 理解和定義業務需求
3. **技術設計** (DDD) - 設計系統架構和領域模型
4. **任務分解** - 將設計分解為具體任務
5. **實施開發** (TDD) - 測試驅動的開發實施

## 品質標準
- 上下文完整性分數 > 75%
- 代碼覆蓋率 > 80%
- 所有函數必須有文檔
- 核心邏輯必須有單元測試
EOF

cat > .kiro/steering/collaboration.md << 'EOF'
# 協作規範

## Sub Agents分工
- business-analyst: 需求分析和用戶體驗
- architect: 系統架構和技術設計
- data-specialist: 數據結構和算法
- integration-specialist: API和系統集成
- test-engineer: 測試和品質保證
- tech-lead: 技術決策和代碼審查
- context-manager: 知識管理和文檔維護

## 多實例協作流程
1. 角色分配和責任劃分
2. 定期進度同步
3. 代碼審查和質量控制
4. 文檔維護和更新
EOF

echo "✅ 知識庫初始化完成"

# 創建快速參考文檔
echo "📖 創建快速參考文檔..."

cat > docs/quick_reference/api_design.md << 'EOF'
# API設計指南

## RESTful設計原則
- 使用HTTP動詞 (GET, POST, PUT, DELETE)
- 資源導向的URL設計
- 統一的響應格式
- 適當的HTTP狀態碼

## 最佳實踐
- API版本管理
- 分頁和排序
- 錯誤處理
- 認證和授權
EOF

cat > docs/quick_reference/design_patterns.md << 'EOF'
# 設計模式參考

## 常用模式
- 單例模式 (Singleton)
- 工廠模式 (Factory)
- 觀察者模式 (Observer)
- 策略模式 (Strategy)

## DDD模式
- 實體 (Entity)
- 值對象 (Value Object)
- 聚合根 (Aggregate Root)
- 領域服務 (Domain Service)
EOF

echo "✅ 快速參考文檔創建完成"

# 創建Git忽略文件
echo "📝 創建配置文件..."

if [ ! -f .gitignore ]; then
cat > .gitignore << 'EOF'
# Logs
*.log
logs/
.claude/scheduler/logs/*.log

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/
htmlcov/

# nyc test coverage
.nyc_output

# Dependency directories
node_modules/
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
.command_audit.log
.quality_check_report.json
EOF

echo "✅ .gitignore 文件創建完成"
fi

# 設置腳本權限
chmod +x test_setup.sh
chmod +x .claude/scheduler/spec_scheduler.py
chmod +x .claude/scheduler/quality_check.py
chmod +x .claude/scheduler/security_check.py
chmod +x .claude/scheduler/context_validator.py
chmod +x .claude/scripts/update_task_log.py
chmod +x scripts/monitoring/view_command_audit.py

# 確保委派檢查清單存在
if [ ! -f ".claude/AGENT_DELEGATION_CHECKLIST.md" ]; then
    echo "⚠️  創建委派檢查清單..."
    touch .claude/AGENT_DELEGATION_CHECKLIST.md
fi

echo "✅ 腳本權限設置完成"

# 創建示例項目結構
echo "📦 創建示例代碼結構..."

cat > src/domain/__init__.py << 'EOF'
"""
領域層模組
包含核心業務邏輯和領域模型
"""
EOF

cat > tests/__init__.py << 'EOF'
"""
測試模組
"""
EOF

cat > tests/test_example.py << 'EOF'
"""
示例測試文件
"""
import unittest

class TestExample(unittest.TestCase):
    def test_example(self):
        """示例測試案例"""
        self.assertEqual(1 + 1, 2)

if __name__ == '__main__':
    unittest.main()
EOF

echo "✅ 示例代碼結構創建完成"

# 運行測試檢查
echo "🧪 運行環境測試..."
if [ -f "test_setup.sh" ]; then
    ./test_setup.sh
else
    echo "⚠️  測試腳本不存在，跳過環境測試"
fi

echo ""
echo "🎉 設置完成！"
echo ""

# 根據框架類型顯示不同的指導
if [ "$FRAMEWORK_TYPE" = "optimized" ]; then
    echo "📋 下一步操作（優化版框架）："
    echo "1. 運行 'claude-code' 啟動開發環境"
    echo "2. 使用 '/spec-init-simple [策略名稱] [描述]' 快速創建策略（推薦）"
    echo "3. 複雜策略可使用 '/spec-init [策略名稱] [描述]' 完整流程"
    echo "4. 查看 README.md 了解量化交易開發指南"
    echo ""
    echo "💡 優化版特色："
    echo "• 快速策略原型開發"
    echo "• 智能判斷策略複雜度"
    echo "• 簡單策略直接實現"
    echo "• 複雜策略自動建議風控評估"
else
    echo "📋 下一步操作（原版框架）："
    echo "1. 運行 'claude-code' 啟動開發環境"
    echo "2. 使用 '/spec-init [策略名稱] [描述]' 創建第一個策略"
    echo "3. 使用 '/spec-generate-prp [策略名稱]' 生成實作藍圖"
    echo "4. 使用 '/spec-ultrathink [策略名稱]' 進行深度分析"
    echo "5. 查看 USAGE_GUIDE.md 了解詳細使用方法"
    echo ""
    echo "📌 原版特色："
    echo "• 完整的風控評估流程"
    echo "• 強制性的策略回測"
    echo "• 詳細的策略文檔"
    echo "• 適合機構級交易系統"
fi

echo ""
echo "🔧 通用命令："
echo "• ./test_setup.sh - 檢查環境狀態"
echo "• python .claude/scheduler/spec_scheduler.py report - 查看策略進度"
echo "• python .claude/scripts/update_task_log.py - 記錄任務執行"
echo "• python scripts/monitoring/view_command_audit.py - 查看命令統計"

# 框架切換提示
echo ""
echo "💡 提示：如需切換框架版本，可手動操作："
if [ "$FRAMEWORK_TYPE" = "optimized" ]; then
    echo "   切換到原版：保留當前 CLAUDE.md"
else
    echo "   切換到優化版：cp CLAUDE_OPTIMIZED.md CLAUDE.md"
fi
echo ""

exit 0