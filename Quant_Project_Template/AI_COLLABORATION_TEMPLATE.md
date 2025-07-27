# AI協作開發項目模板

**基於Claude-Claude Code多實例協作與量化交易開發經驗**

這是一個完整的AI協作開發項目模板，整合了多實例協作、規格驅動開發(SDD)、行為驅動開發(BDD)、領域驅動設計(DDD)、測試驅動開發(TDD)，以及最新的Sub Agents和Hooks功能。

## 📋 目錄結構

```
ai-collaboration-project/
├── README.md                          # 項目說明
├── CLAUDE.md                          # Claude Code 主配置
├── setup.sh                           # 一鍵設置腳本
├── .claude/
│   ├── commands/                      # 自定義命令
│   │   ├── spec-init.md              # 初始化規格
│   │   ├── spec-requirements.md       # 需求分析
│   │   ├── spec-design.md            # 技術設計
│   │   ├── spec-tasks.md             # 任務分解
│   │   └── quant/                    # 量化交易專用命令
│   │       ├── validate-strategy.md
│   │       ├── backtest.md
│   │       ├── optimize.md
│   │       └── risk-check.md
│   ├── agents/                       # Sub Agents 配置
│   │   ├── strategy-analyst.md       # 策略分析師
│   │   ├── risk-manager.md           # 風控專家
│   │   ├── data-engineer.md          # 數據工程師
│   │   ├── api-specialist.md         # API專家
│   │   ├── test-engineer.md          # 測試專家
│   │   └── code-reviewer.md          # 代碼審查員
│   ├── scheduler/                    # 任務調度器
│   │   ├── spec_scheduler.py         # 主調度器
│   │   ├── progress_tracker.py       # 進度追蹤
│   │   └── logs/                     # 日誌目錄
│   ├── templates/                    # 模板文件
│   │   ├── bdd_scenario.feature      # BDD場景模板
│   │   ├── ddd_model.py              # DDD模型模板
│   │   ├── strategy_template.py      # 策略模板
│   │   └── risk_template.py          # 風控模板
│   └── settings.json                 # Hooks配置
├── .kiro/
│   ├── steering/                     # 項目知識庫
│   │   ├── product.md                # 產品概述
│   │   ├── tech.md                   # 技術架構
│   │   ├── structure.md              # 項目結構
│   │   ├── methodology.md            # 開發方法論
│   │   ├── trading_rules.md          # 交易規則
│   │   └── collaboration.md          # 協作規範
│   └── specs/                        # 功能規格
│       └── [feature-name]/
│           ├── spec.json             # 規格狀態
│           ├── requirements.md       # 需求文檔
│           ├── design.md             # 設計文檔
│           └── tasks.md              # 任務清單
├── docs/
│   ├── quick_reference/              # 快速參考
│   │   ├── api_endpoints.md          # API端點
│   │   ├── data_schema.md            # 數據結構
│   │   ├── timezone_handling.md     # 時區處理
│   │   ├── settlement_rules.md      # 結算規則
│   │   └── error_codes.md           # 錯誤代碼
│   ├── detailed/                     # 詳細文檔
│   │   ├── api_full_guide.md         # 完整API指南
│   │   ├── market_data_spec.md       # 市場數據規範
│   │   └── business_rules.md         # 業務規則
│   ├── checklists/                   # 檢查清單
│   │   ├── pre_api_call.md           # API調用前
│   │   ├── data_validation.md        # 數據驗證
│   │   ├── strategy_review.md        # 策略審查
│   │   └── deployment.md             # 部署檢查
│   ├── collaboration/                # 協作指南
│   │   ├── multi_instance.md         # 多實例協作
│   │   ├── role_assignment.md        # 角色分配
│   │   └── workflow.md               # 工作流程
│   └── examples/                     # 使用範例
│       ├── strategy_development.md   # 策略開發
│       ├── bdd_scenarios.md          # BDD場景
│       └── agent_usage.md            # Agent使用
├── src/
│   ├── domain/                       # DDD領域層
│   │   ├── entities/                 # 實體
│   │   ├── value_objects/            # 值對象
│   │   ├── aggregates/               # 聚合根
│   │   └── services/                 # 領域服務
│   ├── application/                  # 應用層
│   │   ├── strategies/               # 策略服務
│   │   ├── backtesting/              # 回測服務
│   │   └── execution/                # 執行服務
│   ├── infrastructure/               # 基礎設施層
│   │   ├── market_data/              # 市場數據
│   │   ├── brokers/                  # 券商接口
│   │   └── persistence/              # 持久化
│   └── utils/                        # 工具函數
├── tests/
│   ├── behavior/                     # BDD測試
│   │   └── features/                 # Gherkin場景
│   ├── unit/                         # TDD單元測試
│   ├── integration/                  # 整合測試
│   └── fixtures/                     # 測試數據
├── scripts/
│   ├── setup_integrated_system.py   # 整合系統設置
│   ├── migrate_quant_project.py     # 量化項目遷移
│   ├── setup_agents_hooks.py       # Sub Agents設置
│   └── monitoring/                   # 監控腳本
│       ├── view_api_audit.py        # API審計查看
│       └── performance_monitor.py    # 性能監控
└── examples/
    ├── strategies/                   # 策略範例
    ├── workflows/                    # 工作流程範例
    └── integrations/                 # 整合範例
```

