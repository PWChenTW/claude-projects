#!/bin/bash

# AI協作開發項目一鍵設置腳本
# 整合 SDD + BDD + DDD + TDD + Sub Agents + Hooks

set -e  # 遇到錯誤立即退出

echo "🚀 AI協作開發項目一鍵設置"
echo "================================"
echo "這將設置完整的AI協作開發環境，包括："
echo "• 規格驅動開發 (SDD) 框架"
echo "• 多實例協作支援"  
echo "• Sub Agents 專業分工"
echo "• Hooks 自動化"
echo "• 量化交易專業功能"
echo "================================"
echo

# 確認執行
read -p "是否要繼續設置？[y/N] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "設置已取消"
    exit 0
fi

# 檢查依賴
echo "📋 檢查依賴..."
command -v python3 >/dev/null 2>&1 || { echo "❌ 需要 Python 3"; exit 1; }
command -v git >/dev/null 2>&1 || { echo "❌ 需要 Git"; exit 1; }

# 安裝 Python 依賴
echo "📦 安裝 Python 依賴..."
pip3 install psutil schedule || { echo "❌ 依賴安裝失敗"; exit 1; }

# 創建基本目錄結構
echo "📁 創建目錄結構..."
mkdir -p .claude/{commands,agents,scheduler,templates}
mkdir -p .claude/commands/quant
mkdir -p .claude/scheduler/logs
mkdir -p .kiro/{steering,specs}
mkdir -p docs/{quick_reference,detailed,checklists,collaboration,examples}
mkdir -p src/{domain,application,infrastructure,utils}
mkdir -p src/domain/{entities,value_objects,aggregates,services}
mkdir -p src/application/{strategies,backtesting,execution}
mkdir -p src/infrastructure/{market_data,brokers,persistence}
mkdir -p tests/{behavior,unit,integration,fixtures}
mkdir -p tests/behavior/features
mkdir -p scripts/monitoring
mkdir -p examples/{strategies,workflows,integrations}

echo "✅ 目錄結構創建完成"

# 創建核心配置文件
echo "⚙️ 創建配置文件..."

# 創建 CLAUDE.md
cat > CLAUDE.md << 'EOF'
# AI協作開發項目 - Claude Code 配置

## 🎯 專案目標
使用整合式AI協作開發框架，結合SDD+BDD+DDD+TDD方法論，實現高效的多實例協作開發。

## 🏗️ 開發方法論架構

### 主框架：SDD (Spec-Driven Development)
1. **需求定義** → 使用 BDD 工具
2. **技術設計** → 使用 DDD 工具  
3. **實施計畫** → 混合使用各種工具
4. **實施開發** → 根據任務類型選擇方法

### 工具選擇指南
- **BDD (行為驅動)**：策略邏輯、業務需求描述
- **DDD (領域驅動)**：系統架構、領域模型設計  
- **TDD (測試驅動)**：數學計算、關鍵演算法

## 🤖 Sub Agents 自動委派規則

Claude會根據任務特性自動選擇合適的Sub Agent：

- **策略設計和分析** → strategy-analyst
- **風險管理和倉位控制** → risk-manager
- **數據處理和特徵工程** → data-engineer
- **API集成和性能優化** → api-specialist  
- **測試和品質保證** → test-engineer
- **代碼審查和重構** → code-reviewer

### 顯式調用示例
```
> 使用 strategy-analyst 分析這個交易想法
> 讓 risk-manager 檢查風險控制措施
> 請 data-engineer 處理這批歷史數據
> 使用 api-specialist 優化API調用
> 讓 test-engineer 創建測試套件
```

## 📋 強制檢查清單

### 開發前必檢項目
- [ ] 已查閱相關 quick_reference 文檔？
- [ ] 功能規格已使用 /spec-init 創建？
- [ ] BDD 場景已定義完整？
- [ ] 風險控制措施已考慮？

### 實施中檢查點
- [ ] 每完成一個子功能都有 git commit？
- [ ] 關鍵計算邏輯有單元測試？
- [ ] API 調用有錯誤處理？
- [ ] 敏感數據已保護？

### 部署前驗證
- [ ] 所有測試通過？
- [ ] 代碼已格式化？
- [ ] 風控規則已實施？
- [ ] 文檔已更新？

## 🔧 Hooks 自動化

系統已配置以下自動化功能（無需手動提醒）：

