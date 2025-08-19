# 初始化功能規格 (SDD + EPE 整合版)

## 🚨 重要：遵循 CLAUDE.md 核心開發原則

初始化功能時必須遵循：
- **MVP First**：從最簡單的版本開始
- **漸進式開發**：一次只加一個小功能
- **批判性思考**：質疑需求的必要性
- **實用主義**：避免過度設計
- **Context First**：充分探索後再計畫和實施

初始化一個新的功能規格，整合 SDD(規格驅動開發) 和 EPE(探索-計畫-執行) 工作流程。

## 用法
`/spec-init [功能名稱] [簡短描述]`

## 功能說明

這個命令會自動：

1. **創建增強版規格目錄結構**
   ```
   .kiro/specs/[feature-name]/
   ├── spec.json          # 規格狀態追蹤
   ├── exploration.md     # EPE探索報告（新增）
   ├── plan.md           # EPE計畫文檔（新增）
   ├── requirements.md    # BDD需求文檔
   ├── design.md         # DDD設計文檔
   ├── tasks.md          # 任務清單
   └── verification.md   # 驗證報告（新增）
   ```

2. **設置規格狀態**
   - 初始狀態：`exploration` (進入探索階段)
   - 創建時間戳
   - 功能基本信息
   - EPE 階段標記

3. **自動觸發 EPE 探索階段**
   - 立即執行 `/explore [feature-name]`
   - 深度理解程式碼庫和需求背景
   - 生成探索報告後才進入需求分析

## 示例

```bash
> /spec-init user-auth "實現用戶認證和授權系統"
```

### 執行流程範例

```markdown
🚀 初始化功能規格：user-auth

📚 階段 1/3：探索階段開始...
執行 /explore user-auth
- 掃描現有認證相關程式碼
- 分析專案架構和模式
- 識別相關依賴和整合點
- 評估技術風險和挑戰
✅ 探索報告已生成：.kiro/specs/user-auth/exploration.md

📋 階段 2/3：計畫階段開始...
執行 /plan user-auth
- 基於探索結果制定方案
- 分解任務和估算時間
- 定義成功標準
- 制定風險緩解策略
✅ 計畫文檔已生成：.kiro/specs/user-auth/plan.md

📝 階段 3/3：需求分析開始...
執行 /spec-requirements user-auth
- 調用 business-analyst-researcher
- 生成 BDD 場景
- 定義驗收標準
✅ 需求文檔已生成：.kiro/specs/user-auth/requirements.md

✨ 功能規格初始化完成！
- 已完成深度探索和計畫
- 下一步：審核後執行 /spec-design user-auth
```

## 整合版規格狀態流程

```
init → exploration → plan → requirements → design → tasks → execute → verify → completed
        ↑___EPE___↑         ↑_________SDD_________↑         ↑___EPE___↑
```

### 階段說明

**EPE 階段（新增）：**
1. **exploration**: 深度探索程式碼和需求（20-30分鐘）
2. **plan**: 制定詳細實施計畫（10-15分鐘）
3. **execute**: 紀律執行與品質控制
4. **verify**: 全面驗證與部署檢查

**SDD 階段（原有）：**
1. **requirements**: BDD需求分析
2. **design**: DDD架構設計
3. **tasks**: 任務分解
4. **implementation**: 實施開發

每個階段都需要人工審核確認才能進入下一階段，確保品質和正確性。

## 模板變量

創建規格時可以使用以下變量：
- `{feature_name}`: 功能名稱
- `{description}`: 功能描述
- `{timestamp}`: 創建時間
- `{author}`: 創建者（如果可獲得）

## 整合優勢

### EPE + SDD 整合帶來的改進

1. **更高成功率**
   - 探索階段將成功率從 60% 提升到 95%
   - 減少返工率至 20% 以下

2. **更好的上下文**
   - 在需求分析前已充分理解程式碼庫
   - 計畫階段確保實施路徑清晰

3. **更快的執行**
   - 前期投入減少後期問題
   - 執行階段效率提升 60%

4. **更完整的驗證**
   - 自動化驗證流程
   - 多層品質保證

## 注意事項

1. **命名規範**：功能名稱使用小寫字母和連字符
2. **唯一性檢查**：避免重複的功能名稱
3. **描述清晰**：提供清楚的功能描述有助於後續分析
4. **階段順序**：必須按照整合流程順序進行
5. **時間投入**：探索和計畫階段需要 30-45 分鐘，但能節省總體時間

## 相關命令

- `/explore [feature]` - 單獨執行探索階段
- `/plan [feature]` - 單獨執行計畫階段
- `/execute [feature]` - 執行實施階段
- `/verify [feature]` - 執行驗證階段
- `/spec-init-simple [feature]` - 使用簡化流程（小功能）