# Quant Template 子代理分析

## 現有代理清單（14個檔案）

### 核心業務代理
1. **strategy-analyst** - 策略需求分析
2. **risk-manager** - 風險管理
3. **quant-analyst** - 量化分析
4. **hft-researcher** - 高頻交易研究

### 數據相關代理
5. **data-engineer** - 數據工程
6. **data-scientist** - 數據科學/機器學習

### 技術實施代理
7. **architect-analyst** - 架構分析（類似 architect）
8. **developer-specialist** - 開發專家
9. **api-specialist** - API集成
10. **quality-engineer** - 品質工程（類似 quality-researcher）
11. **test-engineer** - 測試工程
12. **tech-lead** - 技術領導

### 通用代理
13. **context-manager** - 上下文管理
14. **general-assistant** - 通用助手

## 重疊分析和合併建議

### 建議合併
1. **quality-engineer + test-engineer + tech-lead** → **quality-researcher**
   - 理由：與 General Template 相同，品質相關職責可以整合
   
2. **architect-analyst + developer-specialist** → **system-architect-researcher**
   - 理由：架構和開發在研究模式下職責相近

### 保留獨立
- **strategy-analyst** - 量化策略的核心
- **risk-manager** - 風險管理極其重要
- **quant-analyst** - 量化模型核心
- **hft-researcher** - 高頻交易專業性強
- **data-engineer** - 數據管道專業
- **data-scientist** - ML/AI專業
- **api-specialist** - 交易API集成關鍵
- **context-manager** - 知識管理
- **general-assistant** - 保留但不需改造（已是助手角色）

## 最終結構（9個研究員）
1. strategy-analyst-researcher
2. risk-manager-researcher
3. quant-analyst-researcher
4. hft-researcher（已是researcher）
5. data-engineer-researcher
6. data-scientist-researcher
7. api-specialist-researcher
8. system-architect-researcher（合併）
9. quality-researcher（合併）
10. context-manager-researcher

## 改造優先順序
1. 先改造核心業務代理（strategy, risk, quant, hft）
2. 再改造數據代理（data-engineer, data-scientist）
3. 然後改造技術代理（api, architect+developer合併）
4. 最後處理合併（quality三合一）
5. context-manager 最後改造