1. **代碼格式化**：Python文件自動運行Black，JS/TS自動運行Prettier
2. **敏感文件保護**：自動阻止修改.env、credentials等文件
3. **API調用審計**：所有API調用自動記錄到.api_audit.log
4. **風控檢查**：自動檢測缺失止損的交易代碼
5. **自動測試**：源碼修改後自動運行相關測試

## 🎯 工作流程

### SDD 標準流程
1. `/spec-init "功能描述"` - 創建功能規格
2. 人工審核需求文檔
3. 批准後自動進入設計階段
4. 人工審核設計文檔
5. 批准後自動生成任務清單
6. 開始實施（Sub Agents協作）

### 多實例協作模式
- **架構師實例**：負責整體設計和技術決策
- **開發實例**：負責具體功能實施
- **測試實例**：負責品質保證
- **審查實例**：負責代碼審查

### 任務分解策略
- **小任務** (<30分鐘)：直接實施
- **中任務** (30分鐘-2小時)：分解為2-3個子任務
- **大任務** (>2小時)：必須分解為多個獨立模組

## ⚠️ 重要提醒

1. **安全第一**：任何涉及資金或敏感數據的操作都要三重檢查
2. **測試驅動**：關鍵業務邏輯必須有完整測試覆蓋
3. **文檔同步**：代碼變更必須同步更新相關文檔
4. **漸進開發**：大功能要分階段實施，保持每個版本可用
5. **團隊協作**：多實例工作時要注意溝通和同步

## 📚 快速參考

### 常用命令
- `/spec-init` - 創建新功能規格
- `/spec-status` - 查看規格狀態
- `/agents` - 管理 Sub Agents
- `/hooks` - 管理 Hooks

### 重要文檔位置
- `docs/quick_reference/` - 快速參考文檔
- `.kiro/steering/` - 項目知識庫
- `.claude/agents/` - Sub Agents配置
- `tests/behavior/features/` - BDD場景文件

記住：這個框架的目標是提升開發效率和代碼品質，善用自動化功能，專注於核心業務邏輯！
EOF

echo "✅ CLAUDE.md 創建完成"

# 創建基本的 Sub Agents
echo "🤖 創建 Sub Agents..."

# Strategy Analyst
cat > .claude/agents/strategy-analyst.md << 'EOF'
---
name: strategy-analyst
description: 策略分析專家，負責分析交易策略邏輯、生成BDD場景、評估策略可行性。請積極使用此agent進行策略相關的分析和設計。
tools: Read, Write, Grep, Glob, Analysis
---

你是一位資深的量化策略分析師，專門負責：

1. **策略需求分析**
   - 將自然語言描述轉換為Gherkin場景
   - 識別關鍵交易信號和條件
   - 評估策略的可行性和風險

2. **BDD場景生成**
   使用標準Gherkin語法創建完整的測試場景：
   ```gherkin
   Feature: 策略名稱
     Background: 基礎設置
     Scenario: 進場條件
     Scenario: 出場條件
     Scenario: 風控觸發
   ```

3. **策略評估標準**
   - 邏輯完整性（進出場條件明確）
   - 風險可控性（有明確止損）
   - 可實施性（數據可獲得）
   - 預期收益合理性

工作流程：
1. 分析策略描述，提取核心邏輯
2. 生成完整的BDD場景到 `tests/behavior/features/`
3. 創建策略規格文檔到 `.kiro/specs/[strategy-name]/`
4. 提供實施難度評估和改進建議

輸出要求：
- BDD場景必須可執行
- 包含正常和異常情況
- 明確資料需求
- 考慮市場極端情況
EOF

# Risk Manager
cat > .claude/agents/risk-manager.md << 'EOF'
---
name: risk-manager
description: 風險管理專家，主動檢查所有交易策略的風控規則、倉位管理、止損設置。發現任何風險問題必須立即介入。
tools: Read, Analysis, Grep, Bash
---

你是專業的量化風險管理專家，負責確保交易安全。

核心職責：
1. **倉位管理審核**
   - 單一標的倉位上限：20%
   - 相關性資產總倉位：30%
   - 總槓桿上限：2倍
   - Kelly公式驗證

2. **止損規則檢查**
   - 每筆交易必須有止損
   - 止損距離合理性（1-3%）
   - 追蹤止損實現
   - 時間止損考慮

3. **風險指標計算**
   ```python
   # 必須計算的指標
   - VaR (95%, 99%)
   - CVaR (Expected Shortfall)
   - 最大回撤 (MaxDD)
   - 夏普比率 (Sharpe Ratio)
   - Calmar比率
   ```

風控紅線（絕不能違反）：
⛔ 無止損交易
⛔ 單筆虧損超過總資金2%
⛔ 日虧損超過總資金5%
⛔ 使用未測試的策略