## 🚀 快速開始

### 1. 一鍵設置

```bash
# 克隆模板到新項目
git clone [template-repo] my-ai-project
cd my-ai-project

# 執行一鍵設置
./setup.sh

# 或分步執行
python scripts/setup_integrated_system.py
python scripts/setup_agents_hooks.py
```

### 2. 初始化項目

```bash
# 啟動Claude Code
claude-code

# 初始化項目知識庫
> /steering-init

# 添加項目特定配置
> /steering-custom trading-rules "高頻交易規則與風控要求"
> /steering-custom api-spec "內部API規範與限制"
```

### 3. 開始第一個功能

```bash
# 創建功能規格
> /spec-init "實現基於RSI的均值回歸策略"

# 系統會自動進入SDD流程
# 1. 需求定義 (使用BDD)
# 2. 技術設計 (使用DDD)  
# 3. 任務分解 (混合方法)
# 4. 實施開發 (Sub Agents協作)
```

## 🤖 核心功能

### 1. 多實例協作系統

支援多個Claude Code實例協作開發：

- **角色分工**：架構師、後端、前端、測試、風控
- **任務調度**：自動分配任務給合適的實例
- **進度同步**：統一的進度追蹤和狀態管理
- **衝突管理**：Git分支策略避免代碼衝突

### 2. 整合式開發方法論

結合四種互補的開發方法：

- **SDD (Spec-Driven)**：主框架，提供開發流程結構
- **BDD (Behavior-Driven)**：需求工具，描述業務行為
- **DDD (Domain-Driven)**：設計工具，建立領域模型
- **TDD (Test-Driven)**：品質工具，確保計算正確

### 3. Sub Agents專業分工

5個專業Sub Agent處理不同領域：

- **strategy-analyst**：策略分析和BDD場景生成
- **risk-manager**：風險管理和倉位控制
- **data-engineer**：數據處理和特徵工程
- **api-specialist**：API集成和性能優化
- **test-engineer**：自動化測試和品質保證

### 4. Hooks自動化

多層自動化檢查和處理：

- **PreToolUse**：API審計、敏感文件保護
- **PostToolUse**：代碼格式化、自動測試
- **Stop**：風控檢查、完整性驗證

### 5. 任務調度器

智能化的開發流程管理：

- **階段管理**：SDD的requirements → design → tasks → implementation
- **自動分配**：根據任務類型選擇合適的Sub Agent
- **進度追蹤**：實時監控開發進度
- **人工審核**：關鍵階段需要人工確認

## 📖 使用指南

### 策略開發完整流程

