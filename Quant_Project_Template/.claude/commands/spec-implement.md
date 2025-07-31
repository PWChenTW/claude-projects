# /spec-implement - 實施階段管理

## 用途
進入策略功能的實施階段，協調開發工作並追蹤進度。

## 語法
```
/spec-implement <feature-name> [task-id]
```

## 參數
- `<feature-name>`: 功能名稱（必需）
- `[task-id]`: 特定任務ID（可選）- 直接開始特定任務

## 執行流程

### 1. 驗證前置條件
- 確認功能存在於 `.kiro/specs/`
- 檢查 `spec.json` 中的狀態
- 確認 tasks 階段已完成
- 驗證風險評估是否完成

### 2. 進入實施模式
如果未指定 task-id：
- 顯示所有任務清單和狀態
- 標記 spec 狀態為 "implementation"
- 根據風險等級建議開始順序

如果指定了 task-id：
- 直接開始該任務的實施
- 調用適當的 Sub Agent
- 更新任務狀態為 "in_progress"

### 3. 實施協調
- **自動調用適當的 Sub Agent**：
  - 策略邏輯 → strategy-analyst
  - 風控規則 → risk-manager
  - 數據處理 → data-engineer
  - API整合 → api-specialist
  - 性能優化 → hft-researcher
- **進度追蹤**：
  - 更新 `spec.json` 中的任務狀態
  - 記錄實施開始時間
  - 追蹤回測結果
- **品質檢查**：
  - 自動執行單元測試
  - 觸發回測驗證
  - 風險規則檢查

### 4. 任務完成處理
- 更新任務狀態為 "completed"
- 執行策略回測
- 生成性能報告
- 檢查風控合規性
- 若全部完成，提示進入驗收階段

## 狀態管理
任務狀態流轉：
- `pending` → `in_progress` → `completed`
- `blocked` 狀態（遇到數據或技術阻礙）
- `testing` 狀態（回測中）

## 範例

### 查看所有任務並進入實施模式
```
/spec-implement momentum-strategy
```

### 直接開始特定任務
```
/spec-implement momentum-strategy T001
```

## 輸出格式
```
📊 策略實施：[feature-name]

當前進度：
✅ T001: 實現數據獲取模組 [completed]
🔄 T002: 開發技術指標計算 [in_progress]
🧪 T003: 實現交易信號生成 [testing]
⏳ T004: 整合風控規則 [pending]
⏳ T005: 實現下單執行 [pending]

整體進度：40% (2/5 完成)
回測進度：處理中... (2021-01至2021-06)

建議：T002 需要 data-engineer 協助優化指標計算性能。
風險提醒：確保 T004 風控規則在 T005 下單執行前完成。
```

## 相關命令
- `/spec-init` - 初始化新策略功能
- `/spec-tasks` - 查看或更新任務列表
- `/spec-backtest` - 執行策略回測
- `/spec-risk` - 風險評估報告
- `/spec-complete` - 完成功能並生成報告

## 注意事項
- 實施前確保風險評估已完成
- 關鍵計算邏輯必須有單元測試
- 所有交易邏輯必須經過回測驗證
- 風控規則必須在實盤前完整實施
- 保持與設計文檔的一致性
- 記錄所有重要的策略參數和閾值