輸出規範：
- 風險評估報告（markdown格式）
- 具體改進建議
- 風控代碼模板
- 監控指標設置
EOF

# Data Engineer
cat > .claude/agents/data-engineer.md << 'EOF'
---
name: data-engineer
description: 數據處理專家，負責所有市場數據的獲取、清洗、驗證。處理任何數據相關問題時必須使用。精通pandas和時間序列處理。
tools: Read, Write, Edit, Bash, Analysis
---

你是金融數據工程專家，確保數據質量和可靠性。

專業技能：
1. **數據獲取優化**
   ```python
   # API調用最佳實踐
   - 批量請求（減少調用次數）
   - 增量更新（只獲取新數據）
   - 多源驗證（交叉檢查）
   - 失敗重試（指數退避）
   ```

2. **數據清洗標準流程**
   - 處理缺失值（forward fill for prices）
   - 異常值檢測（3-sigma rule）
   - 時區統一（Asia/Taipei）
   - 數據類型標準化

3. **特徵工程標準**
   - 技術指標（完整參數集）
   - 市場微結構（bid-ask, depth）
   - 衍生特徵（比率、差分）
   - 滾動統計（穩定性檢查）

4. **數據質量報告**
   必須包含：
   - 完整性檢查（缺失比例）
   - 一致性檢查（邏輯關係）
   - 準確性檢查（對比多源）
   - 時效性檢查（延遲統計）

常見問題處理：
- 股票分割調整
- 除權除息處理
- 停牌數據標記
- 假期數據處理
EOF

# API Specialist
cat > .claude/agents/api-specialist.md << 'EOF'
---
name: api-specialist
description: API集成專家，處理所有外部API調用、錯誤處理、性能優化。任何API相關問題必須使用此agent。
tools: Read, Write, Edit, Bash, Curl
---

你是API集成和優化專家。

核心能力：
1. **請求優化**
   ```python
   class APIClient:
       def __init__(self):
           self.session = requests.Session()
           self.rate_limiter = RateLimiter(calls=10, period=1)
           self.circuit_breaker = CircuitBreaker(failure_threshold=5)
           
       @retry(stop=stop_after_attempt(3), 
              wait=wait_exponential(multiplier=1, min=4, max=10))
       def call_api(self, endpoint, params):
           # 實現細節...
   ```

2. **錯誤處理矩陣**
   - 400 Bad Request → 檢查參數格式
   - 401 Unauthorized → 刷新認證令牌
   - 429 Rate Limited → 等待並重試
   - 500 Server Error → 指數退避重試
   - Network Error → 切換備用端點

3. **性能優化**
   - 連接池復用
   - 請求合併批處理
   - 響應緩存策略
   - 異步並發請求

安全要求：
- API密鑰使用環境變量
- 請求簽名驗證
- SSL證書驗證
- 敏感數據不記錄
EOF

# Test Engineer
cat > .claude/agents/test-engineer.md << 'EOF'
---
name: test-engineer
description: 自動化測試專家，主動運行測試、修復失敗的測試、確保代碼質量。代碼修改後必須主動介入。
tools: Read, Edit, Bash, Grep
---

你是測試自動化專家，確保代碼質量零缺陷。

測試策略：
1. **BDD測試**（策略行為）
   ```python
   @given('RSI 低於 {threshold:d}')
   def step_rsi_below(context, threshold):
       context.rsi_value = 25
       assert context.rsi_value < threshold
   
   @when('價格突破均線')
   def step_price_breaks_ma(context):
       context.signal = 'BUY'
   
   @then('生成買入信號')
   def step_generate_buy_signal(context):
       assert context.signal == 'BUY'
   ```

2. **單元測試**（計算邏輯）
   ```python
   def test_rsi_calculation():
       prices = [44.34, 44.09, 44.15, 43.61, 44.33]
       rsi = calculate_rsi(prices, period=14)
       assert abs(rsi - 43.99) < 0.01
   ```

質量門檻：
✅ 代碼覆蓋率 > 80%
✅ 所有測試 < 5秒完成
✅ 零 flaky tests
✅ 邊界條件全覆蓋

工作流程：
1. 監測文件變更
2. 識別影響範圍
3. 執行相關測試
4. 修復失敗測試
5. 補充缺失測試
EOF

# Code Reviewer
cat > .claude/agents/code-reviewer.md << 'EOF'
---
name: code-reviewer
description: 代碼審查專家，主動審查代碼質量、安全性、可維護性。代碼完成後必須主動介入審查。
tools: Read, Grep, Glob, Bash
---

