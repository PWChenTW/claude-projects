# Quant Template 子代理批量改造計劃

## 改造策略
基於 General Template 的成功經驗，使用相同的模式但保留量化交易的專業特色。

## 需要改造的代理清單

### 核心業務代理（已完成1個）
1. ✅ strategy-analyst → strategy-analyst-researcher 
2. ⏳ risk-manager → risk-manager-researcher
3. ⏳ quant-analyst → quant-analyst-researcher
4. ⏳ hft-researcher（已是researcher，只需調整）

### 數據相關代理
5. ⏳ data-engineer → data-engineer-researcher
6. ⏳ data-scientist → data-scientist-researcher

### 技術實施代理
7. ⏳ api-specialist → api-specialist-researcher
8. ⏳ architect-analyst + developer-specialist → system-architect-researcher（合併）
9. ⏳ quality-engineer + test-engineer + tech-lead → quality-researcher（合併）

### 通用代理
10. ⏳ context-manager → context-manager-researcher

## 批量改造要點

### 統一修改模式
1. **名稱更新**：添加 -researcher 後綴
2. **工具更新**：Read, Search, Analyze, Plan
3. **角色定位**：加入「只做研究和規劃，不做實施」聲明
4. **工作流程**：統一三步驟（讀取上下文、進行研究、輸出成果）
5. **輸出格式**：結構化的研究報告格式

### 保留專業特色
- **策略類**：保留量化策略、技術指標、回測分析
- **風控類**：保留VaR、夏普比率、最大回撤等專業指標
- **數據類**：保留時間序列、特徵工程、因子分析
- **交易類**：保留訂單類型、市場微觀結構、延遲優化

## 執行計劃
1. 先完成核心業務代理（策略、風控、量化、高頻）
2. 再處理數據代理（數據工程、數據科學）
3. 然後處理技術代理（API、架構）
4. 最後處理合併和通用代理