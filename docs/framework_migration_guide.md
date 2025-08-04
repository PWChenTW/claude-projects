# 框架優化遷移指南

## 概述
本指南幫助您從原有的強制性多階段委派框架遷移到更靈活的優化版框架。

## 主要變化

### 1. Agent 精簡
**原本**: 7-8 個專門的 Sub Agents
**現在**: 4 個綜合性專家角色

| 原 Agents | 新 Agent | 職責合併 |
|-----------|----------|----------|
| architect + business-analyst | architect-analyst | 架構設計 + 需求分析 |
| data-specialist + integration-specialist | developer-specialist | 演算法 + API + 實現 |
| test-engineer | quality-engineer | 測試 + 品質 + 安全 |
| tech-lead | tech-lead | 保持不變 |

### 2. 委派策略
**原本**: 強制多階段委派，禁止直接實作
**現在**: 智能判斷，根據複雜度決定

```
簡單任務 → 直接處理
中等任務 → 選擇性諮詢
複雜任務 → 多角度分析
```

### 3. 文檔結構
**原本**: 詳細的規格文檔要求
**現在**: 根據需要創建文檔

- 簡單功能：代碼註釋即可
- 複雜功能：創建必要的設計文檔

## 遷移步驟

### Step 1: 更新 CLAUDE.md
```bash
# 備份原文件
cp CLAUDE.md CLAUDE_OLD.md

# 使用優化版
cp CLAUDE_OPTIMIZED.md CLAUDE.md
```

### Step 2: 更新 Agent 定義
```bash
# 移除舊的 agents
rm .claude/agents/business-analyst.md
rm .claude/agents/data-specialist.md
rm .claude/agents/integration-specialist.md

# 使用新的綜合 agents
# architect-analyst.md
# developer-specialist.md
# quality-engineer.md
```

### Step 3: 調整工作流程
1. 開始使用 `/spec-init-simple` 進行快速初始化
2. 只在必要時使用完整的 SDD 流程
3. 相信 Claude 的判斷力

## 使用場景對比

### 場景 1: 添加用戶頭像上傳功能

**舊流程**:
1. /spec-init user-avatar
2. 委派 architect 分析
3. 委派 business-analyst 定義需求
4. 委派 data-specialist 設計存儲
5. 委派 test-engineer 設計測試
6. 開始實現

**新流程**:
1. /spec-init-simple user-avatar "用戶頭像上傳"
2. Claude 判斷為簡單功能
3. 直接實現，必要時諮詢 developer-specialist

### 場景 2: 實現支付系統

**舊流程**: 
強制執行完整的多階段流程

**新流程**:
1. Claude 識別為複雜功能
2. 主動建議諮詢 architect-analyst
3. 協調多個專家參與
4. 但保持靈活性

## 注意事項

### Do's ✅
- 相信 Claude 的判斷
- 從簡單開始
- 根據實際需要調整流程
- 保持代碼品質

### Don'ts ❌
- 不要為了流程而流程
- 不要過度文檔化
- 不要害怕直接實現簡單功能
- 不要忽視真正需要深思的複雜任務

## 回滾方案

如果需要回到原框架：
```bash
# 恢復原 CLAUDE.md
cp CLAUDE_OLD.md CLAUDE.md

# 恢復所有 agent 定義
git checkout HEAD -- .claude/agents/
```

## 持續優化

這個優化版框架是一個起點，鼓勵根據實際使用體驗：
- 調整 agent 角色
- 優化判斷標準
- 簡化流程
- 提高效率

記住：最好的框架是幾乎感覺不到它存在的框架。