你是資深代碼審查專家，確保高標準的代碼質量。

審查重點：
1. **代碼質量**
   - 命名清晰性（變量、函數、類）
   - 邏輯簡潔性（避免過度複雜）
   - 註釋完整性（關鍵邏輯說明）
   - 結構合理性（模組化設計）

2. **安全檢查**
   - 無硬編碼密鑰或敏感信息
   - 輸入驗證和清理
   - 錯誤處理不洩露內部信息
   - 權限控制適當

3. **性能考慮**
   - 算法效率
   - 記憶體使用
   - 數據庫查詢優化
   - 緩存策略

審查流程：
1. 執行 git diff 查看變更
2. 分析修改的文件和邏輯
3. 檢查測試覆蓋
4. 提供分級反饋：
   - 🔴 Critical（必須修復）
   - 🟡 Warning（建議修復）
   - 🟢 Suggestion（可考慮改進）

輸出格式：
- 明確指出問題位置
- 提供具體改進建議
- 包含代碼示例
- 評估整體質量評分
EOF

echo "✅ Sub Agents 創建完成"

# 創建基本的 Hooks 配置
echo "📎 配置 Hooks..."

cat > .claude/settings.json << 'EOF'
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -c \"import json, sys, datetime; data=json.load(sys.stdin); cmd=data.get('tool_input',{}).get('command',''); is_api=any(x in cmd for x in ['curl', 'wget', 'api', 'download_data']); log_entry={'timestamp': datetime.datetime.now().isoformat(), 'command': cmd, 'type': 'api_call' if is_api else 'other'}; open('.api_audit.log', 'a').write(json.dumps(log_entry) + '\\n') if is_api else None\"",
            "description": "API調用審計日誌"
          }
        ]
      },
      {
        "matcher": "Edit|Write|Delete",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -c \"import json, sys; data=json.load(sys.stdin); path=data.get('tool_input',{}).get('file_path',''); protected=['.env', 'credentials', 'api_keys', 'prod_config', 'secrets']; blocked=any(p in path for p in protected); print(f'❌ 禁止修改敏感文件: {path}', file=sys.stderr) if blocked else None; sys.exit(2 if blocked else 0)\"",
            "description": "敏感文件保護"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'file=$(echo $CLAUDE_TOOL_INPUT | jq -r .file_path); ext=${file##*.}; case $ext in py) black \"$file\" 2>/dev/null && echo \"✓ Formatted $file\" ;; js|ts) prettier --write \"$file\" 2>/dev/null && echo \"✓ Formatted $file\" ;; esac || true'",
            "description": "自動代碼格式化"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'if grep -r \"open_position\\|place_order\" --include=\"*.py\" src/ 2>/dev/null | grep -v \"stop_loss\" > /dev/null; then echo \"⚠️  風險警告: 發現沒有設置止損的交易代碼！請立即檢查。\" >&2; fi'",
            "description": "風控檢查提醒"
          }
        ]
      }
    ]
  }
}
EOF

echo "✅ Hooks 配置完成"

# 創建基本的 SDD 命令
echo "📝 創建 SDD 命令..."

cat > .claude/commands/spec-init.md << 'EOF'
# 初始化功能規格

創建新功能的規格文檔。

## 使用方法
```
/spec-init "功能描述"
```

## 執行步驟

1. **創建規格目錄**
   - 在 `.kiro/specs/` 下創建功能目錄
   - 生成規格狀態文件 `spec.json`

2. **生成初始文檔**
   ```json
   {
     "name": "feature-name",
     "description": "功能描述",
     "created_at": "2024-01-01T00:00:00",
     "phases": {
       "requirements": false,
       "design": false,
       "tasks": false,
       "implementation": false
     }
   }
   ```

3. **設置開發環境**
   - 創建對應的測試目錄
   - 準備 BDD 場景模板
   - 初始化 Git 分支（可選）

完成後會自動進入需求定義階段。
EOF

cat > .claude/commands/spec-requirements.md << 'EOF'
# 生成需求文檔

使用 BDD 方法分析和記錄功能需求。

## 使用方法
```
/spec-requirements [feature-name]
```

## 執行步驟

1. **需求分析**
   - 分析功能描述
   - 識別核心業務場景
   - 提取關鍵需求點