```bash
# 1. 策略構思
> 使用 strategy-analyst 分析"當RSI<30且價格觸及布林帶下軌時做多"的策略

# 2. 風險評估
> 讓 risk-manager 評估這個策略的風險並給出倉位建議

# 3. 數據準備
> 使用 data-engineer 準備AAPL過去兩年的日線數據

# 4. 實施開發
> 現在實施這個策略
# (test-engineer會自動介入確保測試覆蓋)

# 5. 回測驗證
> /quant:backtest AAPL 2022-01-01 2024-01-01

# 6. 風控檢查
> /quant:risk-check
```

### 多實例協作工作流

```bash
# Terminal 1 - 策略架構師
claude-code --role architect
> 負責整體策略設計和技術架構

# Terminal 2 - 後端開發
claude-code --role backend  
> 實現數據處理和策略邏輯

# Terminal 3 - 風控專家
claude-code --role risk
> 實現風險管理和倉位控制

# Terminal 4 - 測試工程師
claude-code --role test
> 實現測試框架和品質保證
```

### BDD場景驅動開發

```gherkin
# tests/behavior/features/rsi_strategy.feature
Feature: RSI超賣反彈策略
  作為量化交易員
  我希望在RSI超賣時自動開倉
  以便捕捉反彈機會

  Background:
    Given 使用日線數據
    And 交易標的為AAPL
    And 初始資金為100000

  Scenario: 標準超賣開倉
    Given RSI(14) 低於 30
    And 價格接近布林帶下軌
    And 成交量高於20日均量
    When RSI形成金叉
    Then 開多倉2%倉位
    And 設置停損在入場價-1.5%
    And 設置止盈在入場價+3%

  Scenario: 風控觸發
    Given 持有多倉位
    When 未實現虧損達到2%
    Then 立即平倉
    And 記錄風控事件
```

### DDD領域建模

```python
# src/domain/entities/strategy.py
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional
from datetime import datetime

@dataclass(frozen=True)
class RSISignal(ValueObject):
    """RSI信號值對象"""
    value: Decimal
    period: int
    timestamp: datetime
    confidence: Decimal

class TradingStrategy(Entity):
    """交易策略聚合根"""
    def __init__(self, strategy_id: StrategyId, name: str):
        self.id = strategy_id
        self.name = name
        self.signals: List[Signal] = []
        self.positions: List[Position] = []
        self.risk_manager: RiskManager = None
        
    def generate_signal(self, market_data: MarketData) -> Optional[Signal]:
        """生成交易信號"""
        # 策略邏輯實現
        pass
        
    def validate_risk_rules(self, signal: Signal) -> bool:
        """驗證風控規則"""
        return self.risk_manager.validate(signal)
```

## ⚙️ 配置與自定義

### 1. 調整Sub Agent行為

編輯 `.claude/agents/[agent-name].md` 修改系統提示詞：

```markdown
---
name: strategy-analyst
description: 策略分析專家，負責分析交易策略邏輯
tools: Read, Write, Grep, Analysis
---

你是資深的量化策略分析師，專門負責：
1. 策略需求分析
2. BDD場景生成  
3. 策略評估
...
```

### 2. 添加自定義Hooks

編輯 `.claude/settings.json`：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command", 
            "command": "python validate_trading_logic.py"
          }
        ]
      }
    ]
  }
}
```

### 3. 創建專案特定命令

在 `.claude/commands/` 添加新命令：

```markdown
# .claude/commands/deploy-strategy.md
部署策略到生產環境：

1. 運行完整測試套件
2. 檢查風控規則
3. 備份當前配置
4. 更新策略參數
5. 監控初始運行
```

## 🔒 安全與合規

### 1. 敏感文件保護

- 自動阻止修改 `.env`、`credentials`、`api_keys` 等文件
- API密鑰使用環境變量管理
- 生產配置與開發環境隔離

### 2. API調用審計

- 所有API調用自動記錄到 `.api_audit.log`
- 包含時間戳、端點、參數、響應時間
- 定期審計和異常檢測

### 3. 風控自動檢查

- 每次完成開發後自動檢查止損設置
- 驗證倉位限制和風險參數
- 異常交易邏輯警告

## 📊 監控與維護

### 1. 進度追蹤

```bash
# 查看項目整體進度
python scripts/monitoring/progress_tracker.py

