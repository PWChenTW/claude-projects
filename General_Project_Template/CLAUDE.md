# Claude Code 通用專案配置

## 核心開發原則

### 漸進式開發 (Progressive Development)
- **Start Small**: 從最簡單的可運行版本開始
- **Iterate Fast**: 快速迭代，每次只增加一個小功能
- **Fail Early**: 儘早發現問題，避免累積技術債
- **MVP First**: 先做出最小可行產品，再逐步優化

### 批判性思考 (Critical Thinking)
- **質疑需求**: 主動評估用戶需求的合理性和優先級
- **挑戰假設**: 不盲目接受，要驗證假設是否成立
- **提供替代方案**: 當發現更好的解決方案時，主動提出
- **誠實反饋**: 如果某個想法有問題，直接指出並解釋原因

### 實用主義 (Pragmatism)
- **避免過度設計**: 不要一開始就建立複雜架構
- **YAGNI原則**: You Aren't Gonna Need It - 只實現當前需要的功能
- **簡單優先**: 能用簡單方案解決的，不用複雜方案
- **可用性優先**: 先確保基本功能正常運作，再考慮優化

詳見 `docs/guides/mvp-development.md` 了解 MVP 開發最佳實踐。

## 項目概述
這是一個集成了多實例協作、規格驅動開發(SDD)、和專業Sub Agents的通用AI協作開發模板。

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
- **目標**: 確保核心邏輯的正確性
- **應用**: implementation階段，特別是複雜算法
- **觸發**: test-engineer 自動介入

## Sub Agents 調用指導

### 🔴 重要：調用 Sub Agent 時的必要提醒

在調用任何 Sub Agent 執行任務時，**必須**在 prompt 中包含以下指示：

```
【重要】開始任務前，請先閱讀並理解 .claude/agents/_core_principles.md 文件中的核心開發原則。

【具體任務】
[任務描述]

【預期產出】
請基於核心開發原則（MVP優先、漸進式開發、批判性思考、實用主義），提供最簡單可行的解決方案。
如果需求過於複雜，請先提出簡化建議。
```

如果 Sub Agent 無法訪問文件，則使用以下備用 prompt：

```
【核心開發原則摘要】
1. MVP 優先 - 從最簡單的解決方案開始
2. 漸進式開發 - 快速迭代，每次只加一個小功能  
3. 批判性思考 - 質疑需求，提供更好的替代方案
4. 實用主義 - YAGNI原則，避免過度設計

【具體任務】
[任務描述]
```

這確保所有 Sub Agents 都遵循相同的開發理念。

## Sub Agents 自動觸發規則

### general-assistant (通用助手)
**觸發詞**: 一般問題、簡單任務、不確定、哪個agent、幫助、解釋
**專業領域**: 
- 一般問答
- 簡單任務處理
- 跨領域協調
- 初步需求分類

### business-analyst (業務分析師)
**觸發詞**: 需求、分析、業務邏輯、BDD、場景、用戶故事、功能
**專業領域**: 
- 業務需求分析
- BDD場景生成
- 用戶體驗設計
- 功能規劃

### architect (系統架構師)
**觸發詞**: 架構、設計、系統、模組、組件、DDD、模式、框架
**專業領域**:
- 系統架構設計
- DDD領域建模
- 技術選型
- 模式設計

### data-specialist (數據專家)
**觸發詞**: 數據、算法、計算、處理、演算法、優化、效能
**專業領域**:
- 數據結構設計
- 算法實現
- 性能優化
- 計算邏輯

### integration-specialist (集成專家)
**觸發詞**: API、接口、集成、外部、服務、網路、通訊
**專業領域**:
- API設計與集成
- 外部服務整合
- 網路通訊
- 系統間集成

### test-engineer (測試工程師)
**觸發詞**: 測試、單元測試、整合測試、品質、覆蓋率、重構
**專業領域**:
- 測試策略設計
- 自動化測試
- 代碼品質檢查
- 重構支援

### tech-lead (技術主管)
**觸發詞**: 技術決策、代碼審查、團隊、技術債、重構、標準、最佳實踐
**專業領域**:
- 技術領導與決策
- 代碼品質管理
- 團隊協調
- 技術債管理

### context-manager (上下文管理專家)
**觸發詞**: 文檔、知識、上下文、記錄、歷史、決策、更新、維護
**專業領域**:
- 知識管理
- 文檔維護
- 信息同步
- 項目記憶

## 觸發詞自動查閱機制

當對話中出現以下關鍵詞時，自動查閱對應的快速參考文檔：

### 技術相關
- `API設計`、`RESTful` → 查閱 `docs/quick_reference/api_design.md`
- `數據結構`、`algorithm` → 查閱 `docs/quick_reference/data_structures.md`
- `設計模式`、`pattern` → 查閱 `docs/quick_reference/design_patterns.md`
- `性能優化`、`performance` → 查閱 `docs/quick_reference/performance.md`

### 開發流程
- `BDD場景`、`Gherkin` → 查閱 `docs/examples/bdd_scenarios.md`
- `多實例協作` → 查閱 `docs/collaboration/multi_instance.md`
- `角色分配` → 查閱 `docs/collaboration/role_assignment.md`
- `工作流程` → 查閱 `docs/collaboration/workflow.md`

### 錯誤處理
- `錯誤處理`、`error` → 查閱 `docs/quick_reference/error_handling.md`
- `檢查清單` → 查閱 `docs/checklists/`
- `故障排除` → 查閱 `docs/troubleshooting/`

## 自動化檢查規則

### 代碼品質檢查
每次代碼修改後，自動執行：
1. Python: Black格式化 + flake8檢查
2. JavaScript/TypeScript: Prettier格式化 + ESLint檢查
3. 單元測試執行（如果存在）
4. 類型檢查（如果適用）

### 安全檢查
每次完成開發後，自動檢查：
1. 是否有硬編碼的敏感信息
2. 錯誤處理是否完善
3. 輸入驗證是否充分
4. 安全最佳實踐遵循

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
- `business_rules.md`: 業務規則和約束
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
1. **產品實例**: 負責需求分析和產品設計
2. **架構實例**: 專注系統架構和技術設計
3. **開發實例**: 負責核心功能實現
4. **測試實例**: 負責測試設計和品質保證
5. **集成實例**: 負責系統集成和部署

### 分支策略
- `main`: 穩定版本
- `feature/[feature-name]`: 功能開發分支
- `role/[role-name]`: 角色專用分支
- `integration`: 整合測試分支

### 並行開發
- **Git Worktree**: 用於完全獨立的任務並行開發
- **多實例協作**: 用於需要協調的角色分工
- 詳見 `docs/guides/parallel-workflow.md`

### 同步機制
1. 每日同步會議（虛擬）
2. 重要節點的進度檢查
3. Git分支定期合併
4. 衝突解決和協調

## 品質保證標準

### 代碼標準
1. 所有函數必須有docstring
2. 核心邏輯必須有單元測試
3. API調用必須有錯誤處理
4. 敏感信息不得硬編碼

### 業務邏輯標準
1. 複雜算法必須有詳細註解
2. 關鍵決策必須有文檔說明
3. 用戶輸入必須有驗證
4. 異常情況必須有處理機制

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