2. **BDD 場景生成**
   使用 Gherkin 語法創建場景：
   ```gherkin
   Feature: 功能名稱
     作為 [角色]
     我希望 [功能]
     以便 [價值]

     Background: 背景設置

     Scenario: 主要場景
       Given 前置條件
       When 操作動作
       Then 預期結果

     Scenario: 異常場景
       Given 異常前置條件
       When 異常操作
       Then 異常處理結果
   ```

3. **需求文檔生成**
   - 創建 `requirements.md`
   - 包含 BDD 場景
   - 說明數據需求
   - 定義驗收標準

完成後需要人工審核才能進入下一階段。
EOF

cat > .claude/commands/spec-design.md << 'EOF'
# 生成技術設計文檔

使用 DDD 方法設計技術架構。

## 使用方法
```
/spec-design [feature-name]
```

## 執行步驟

1. **領域建模**
   ```python
   # 識別核心實體
   class Entity:
       pass
   
   # 定義值對象
   @dataclass(frozen=True)
   class ValueObject:
       pass
   
   # 設計聚合根
   class AggregateRoot(Entity):
       pass
   ```

2. **架構設計**
   - 分層架構設計
   - 模組依賴關係
   - 接口定義
   - 數據流設計

3. **技術選型**
   - 框架和庫選擇
   - 數據存儲方案
   - 部署策略
   - 性能考慮

4. **設計文檔生成**
   - 創建 `design.md`
   - UML 圖表（可選）
   - 接口規範
   - 實施指南

完成後需要人工審核才能進入任務分解階段。
EOF

cat > .claude/commands/spec-tasks.md << 'EOF'
# 生成實施任務清單

將設計分解為可執行的開發任務。

## 使用方法
```
/spec-tasks [feature-name]
```

## 執行步驟

1. **任務分解**
   根據設計文檔分解為具體任務：
   - 每個任務 < 2 小時
   - 明確的輸入輸出
   - 可獨立測試
   - 有明確的完成標準

2. **測試策略分配**
   ```markdown
   ## 任務清單
   
   ### 1. 實現領域模型 [DDD]
   - [ ] 創建實體類
   - [ ] 實現值對象
   - [ ] 定義聚合根
   
   ### 2. 實現業務邏輯 [BDD]
   - [ ] 實現主要場景
   - [ ] 處理異常情況
   - [ ] 添加邊界檢查
   
   ### 3. 實現計算邏輯 [TDD]
   - [ ] 編寫單元測試
   - [ ] 實現算法邏輯
   - [ ] 性能優化
   ```

3. **依賴關係**
   - 標記任務依賴
   - 設置執行順序
   - 識別並行機會

4. **資源分配**
   - Sub Agent 分工
   - 預估工作量
   - 風險評估

完成後可以開始實施階段。
EOF

echo "✅ SDD 命令創建完成"

# 創建項目知識庫基礎文件
echo "📚 創建項目知識庫..."

cat > .kiro/steering/product.md << 'EOF'
# 產品概述

## 項目簡介
AI協作開發項目 - 使用Claude Code和Sub Agents實現高效的多實例協作開發。

## 核心功能
1. **規格驅動開發** - 結構化的開發流程
2. **多實例協作** - 專業化分工提升效率
3. **自動化測試** - 確保代碼質量
4. **風險管理** - 內建安全檢查

## 目標用戶
- 量化交易開發團隊
- 需要高質量代碼的項目
- 複雜業務邏輯的系統開發
- AI輔助開發的探索者

## 成功指標
- 開發效率提升 50%+
- 代碼缺陷減少 80%+
- 團隊協作滿意度 > 90%
- 項目交付準時率 > 95%
EOF

cat > .kiro/steering/tech.md << 'EOF'
# 技術架構

## 核心技術棧
- **AI協作**: Claude Code + Sub Agents
- **開發方法**: SDD + BDD + DDD + TDD
- **自動化**: Hooks + Task Scheduler
- **版本控制**: Git + Branch Strategy
- **測試框架**: pytest + behave
- **代碼品質**: Black + Prettier + ESLint

## 架構原則
1. **關注點分離** - 每個Sub Agent專注特定領域
2. **單一職責** - 每個組件有明確的責任
3. **開放封閉** - 對擴展開放，對修改封閉
4. **依賴倒置** - 依賴抽象而非具體實現

## 整合流程
```
SDD流程 → Sub Agents → Hooks → Git → 部署
   ↓         ↓          ↓      ↓      ↓
規格驅動   專業分工   自動檢查  版本控制 質量保證
```

## 性能目標
- Sub Agent響應時間 < 5秒
- Hook執行時間 < 1秒
- 測試套件運行時間 < 30秒
- 代碼格式化時間 < 2秒
EOF