# 查看特定功能進度  
python scripts/monitoring/progress_tracker.py --feature rsi-strategy
```

### 2. API審計分析

```bash
# 分析API調用模式
python scripts/monitoring/view_api_audit.py

# 性能監控
python scripts/monitoring/performance_monitor.py
```

### 3. 日誌管理

```bash
# 查看調度器日誌
tail -f .claude/scheduler/logs/scheduler.log

# 查看Sub Agent活動
grep "agent:" .claude/scheduler/logs/*.log
```

## 🎯 最佳實踐

### 1. 開發流程

1. **永遠從規格開始**：使用 `/spec-init` 創建功能規格
2. **遵循SDD流程**：requirements → design → tasks → implementation
3. **善用Sub Agents**：讓專業的agent處理專業的事
4. **頻繁提交**：保持Git歷史清晰可追溯
5. **人工審核關鍵點**：每個SDD階段都需要確認

### 2. 協作管理

1. **明確角色分工**：每個實例專注特定領域
2. **統一溝通規範**：使用標準的術語和格式
3. **定期同步進度**：避免工作重複和衝突
4. **文檔即時更新**：保持文檔與代碼同步

### 3. 品質保證

1. **測試驅動**：關鍵邏輯先寫測試
2. **行為優先**：用BDD描述業務邏輯
3. **持續驗證**：利用Hooks自動檢查
4. **風險意識**：交易邏輯必須有風控

### 4. 性能優化

1. **Sub Agent專業化**：避免過於通用的agent
2. **Hook輕量化**：保持Hook邏輯簡單快速
3. **上下文管理**：利用獨立上下文保持聚焦
4. **資源監控**：定期檢查系統資源使用

## 🔄 升級與擴展

### 1. 新增Sub Agent

```bash
# 使用互動式創建
> /agents

# 或手動創建
mkdir -p .claude/agents
echo '---
name: performance-optimizer
description: 性能優化專家
---
你是性能優化專家...' > .claude/agents/performance-optimizer.md
```

### 2. 擴展命令集

```bash
# 創建新的slash command
mkdir -p .claude/commands/custom
echo '# 自定義命令說明...' > .claude/commands/custom/my-command.md
```

### 3. 整合新工具

編輯 `CLAUDE.md` 添加新工具的觸發詞：

```markdown
### 觸發詞自動查閱機制
- `new_tool` → 查閱 `docs/quick_reference/new_tool.md`
```

## 🆘 故障排除

### 常見問題

1. **Sub Agent未被調用**
   - 檢查description是否包含觸發關鍵詞
   - 嘗試顯式調用：「使用 [agent-name] 來...」

2. **Hooks未觸發**
   - 檢查 `.claude/settings.json` 語法
   - 確認matcher模式正確

3. **任務調度器異常**
   - 查看 `.claude/scheduler/logs/scheduler.log`
   - 重新啟動調度器

4. **Git衝突**
   - 使用分支隔離：每個實例一個分支
   - 定期merge和resolve衝突

### 獲得幫助

1. **檢查日誌**：`.claude/scheduler/logs/`
2. **查看配置**：`CLAUDE.md` 和 `.claude/settings.json`
3. **測試基本功能**：運行 `./scripts/test_agents.sh`
4. **重置環境**：備份後重新運行設置腳本

---

這個模板提供了一個完整的AI協作開發環境，特別適合複雜的量化交易項目。通過整合多種開發方法論和最新的AI功能，它能顯著提升開發效率和代碼品質。

每次開新項目時，基於這個模板開始，你將擁有一個專業、高效、安全的AI協作開發環境！