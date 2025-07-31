# AI協作開發模板

🎯 **一個完整的AI協作開發環境，專為量化交易項目設計**

## 🚀 快速開始

```bash
# 測試環境
./test_setup.sh

# 開始使用
claude-code
> /spec-init "我的第一個策略" "基於RSI的交易策略"
```

## 📋 核心特色

### 🤖 **整合式開發方法論**
- **SDD** (規格驅動) 作為主框架
- **BDD** (行為驅動) 處理需求
- **DDD** (領域驅動) 處理設計
- **TDD** (測試驅動) 確保品質

### 👥 **10個專業Sub Agents**
- `strategy-analyst` - 策略分析師
- `risk-manager` - 風控專家
- `data-engineer` - 數據工程師
- `api-specialist` - API專家
- `test-engineer` - 測試工程師
- `tech-lead` - 量化技術主管
- `context-manager` - 量化上下文管理專家
- `data-scientist` - 數據科學家
- `hft-researcher` - 高頻交易研究員
- `quant-analyst` - 量化分析師

### ⚡ **自動化Hooks**
- 代碼格式化
- 敏感文件保護
- API調用審計
- 風控自動檢查

### 🔄 **多實例協作**
- 角色分工明確
- 任務自動調度
- Git分支策略
- 進度實時追蹤

## 📖 使用指南

### 標準SDD流程
```bash
# 1. 初始化功能規格
> /spec-init [功能名稱] [描述]

# 2. BDD需求分析
> /spec-requirements [功能名稱]

# 3. DDD技術設計
> /spec-design [功能名稱]

# 4. 任務分解
> /spec-tasks [功能名稱]

# 5. 開始實施
> 現在開始實施 [功能名稱]
```

### Sub Agents使用
```bash
# 顯式調用特定Agent
> 使用 strategy-analyst 分析這個策略的可行性
> 讓 risk-manager 檢查風控規則
> 請 data-engineer 處理市場數據
```

## 📊 監控工具

```bash
# 查看API調用統計
python scripts/monitoring/view_api_audit.py

# 查看項目進度
python .claude/scheduler/spec_scheduler.py report

# 檢查環境狀態
./test_setup.sh
```

## 📁 項目結構

```
├── AI_COLLABORATION_TEMPLATE.md    # 完整模板說明
├── USAGE_GUIDE.md                 # 詳細使用指南
├── CLAUDE.md                      # Claude Code配置
├── setup.sh                       # 一鍵設置腳本
├── test_setup.sh                  # 環境測試腳本
├── .claude/
│   ├── agents/                    # Sub Agents配置
│   ├── commands/                  # Slash Commands
│   ├── scheduler/                 # 任務調度器
│   └── settings.json              # Hooks配置
├── .kiro/
│   ├── steering/                  # 項目知識庫
│   └── specs/                     # 功能規格
├── docs/                          # 文檔目錄
├── src/                           # 源代碼
├── tests/                         # 測試代碼
└── scripts/                       # 工具腳本
```

## 🎯 適用場景

✅ **量化交易系統開發**
✅ **複雜業務邏輯系統**
✅ **需要高代碼品質的項目**
✅ **團隊協作開發**
✅ **AI輔助開發探索**

## 📚 深入了解

- **[AI_COLLABORATION_TEMPLATE.md](AI_COLLABORATION_TEMPLATE.md)** - 完整模板框架
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - 詳細使用指南
- **[CLAUDE.md](CLAUDE.md)** - Claude Code配置說明

## 🆘 獲得幫助

1. 查看使用指南：`USAGE_GUIDE.md`
2. 檢查配置文件：`CLAUDE.md`
3. 運行環境測試：`./test_setup.sh`
4. 查看日誌：`.claude/scheduler/logs/`

---

🎉 **開始您的高效AI協作開發之旅！**