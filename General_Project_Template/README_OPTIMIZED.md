# 通用AI協作開發模板 (優化版)

🎯 **靈活高效的AI協作開發環境，平衡結構與自由度**

## 🚀 快速開始

```bash
# 測試環境
./test_setup.sh

# 簡單功能 - 使用簡化流程
claude-code
> /spec-init-simple "用戶頭像" "上傳和顯示用戶頭像"

# 複雜功能 - 使用完整流程
> /spec-init "支付系統" "集成多個支付渠道的完整支付解決方案"
```

## 📋 核心理念

### 🎯 **三大開發原則**
1. **MVP 優先** - 從最簡單的解決方案開始
2. **批判性思考** - 質疑需求，提供更好方案
3. **實用主義** - 避免過度設計，專注價值

### 🤖 **智能協作模式**
- 根據任務複雜度自動決定工作方式
- 簡單任務直接處理，複雜任務多角度分析
- 保持 Claude 的自然判斷能力

### 👥 **精簡的專家團隊**
- `architect-analyst` - 架構與需求專家
- `developer-specialist` - 開發專家
- `quality-engineer` - 品質工程師
- `tech-lead` - 技術領導（重大決策）

### ⚡ **輕量級自動化**
- 必要的代碼格式化
- 基本的安全保護
- 簡潔的品質檢查

## 📖 使用指南

### 快速判斷使用哪種流程

```
你的功能是...
├── 簡單的 CRUD？ → 使用 /spec-init-simple
├── UI 小調整？ → 直接實現
├── 涉及支付/安全？ → 使用完整 /spec-init
├── 架構變更？ → 諮詢 architect-analyst
└── 不確定？ → 從簡單開始，按需升級
```

### 簡化工作流程

#### 1. 簡單功能（推薦）
```bash
# 一步初始化
/spec-init-simple "功能名" "描述"

# Claude 會智能判斷並給出建議
# 大多數日常功能都可以這樣開始
```

#### 2. 複雜功能
```bash
# 使用完整流程
/spec-init "功能名" "描述"

# 按需諮詢專家
# 保持靈活性
```

### 實用命令

```bash
# 快速查看進度
python .claude/scheduler/spec_scheduler_simple.py report

# 分析特定功能
python .claude/scheduler/spec_scheduler_simple.py analyze user-auth

# 記錄完成的任務
python .claude/scripts/update_task_log.py "實現用戶登錄" "auth.py" "JWT認證"
```

## 🏗️ 項目結構（精簡版）

```
project/
├── .claude/            # AI 協作配置
│   ├── agents/         # 專家定義（4個）
│   └── commands/       # 快捷命令
├── .kiro/              # 項目知識庫
│   ├── steering/       # 核心知識
│   └── specs/          # 功能規格（按需創建）
├── src/                # 源代碼
└── tests/              # 測試代碼
```

## 💡 最佳實踐

### Do's ✅
- 從簡單開始，逐步迭代
- 相信 Claude 的判斷
- 只在需要時創建文檔
- 保持代碼簡潔
- 主動質疑和優化

### Don'ts ❌
- 不要過度規劃
- 不要為了流程而流程
- 不要創建不必要的抽象
- 不要忽視真正的複雜性
- 不要追求完美

## 🔄 從舊版遷移

如果你在使用原版框架：
1. 查看 `docs/framework_migration_guide.md`
2. 主要變化：更少的強制規則，更多的靈活性
3. 保留核心價值，簡化執行流程

## 📚 進階主題

- 需要多實例協作？查看 `docs/collaboration/`
- 想了解完整 SDD？查看 `docs/guides/sdd-workflow.md`
- Context Engineering 詳情？查看 `.kiro/steering/context_engineering.md`

## 🤝 理念

> "最好的框架是你幾乎感覺不到它存在的框架"

我們相信：
- 簡單勝於複雜
- 靈活勝於僵化
- 實用勝於理論
- 交付勝於完美

---

**記住**：這個框架是為了幫助你更快更好地開發，而不是限制你。當它妨礙你時，請毫不猶豫地調整它。