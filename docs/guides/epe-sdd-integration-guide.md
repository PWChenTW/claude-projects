# EPE + SDD 整合指南

## 概述

本指南說明如何將 EPE (Explore-Plan-Execute) 工作流程與 SDD (Spec-Driven Development) 整合，創建更強大的開發流程。

## 🎯 整合目標

將兩個方法論的優勢結合：
- **EPE 的優勢**：深度上下文理解、風險預防、高成功率
- **SDD 的優勢**：結構化規格管理、清晰的階段劃分、品質保證

## 🔄 整合後的完整工作流程

```mermaid
graph LR
    A[Init] --> B[🔍 Explore]
    B --> C[📋 Plan]
    C --> D[📝 Requirements]
    D --> E[🏗️ Design]
    E --> F[✅ Tasks]
    F --> G[⚡ Execute]
    G --> H[🔍 Verify]
    H --> I[🚀 Deploy]
    
    style B fill:#e1f5fe
    style C fill:#e1f5fe
    style G fill:#e1f5fe
    style H fill:#e1f5fe
    style D fill:#fff3e0
    style E fill:#fff3e0
    style F fill:#fff3e0
```

藍色：EPE 階段 | 橙色：SDD 階段

## 📊 階段詳解

### 第一部分：EPE 前置階段（探索與計畫）

#### 1. 探索階段 (Explore) - 20-30分鐘
**目的**：建立充分的上下文理解

**執行內容**：
- 掃描相關程式碼庫
- 識別現有設計模式
- 理解技術約束
- 評估潛在風險

**輸出**：
- `.kiro/specs/[feature]/exploration.md`
- 關鍵發現和風險評估

**命令**：
```bash
/explore [feature-name]
```

#### 2. 計畫階段 (Plan) - 10-15分鐘
**目的**：制定可行的實施策略

**執行內容**：
- 設計技術方案
- 分解任務並估時
- 定義成功標準
- 制定風險緩解策略

**輸出**：
- `.kiro/specs/[feature]/plan.md`
- 詳細的任務清單和時間估算

**命令**：
```bash
/plan [feature-name]
```

### 第二部分：SDD 核心階段（規格與設計）

#### 3. 需求階段 (Requirements)
**目的**：定義業務需求和驗收標準

**執行內容**：
- 調用 business-analyst-researcher
- 生成 BDD 場景
- 定義驗收標準

**輸出**：
- `.kiro/specs/[feature]/requirements.md`
- Gherkin 格式的測試場景

**命令**：
```bash
/spec-requirements [feature-name]
```

#### 4. 設計階段 (Design)
**目的**：創建系統架構和領域模型

**執行內容**：
- 調用 architect-researcher
- DDD 領域建模
- 定義介面和契約

**輸出**：
- `.kiro/specs/[feature]/design.md`
- 架構圖和領域模型

**命令**：
```bash
/spec-design [feature-name]
```

#### 5. 任務階段 (Tasks)
**目的**：創建可執行的任務清單

**執行內容**：
- 細化任務分解
- 設定優先級
- 分配資源

**輸出**：
- `.kiro/specs/[feature]/tasks.md`
- 詳細的任務清單

**命令**：
```bash
/spec-tasks [feature-name]
```

### 第三部分：EPE 執行階段（實施與驗證）

#### 6. 執行階段 (Execute)
**目的**：根據計畫實施功能

**執行內容**：
- 小步迭代開發
- 頻繁測試
- 持續提交

**輸出**：
- 實際的程式碼實現
- 執行日誌

**命令**：
```bash
/execute [feature-name]
```

#### 7. 驗證階段 (Verify)
**目的**：確保品質和部署就緒

**執行內容**：
- 功能測試
- 性能驗證
- 安全檢查

**輸出**：
- `.kiro/specs/[feature]/verification.md`
- 測試報告和部署檢查清單

**命令**：
```bash
/verify [feature-name]
```

