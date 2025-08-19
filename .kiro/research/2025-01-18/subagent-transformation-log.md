# 子代理系統改造研究日誌

## 改造原則
基於 VibeCodingNotes 的關鍵洞察：
1. 子代理應該是研究員，而非實施者
2. 上下文隔離會導致調試困難
3. 研究和規劃可以節省 50-80% 的 token

## 改造進度

### 2025-01-18

#### ✅ business-analyst → business-analyst-researcher
**改造要點**：
- 重新定位為純研究角色
- 移除所有實施相關功能
- 新增結構化輸出格式（研究報告、BDD場景、實施建議）
- 強調檔案系統作為輸出目標
- 保留原有的 MVP 原則，但轉為研究導向

**關鍵變更**：
1. 名稱：business-analyst → business-analyst-researcher
2. 工具：Read, Write, Grep, Analysis → Read, Search, Analyze, Plan
3. 輸出：直接實施 → 研究報告和規劃文檔
4. 協作：獨立工作 → 明確的父子代理協作流程

**預期效益**：
- Token 節省：預計減少 60-70%
- 準確性提升：專注研究可以更深入
- 調試改善：父代理擁有完整上下文

---

## 待改造項目

### General Template (6個)
- [ ] architect
- [ ] data-specialist
- [ ] integration-specialist
- [ ] test-engineer
- [ ] tech-lead
- [ ] context-manager

### Quant Template (9個)
- [ ] strategy-analyst
- [ ] risk-manager
- [ ] data-engineer
- [ ] api-specialist
- [ ] test-engineer
- [ ] tech-lead
- [ ] context-manager
- [ ] data-scientist
- [ ] hft-researcher
- [ ] quant-analyst

## 改造模式總結

### 通用改造步驟
1. **角色重定義**：從實施者改為研究者
2. **工具調整**：移除 Write，保留 Read/Search/Analyze
3. **輸出規範**：定義標準報告格式
4. **工作流程**：建立上下文讀取→研究→輸出的標準流程
5. **協作機制**：明確與父代理的互動方式

### 注意事項
- 保留原有的專業知識和原則
- 強化研究和分析能力描述
- 明確標示「不做實施」的邊界
- 提供具體的輸出路徑和格式