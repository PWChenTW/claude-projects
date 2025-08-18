# 子代理批量改造總結

## 改造進度

### ✅ 已完成 (2/7)
1. business-analyst → business-analyst-researcher
2. architect → architect-researcher

### 🔄 進行中 (5/7)
需要批量改造的子代理：
- data-specialist
- integration-specialist  
- test-engineer
- tech-lead
- context-manager

## 批量改造模式

為了提高效率，剩餘的子代理將採用標準化模式批量改造：

### 通用改造模板

```yaml
原名稱: [agent-name]
新名稱: [agent-name]-researcher
描述: [領域]研究專家，負責[核心職責]（只做研究和規劃，不做實施）
工具: Read, Search, Analyze, Plan

核心變更:
  - 角色: 實施者 → 研究者
  - 輸出: 程式碼 → 研究報告/規劃文檔
  - 工具: Write/Execute → Analyze/Plan
  - 協作: 獨立 → 父子代理明確分工
```

### 標準章節結構

1. **角色定位** - 明確研究職責
2. **MVP研究原則** - 保留原有原則但轉為研究導向
3. **工作流程** - 上下文→研究→輸出
4. **輸出格式** - 3種標準文檔格式
5. **與父代理協作** - 明確互動方式
6. **範例場景** - 具體研究案例
7. **核心能力** - 研究和分析能力
8. **工具使用** - 搜索和分析命令
9. **限制邊界** - 明確不做實施
10. **成功指標** - 可衡量的研究成果

## 快速改造計劃

### data-specialist-researcher
- 核心：數據結構研究、算法分析、性能評估
- 輸出：算法研究報告、性能分析、優化建議

### integration-specialist-researcher  
- 核心：API設計研究、集成方案評估、協議分析
- 輸出：集成架構報告、API規範、風險評估

### test-engineer-researcher
- 核心：測試策略研究、覆蓋率分析、品質評估
- 輸出：測試計劃、品質報告、改進建議

### tech-lead-researcher
- 核心：技術決策研究、最佳實踐分析、團隊流程優化
- 輸出：技術評估報告、決策建議、流程改進方案

### context-manager-researcher
- 核心：知識管理研究、文檔體系規劃、信息架構設計
- 輸出：知識管理方案、文檔標準、信息流程圖

## 預期效益

通過批量改造，預計：
- **開發時間**：從每個30分鐘減少到5分鐘
- **一致性**：100%遵循研究員模式
- **Token節省**：整體減少60-70%
- **調試效率**：提升3倍以上