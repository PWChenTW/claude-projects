# 初始化功能規格

## 🚨 重要：遵循 CLAUDE.md 核心開發原則

初始化功能時必須遵循：
- **MVP First**：從最簡單的版本開始
- **漸進式開發**：一次只加一個小功能
- **批判性思考**：質疑需求的必要性
- **實用主義**：避免過度設計

初始化一個新的功能規格，創建SDD(規格驅動開發)流程的起始點。

## 用法
`/spec-init [功能名稱] [簡短描述]`

## 功能說明

這個命令會自動：

1. **創建規格目錄結構**
   ```
   .kiro/specs/[feature-name]/
   ├── spec.json          # 規格狀態追蹤
   ├── requirements.md    # BDD需求文檔（待生成）
   ├── design.md         # DDD設計文檔（待生成）
   ├── tasks.md          # 任務清單（待生成）
   ├── exploration.md    # EPE探索報告（自動生成）
   ├── implementation-plan.md # EPE實施計畫（自動生成）
   └── verification-report.md # 驗證報告（待生成）
   ```

2. **設置規格狀態**
   - 狀態：`exploration` (進入探索階段)
   - 創建時間戳
   - 功能基本信息

3. **自動觸發 EPE 工作流程**
   - **探索階段** (20-30分鐘)：使用 `/explore` 深度理解需求
   - **計畫階段** (10-15分鐘)：使用 `/plan` 制定實施策略
   - **執行階段**：基於計畫逐步實施
   - **驗證階段**：使用 `/verify` 確保品質

4. **整合 SDD 流程**
   - EPE 探索完成後自動進入 requirements 階段
   - 保持原有的 SDD 品質控制流程
   - 文檔自動串聯，減少重複工作

## 示例

```bash
> /spec-init user-auth "實現用戶認證和授權系統"
```

這將自動：
1. 創建目錄：`.kiro/specs/user-auth/`
2. 啟動 EPE 探索階段（20-30分鐘深度分析）
3. 生成探索報告和實施計畫
4. 進入 SDD requirements 階段
5. 下一步：審核探索結果，使用 `/spec-requirements user-auth` 細化需求

## 規格狀態流程

### EPE + SDD 整合流程
```
init → [EPE: explore → plan] → requirements → design → tasks → [EPE: execute → verify] → completed
```

### 階段說明
1. **Exploration** (EPE): 深度探索和理解需求
2. **Planning** (EPE): 制定詳細實施計畫
3. **Requirements** (SDD): BDD場景和需求文檔
4. **Design** (SDD): DDD設計和架構
5. **Tasks** (SDD): 任務分解和指派
6. **Execution** (EPE): 紀律執行實施
7. **Verification** (EPE): 多層驗證確保品質

每個階段都需要人工審核確認才能進入下一階段，確保品質和正確性。

## 模板變量

創建規格時可以使用以下變量：
- `{feature_name}`: 功能名稱
- `{description}`: 功能描述
- `{timestamp}`: 創建時間
- `{author}`: 創建者（如果可獲得）

## 注意事項

1. **命名規範**：功能名稱使用小寫字母和連字符
2. **唯一性檢查**：避免重複的功能名稱
3. **描述清晰**：提供清楚的功能描述有助於後續分析
4. **階段順序**：必須按照SDD流程順序進行