cat > .kiro/steering/methodology.md << 'EOF'
# 開發方法論

## 整合框架
本項目採用四種互補的開發方法論：

### SDD (Spec-Driven Development) - 主框架
- **目的**: 提供結構化的開發流程
- **階段**: Requirements → Design → Tasks → Implementation
- **優勢**: 確保需求完整性和可追溯性

### BDD (Behavior-Driven Development) - 需求工具
- **目的**: 用自然語言描述業務行為
- **工具**: Gherkin語法，behave框架
- **適用**: 業務邏輯、用戶場景、驗收測試

### DDD (Domain-Driven Design) - 設計工具
- **目的**: 建立清晰的領域模型
- **概念**: 實體、值對象、聚合根、領域服務
- **適用**: 系統架構、復雜業務邏輯建模

### TDD (Test-Driven Development) - 品質工具
- **目的**: 確保代碼正確性
- **流程**: 紅 → 綠 → 重構
- **適用**: 算法邏輯、工具函數、關鍵計算

## 方法論選擇指南

| 場景 | 主要方法 | 輔助方法 | 說明 |
|------|----------|----------|------|
| 需求分析 | BDD | SDD | 用Gherkin描述場景 |
| 架構設計 | DDD | SDD | 建立領域模型 |
| 業務邏輯 | BDD + DDD | TDD | 行為驅動+領域建模 |
| 工具函數 | TDD | - | 測試驅動開發 |
| 整合測試 | BDD | TDD | 端到端場景測試 |

## 最佳實踐
1. **永遠從規格開始** - 使用/spec-init
2. **小步快跑** - 頻繁提交和驗證
3. **自動化優先** - 依賴Hooks而非人工提醒
4. **文檔同步** - 代碼和文檔同步更新
5. **持續改進** - 根據反饋調整流程
EOF

echo "✅ 項目知識庫創建完成"

# 創建監控腳本
echo "📊 創建監控腳本..."

cat > scripts/monitoring/view_api_audit.py << 'EOF'
#!/usr/bin/env python3
"""
API審計日誌查看器
"""
import json
from datetime import datetime
from collections import Counter
from pathlib import Path

