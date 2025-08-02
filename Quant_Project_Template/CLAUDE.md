# Claude Code 專案配置

## 核心開發原則

### 漸進式開發 (Progressive Development)
- **Start Small**: 從最簡單的策略開始，先確保基本邏輯正確
- **Iterate Fast**: 快速迭代，每次只增加一個指標或規則
- **Backtest Early**: 儘早回測，避免累積錯誤
- **MVP First**: 先做出最小可行策略，再逐步優化

### 批判性思考 (Critical Thinking)
- **質疑策略**: 主動評估策略邏輯的合理性
- **挑戰假設**: 不盲目相信歷史數據，要驗證假設
- **風險評估**: 始終將風險管理放在首位
- **誠實反饋**: 如果策略有明顯缺陷，直接指出

### 實用主義 (Pragmatism)
- **避免過度優化**: 不要過度擬合歷史數據
- **KISS原則**: Keep It Simple, Stupid - 簡單策略往往更穩定
- **穩定優先**: 先確保策略穩定運行，再考慮收益優化
- **風控優先**: 寧可錯過機會，不可承擔過大風險

詳見 `docs/guides/mvp-development.md` 了解策略 MVP 開發最佳實踐。

## 項目概述
這是一個集成了多實例協作、規格驅動開發(SDD)、和專業Sub Agents的AI協作開發模板。

## AI Assistant Guidelines

### Task Delegation Principle
- **Complex or specialized tasks**: Always delegate to appropriate Sub Agents
- **Simple queries**: Can be handled directly for efficiency
- **When in doubt**: Prefer delegation to ensure quality

### General Purpose Agent
For queries that don't fit specialized agents, use:
- `general-assistant`: General Q&A, simple tasks, cross-domain coordination

## 開發方法論整合

### 規格驅動開發 (SDD) - 主框架
- **目標**: 結構化的開發流程管理  
- **階段**: requirements → design → tasks → implementation
- **觸發**: 使用 `/spec-init [功能名稱]` 開始

### 行為驅動開發 (BDD) - 需求工具
- **目標**: 描述業務行為和使用者需求
- **應用**: requirements階段生成Gherkin場景
- **檔案**: `.kiro/specs/[feature]/requirements.md`

### 領域驅動設計 (DDD) - 設計工具  
- **目標**: 建立清晰的領域模型
- **應用**: design階段建立實體和聚合
- **檔案**: `.kiro/specs/[feature]/design.md`

### 測試驅動開發 (TDD) - 品質工具
- **目標**: 確保關鍵計算邏輯的正確性
- **應用**: implementation階段，特別是金融計算
- **觸發**: test-engineer 自動介入

## Sub Agents 調用指導

### 🔴 重要：調用 Sub Agent 時的必要提醒

在調用任何 Sub Agent 執行任務時，**必須**在 prompt 中包含以下指示：

```
【重要】開始任務前，請先閱讀並理解 .claude/agents/_core_principles.md 文件中的核心開發原則。

【具體任務】
[任務描述]

【預期產出】
請基於核心開發原則（MVP優先、漸進式開發、批判性思考、實用主義），提供最簡單可行的策略方案。
特別注意：從單一指標開始、固定參數、簡單風控、避免過度優化。
```

如果 Sub Agent 無法訪問文件，則使用以下備用 prompt：

```
【核心開發原則摘要】
1. 策略 MVP - 從最簡單的策略開始，單一信號即可
2. 漸進式開發 - 先驗證核心邏輯，再優化細節
3. 批判性思考 - 質疑策略假設，避免過度擬合
4. 風控優先 - 簡單策略往往更穩健，永遠設置止損

【具體任務】
[任務描述]
```

這確保所有 Sub Agents 都遵循相同的開發理念。

## Sub Agents 自動觸發規則

### general-assistant (通用助手)
**觸發詞**: 一般問題、簡單任務、不確定、哪個agent、幫助、解釋、什麼是
**專業領域**: 
- 一般問答
- 簡單任務處理
- 跨領域協調
- 初步需求分類
- 基礎交易術語解釋

### strategy-analyst (策略分析師)
**觸發詞**: 策略、分析、需求、BDD、場景、評估、可行性
**專業領域**: 
- 策略需求分析
- BDD場景生成
- 策略風險評估
- 業務邏輯驗證

### risk-manager (風控專家)
**觸發詞**: 風險、風控、倉位、止損、風險管理、回撤、爆倉
**專業領域**:
- 風險規則制定
- 倉位計算
- 資金管理
- 安全檢查

### data-engineer (數據工程師)
**觸發詞**: 數據、清洗、特徵、指標、數據源、ETL、數據品質
**專業領域**:
- 數據獲取和清洗
- 技術指標計算
- 特徵工程
- 數據管道設計

### api-specialist (API專家)
**觸發詞**: API、接口、調用、限流、性能、集成、錯誤處理
**專業領域**:
- API集成設計
- 性能優化
- 錯誤處理
- 限流管理

### test-engineer (測試工程師)
**觸發詞**: 測試、單元測試、整合測試、品質、覆蓋率、重構
**專業領域**:
- 測試策略設計
- 自動化測試
- 代碼品質檢查
- 重構支援

### tech-lead (量化技術主管)
**觸發詞**: 技術決策、性能優化、系統穩定、團隊、監控、架構升級
**專業領域**:
- 交易系統技術領導
- 性能優化
- 系統穩定性
- 團隊協調

### context-manager (量化上下文管理專家)
**觸發詞**: 文檔、策略記錄、市場事件、交易日誌、研究報告、知識管理
**專業領域**:
- 策略知識管理
- 市場情報整理
- 交易記錄維護
- 研究文檔管理