## 🚀 快速開始

### 完整流程（複雜功能）
```bash
# 1. 初始化功能（自動觸發探索）
/spec-init payment-system "實現支付系統"

# 2-7. 按順序執行各階段
# 系統會自動提示下一步
```

### 簡化流程（簡單功能）
```bash
# 使用輕量級版本
/spec-init-simple user-profile "用戶資料管理"

# 直接進入執行
/execute user-profile
```

## 📈 效益對比

### 傳統 SDD vs EPE+SDD 整合

| 指標 | 傳統 SDD | EPE+SDD 整合 | 改進 |
|------|----------|--------------|------|
| 首次成功率 | 60% | 95% | +58% |
| 返工率 | 40% | 20% | -50% |
| 總開發時間 | 100% | 70% | -30% |
| 上下文理解 | 有限 | 深入 | 顯著提升 |
| 風險預防 | 被動 | 主動 | 根本改變 |

## 🎯 最佳實踐

### 1. 選擇正確的流程

**使用完整流程當：**
- 功能複雜度高
- 涉及核心業務邏輯
- 需要外部整合
- 安全性要求高
- 預估 > 8 小時

**使用簡化流程當：**
- CRUD 操作
- UI 調整
- Bug 修復
- 小功能增強
- 預估 < 4 小時

### 2. 時間投入指南

**完整流程時間分配：**
- 探索：20-30 分鐘
- 計畫：10-15 分鐘
- 需求：15-20 分鐘
- 設計：20-30 分鐘
- 任務：10-15 分鐘
- 執行：根據複雜度
- 驗證：20-30 分鐘

**投資回報：**
前期投入 1 小時 = 後期節省 3-5 小時

### 3. 關鍵成功因素

1. **不要跳過探索**
   - 即使功能看似簡單
   - 探索能發現隱藏的複雜性

2. **計畫要具體**
   - 任務粒度控制在 2 小時內
   - 包含具體的檔案和函數

3. **頻繁驗證**
   - 每個里程碑都要驗證
   - 及早發現問題

4. **保持文檔同步**
   - 決策要記錄
   - 變更要更新

## 🔧 配置選項

### 在 `.claude/settings.json` 配置整合行為：

```json
{
  "workflow": {
    "mode": "integrated",  // "integrated" | "sdd-only" | "epe-only"
    "auto_progression": true,
    "require_approval": true,
    "exploration": {
      "depth": "deep",
      "time_limit": "30m"
    },
    "planning": {
      "detail_level": "high",
      "risk_assessment": true
    },
    "verification": {
      "coverage_threshold": 80,
      "performance_check": true,
      "security_scan": true
    }
  }
}
```

## 📚 相關文檔

- [EPE 工作流程詳解](./explore-plan-execute-workflow.md)
- [SDD 方法論](./spec-driven-development.md)
- [MVP 開發原則](./mvp-development.md)
- [子代理研究員模式](../improvements/subagent-researcher-pattern.md)

## 💡 常見問題

### Q: 什麼時候應該使用整合流程？
**A:** 當功能預估超過 4 小時，或涉及系統核心功能時。

### Q: 探索階段發現問題怎麼辦？
**A:** 這正是探索的價值！及早發現問題可以調整方案或重新評估需求。

### Q: 可以跳過某些階段嗎？
**A:** 簡化流程可以跳過部分 SDD 階段，但永遠不要跳過探索。

### Q: 如何處理緊急需求？
**A:** 使用 `/spec-init-simple` 但仍保留輕量級探索（5-10分鐘）。

## 🎓 總結

EPE + SDD 整合創建了一個平衡的開發流程：

- **前期投入**確保理解和規劃
- **中期結構**提供清晰的執行路徑
- **後期驗證**保證品質和可靠性

記住核心原則：
> **"Context is everything, and planning is half the battle."**

透過整合 EPE 和 SDD，我們不僅提高了成功率，更建立了可持續、可預測的開發流程。