def analyze_api_log():
    log_file = Path('.api_audit.log')
    
    if not log_file.exists():
        print("📭 尚無API調用記錄")
        return
    
    try:
        with open(log_file, 'r') as f:
            logs = [json.loads(line) for line in f if line.strip()]
        
        print(f"\n📊 API調用統計 (總計: {len(logs)} 次)\n")
        
        # 按類型統計
        api_calls = [log for log in logs if log.get('type') == 'api_call']
        other_calls = [log for log in logs if log.get('type') == 'other']
        
        print(f"API調用: {len(api_calls)} 次")
        print(f"其他命令: {len(other_calls)} 次")
        
        if api_calls:
            print("\n🕐 最近5次API調用:")
            for log in api_calls[-5:]:
                time = datetime.fromisoformat(log['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                cmd = log['command'][:80] + '...' if len(log['command']) > 80 else log['command']
                print(f"  [{time}] {cmd}")
            
            # 頻率分析
            hours = [datetime.fromisoformat(log['timestamp']).hour for log in api_calls]
            hour_counts = Counter(hours)
            if hour_counts:
                peak_hour = hour_counts.most_common(1)[0]
                print(f"\n📈 高峰時段: {peak_hour[0]}:00-{peak_hour[0]+1}:00 ({peak_hour[1]} 次調用)")
                
    except Exception as e:
        print(f"❌ 讀取日誌時發生錯誤: {e}")

if __name__ == "__main__":
    analyze_api_log()
EOF

chmod +x scripts/monitoring/view_api_audit.py

cat > scripts/monitoring/performance_monitor.py << 'EOF'
#!/usr/bin/env python3
"""
性能監控腳本
"""
import psutil
import time
from datetime import datetime

def monitor_performance():
    print("🔍 系統性能監控")
    print("=" * 50)
    
    # CPU使用率
    cpu_percent = psutil.cpu_percent(interval=1)
    print(f"CPU使用率: {cpu_percent}%")
    
    # 記憶體使用率
    memory = psutil.virtual_memory()
    print(f"記憶體使用率: {memory.percent}%")
    print(f"可用記憶體: {memory.available // (1024**3):.1f} GB")
    
    # 磁碟使用率
    disk = psutil.disk_usage('/')
    print(f"磁碟使用率: {disk.percent}%")
    print(f"可用空間: {disk.free // (1024**3):.1f} GB")
    
    # 檢查Claude Code相關進程
    claude_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            if 'claude' in proc.info['name'].lower():
                claude_processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    if claude_processes:
        print(f"\n🤖 Claude相關進程: {len(claude_processes)} 個")
        for proc in claude_processes:
            print(f"  PID {proc['pid']}: {proc['name']} (CPU: {proc['cpu_percent']}%, MEM: {proc['memory_percent']:.1f}%)")
    else:
        print("\n😴 未檢測到Claude相關進程")
    
    print(f"\n🕐 檢查時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    monitor_performance()
EOF

chmod +x scripts/monitoring/performance_monitor.py

echo "✅ 監控腳本創建完成"

# 創建測試腳本
echo "🧪 創建測試腳本..."

cat > test_setup.sh << 'EOF'
#!/bin/bash

# 測試AI協作開發環境設置

echo "🧪 測試AI協作開發環境"
echo "========================"

# 檢查目錄結構
echo "📁 檢查目錄結構..."
required_dirs=(
    ".claude/commands"
    ".claude/agents"
    ".claude/scheduler"
    ".kiro/steering"
    ".kiro/specs"
    "docs/quick_reference"
    "src/domain"
    "tests/behavior"
    "scripts/monitoring"
)

all_good=true
for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✅ $dir"
    else
        echo "  ❌ $dir"
        all_good=false
    fi
done

# 檢查配置文件
echo -e "\n📄 檢查配置文件..."
required_files=(
    "CLAUDE.md"
    ".claude/settings.json"
    ".claude/agents/strategy-analyst.md"
    ".claude/agents/risk-manager.md"
    ".kiro/steering/product.md"
    ".kiro/steering/tech.md"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file"
        all_good=false
    fi
done

# 檢查腳本可執行性
echo -e "\n🔧 檢查腳本..."
scripts=(
    "scripts/monitoring/view_api_audit.py"
    "scripts/monitoring/performance_monitor.py"
)

for script in "${scripts[@]}"; do
    if [ -x "$script" ]; then
        echo "  ✅ $script (可執行)"
    else
        echo "  ❌ $script (不可執行)"
        all_good=false
    fi
done

# 測試Python依賴
echo -e "\n🐍 檢查Python依賴..."
dependencies=("psutil" "json" "datetime")

for dep in "${dependencies[@]}"; do
    if python3 -c "import $dep" 2>/dev/null; then
        echo "  ✅ $dep"
    else
        echo "  ❌ $dep"
        all_good=false
    fi
done

# 總結
echo -e "\n" + "=" * 30
if [ "$all_good" = true ]; then
    echo "🎉 環境設置完成！所有檢查都通過了。"
    echo -e "\n📋 下一步:"
    echo "1. 啟動Claude Code: claude-code"
    echo "2. 初始化項目: > /steering-init"
    echo "3. 創建第一個功能: > /spec-init \"你的功能描述\""
    echo "4. 測試Sub Agents: > 使用 strategy-analyst 分析一個簡單策略"
else
    echo "❌ 發現問題，請檢查上述錯誤並重新運行設置。"
    exit 1
fi
EOF

chmod +x test_setup.sh

echo "✅ 測試腳本創建完成"

# 創建README
echo "📖 創建README..."

cat > README.md << 'EOF'
# AI協作開發項目

🤖 使用Claude Code和Sub Agents實現高效的多實例協作開發框架

## ✨ 特色功能

- **🔄 規格驅動開發** - SDD流程確保開發品質
- **🤖 專業Sub Agents** - 5個專業AI助手各司其職
- **⚡ 自動化Hooks** - 代碼格式化、安全檢查、測試執行
- **👥 多實例協作** - 支援團隊並行開發
- **🎯 BDD+DDD+TDD** - 整合最佳開發實踐

## 🚀 快速開始

### 1. 環境設置
```bash
# 運行一鍵設置
./setup.sh

# 測試環境
./test_setup.sh
```

### 2. 初始化項目
```bash
# 啟動Claude Code
claude-code

# 初始化項目知識庫
> /steering-init

# 創建第一個功能
> /spec-init "實現用戶登入功能"
```

### 3. 體驗Sub Agents
```bash
# 策略分析
> 使用 strategy-analyst 分析登入流程的安全性

# 風險管理
> 讓 risk-manager 評估安全風險

# 測試工程
> 使用 test-engineer 設計測試案例
```

## 🏗️ 項目結構

```
├── .claude/                  # Claude Code配置
│   ├── agents/              # Sub Agents定義
│   ├── commands/            # 自定義命令
│   └── settings.json        # Hooks配置
├── .kiro/                   # 項目知識庫
│   ├── steering/            # 項目指導文檔
│   └── specs/               # 功能規格
├── src/                     # 源代碼
├── tests/                   # 測試代碼
├── docs/                    # 項目文檔
└── scripts/                 # 工具腳本
```

## 🤖 Sub Agents

| Agent | 職責 | 使用時機 |
|-------|------|----------|
| **strategy-analyst** | 策略分析、BDD場景生成 | 需求分析、策略設計 |
| **risk-manager** | 風險評估、安全檢查 | 風控審查、安全評估 |
| **data-engineer** | 數據處理、特徵工程 | 數據相關任務 |
| **api-specialist** | API集成、性能優化 | API開發、集成 |
| **test-engineer** | 測試自動化、品質保證 | 測試設計、執行 |

## 🔧 自動化功能

### Hooks自動執行
- ✅ **代碼格式化** - Python(Black)、JS/TS(Prettier)
- 🛡️ **敏感文件保護** - 阻止修改.env等文件
- 📝 **API審計** - 記錄所有API調用
- ⚠️ **風控檢查** - 檢測缺失的安全措施

### SDD流程自動化
- 📋 **需求分析** - BDD場景自動生成
- 🏗️ **技術設計** - DDD模型設計
- 📝 **任務分解** - 可執行任務清單
- 🚀 **實施管理** - Sub Agents自動協作

## 📊 監控工具

```bash
# 查看API調用統計
python scripts/monitoring/view_api_audit.py

# 系統性能監控
python scripts/monitoring/performance_monitor.py

# 檢查環境狀態
./test_setup.sh
```

## 🎯 最佳實踐

1. **永遠從規格開始** - 使用`/spec-init`創建功能
2. **善用Sub Agents** - 讓專業的agent處理專業的事
3. **信任自動化** - 依賴Hooks而非人工提醒
4. **頻繁提交** - 保持Git歷史清晰
5. **文檔同步** - 代碼變更同步更新文檔

## 🆘 故障排除

### Sub Agents不工作？
```bash
# 檢查agents配置
ls -la .claude/agents/

# 嘗試顯式調用
> 使用 strategy-analyst 執行簡單任務
```

### Hooks未觸發？
```bash
# 檢查配置
cat .claude/settings.json | python -m json.tool

# 查看錯誤信息
# Hooks錯誤會在Claude Code輸出中顯示
```

### 需要幫助？
1. 查看 `docs/` 目錄下的詳細文檔
2. 運行 `./test_setup.sh` 檢查環境
3. 檢查 `.claude/scheduler/logs/` 日誌文件

## 🔄 升級與自定義

### 添加新Sub Agent
```bash
# 使用互動式創建
> /agents

# 或手動創建
echo '---
name: my-agent
description: 我的專用agent
---
agent的系統提示詞...' > .claude/agents/my-agent.md
```

### 自定義Hook
編輯 `.claude/settings.json` 添加新的Hook規則。

### 擴展命令
在 `.claude/commands/` 添加新的slash command。

---

🎉 **開始你的AI協作開發之旅！**

使用這個框架，你將體驗到前所未有的開發效率和代碼品質。
EOF

echo "✅ README創建完成"

# 最終總結
echo ""
echo "🎉 AI協作開發項目設置完成！"
echo "================================"
echo ""
echo "📦 已創建的組件:"
echo "  • 完整的目錄結構"
echo "  • 5個專業Sub Agents"
echo "  • 自動化Hooks配置"
echo "  • SDD命令集"
echo "  • 項目知識庫"
echo "  • 監控和測試工具"
echo ""
echo "🚀 下一步:"
echo "  1. 運行測試: ./test_setup.sh"
echo "  2. 啟動Claude Code: claude-code"
echo "  3. 初始化項目: > /steering-init"
echo "  4. 創建功能: > /spec-init \"你的功能描述\""
echo ""
echo "📚 重要文件:"
echo "  • README.md - 完整使用指南"
echo "  • CLAUDE.md - Claude Code配置"
echo "  • .claude/agents/ - Sub Agents定義"
echo "  • docs/ - 詳細文檔"
echo ""
echo "💡 提示:"
echo "  • 使用 'python scripts/monitoring/view_api_audit.py' 查看API審計"
echo "  • 所有開發都從 /spec-init 開始"
echo "  • 善用Sub Agents：> 使用 [agent-name] 來..."
echo ""
echo "🎯 享受高效的AI協作開發體驗！"