### data-scientist (數據科學家)
**觸發詞**: 機器學習、統計、模型、預測、特徵選擇、因子、ML、AI
**專業領域**:
- 機器學習建模
- 統計分析
- 預測模型
- 量化研究

### hft-researcher (高頻交易研究員)
**觸發詞**: 高頻、HFT、微觀結構、延遲、訂單簿、執行、毫秒、微秒
**專業領域**:
- 市場微觀結構分析
- 延遲優化
- 訂單執行研究
- 高頻策略開發

### quant-analyst (量化分析師)
**觸發詞**: 量化、金融模型、衍生品、期權、組合優化、風險建模、定價
**專業領域**:
- 金融建模
- 衍生品定價
- 投資組合優化
- 量化研究方法

## 觸發詞自動查閱機制

當對話中出現以下關鍵詞時，自動查閱對應的快速參考文檔：

### 量化交易相關
- `RSI`、`MACD`、`布林帶` → 查閱 `docs/quick_reference/technical_indicators.md`
- `回測`、`回測結果` → 查閱 `docs/quick_reference/backtesting.md`
- `倉位管理`、`風控` → 查閱 `docs/quick_reference/risk_management.md`
- `交易信號`、`進出場` → 查閱 `docs/quick_reference/signal_generation.md`

### API與數據
- `API調用`、`接口` → 查閱 `docs/quick_reference/api_endpoints.md`
- `數據結構`、`schema` → 查閱 `docs/quick_reference/data_schema.md`
- `時區`、`timezone` → 查閱 `docs/quick_reference/timezone_handling.md`
- `結算`、`settlement` → 查閱 `docs/quick_reference/settlement_rules.md`

### 開發流程
- `BDD場景`、`Gherkin` → 查閱 `docs/examples/bdd_scenarios.md`
- `多實例協作` → 查閱 `docs/collaboration/multi_instance.md`
- `角色分配` → 查閱 `docs/collaboration/role_assignment.md`
- `工作流程` → 查閱 `docs/collaboration/workflow.md`

### 錯誤處理
- `錯誤代碼`、`error` → 查閱 `docs/quick_reference/error_codes.md`
- `檢查清單` → 查閱 `docs/checklists/`
- `故障排除` → 查閱 `docs/troubleshooting/`

## 自動化檢查規則

### 風控自動檢查
每次完成開發後，自動檢查：
1. 交易邏輯是否包含停損機制
2. 倉位計算是否有上限
3. 風險參數是否合理
4. 是否有異常處理

### 代碼品質檢查
每次代碼修改後，自動執行：
1. Python: Black格式化 + flake8檢查
2. JavaScript/TypeScript: Prettier格式化 + ESLint檢查
3. 單元測試執行（如果存在）
4. 類型檢查（如果適用）

### API調用審計
記錄所有API調用：
1. 時間戳記
2. 調用端點
3. 參數內容（敏感信息遮蔽）
4. 響應時間
5. 狀態碼

## 專案知識庫結構

### .kiro/steering/ - 核心知識
- `product.md`: 產品概述和目標
- `tech.md`: 技術棧和架構決策
- `structure.md`: 專案結構說明
- `methodology.md`: 開發方法論詳細說明
- `trading_rules.md`: 量化交易特定規則
- `collaboration.md`: 多實例協作規範

### .kiro/specs/ - 功能規格
每個功能都有獨立目錄：
```
feature-name/
├── spec.json          # 規格狀態和基本信息
├── requirements.md     # BDD需求文檔
├── design.md          # DDD設計文檔
└── tasks.md           # 具體任務清單
```

## 多實例協作工作流

### 角色分配範例
1. **架構師實例**: 負責技術架構和整體設計
2. **策略實例**: 專注策略邏輯和算法實現
3. **風控實例**: 負責風險管理和合規檢查
4. **測試實例**: 負責測試設計和品質保證
5. **數據實例**: 負責數據處理和特徵工程

### 分支策略
- `main`: 穩定版本
- `feature/[feature-name]`: 功能開發分支
- `strategy/[strategy-name]`: 策略專用分支
- `role/[role-name]`: 角色專用分支
- `integration`: 整合測試分支

### 並行開發
- **Git Worktree**: 用於獨立策略或模組的並行開發
- **多實例協作**: 用於策略、風控、數據的協同開發
- 詳見 `docs/guides/parallel-workflow.md`

### 同步機制
1. 每日同步會議（虛擬）
2. 重要節點的進度檢查
3. Git分支定期合併
4. 衝突解決和協調

## 品質保證標準

### 代碼標準
1. 所有函數必須有docstring
2. 關鍵邏輯必須有單元測試
3. API調用必須有錯誤處理
4. 敏感信息不得硬編碼

### 交易邏輯標準
1. 每個策略必須有停損機制
2. 倉位計算必須有上限檢查
3. 所有信號必須有信心度評分
4. 風控規則必須可配置

### 文檔標準
1. 每個功能必須有BDD場景描述
2. 重要設計決策必須文檔化
3. API變更必須更新文檔
4. 例外情況必須說明處理方式

## 性能與監控

### 監控指標
1. Sub Agent響應時間
2. API調用頻率和響應時間
3. 測試執行時間
4. 內存和CPU使用率

### 日誌管理
1. 結構化日誌格式
2. 自動日誌輪轉
3. 敏感信息自動遮蔽
4. 錯誤日誌即時警報

### 性能優化
1. Sub Agent並行執行
2. API調用批次處理
3. 緩存常用計算結果
4. 定期清理臨時文件