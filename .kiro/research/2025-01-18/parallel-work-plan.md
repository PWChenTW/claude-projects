# 並行工作計劃 - Git Worktree

## 工作目錄結構
```
/Users/chenpowen/Python Projects/
├── claude/                    # 主工作目錄 (feature/ai-framework-enhancement)
├── claude-epe/                # EPE 工作流程開發 (feature/epe-workflow)
└── claude-quant/              # Quant 代理改造 (feature/quant-agents)
```

## 並行任務分配

### Worktree 1: claude-epe (EPE 工作流程)
**分支**: feature/epe-workflow
**任務**：
1. 創建 explore.md 命令 - 探索階段
2. 創建 plan.md 命令 - 計劃階段
3. 創建 execute.md 命令 - 執行階段
4. 創建 verify.md 命令 - 驗證階段
5. 整合到現有 SDD 流程

**檔案位置**：
- General_Project_Template/.claude/commands/explore.md
- General_Project_Template/.claude/commands/plan.md
- General_Project_Template/.claude/commands/execute.md
- General_Project_Template/.claude/commands/verify.md

### Worktree 2: claude-quant (Quant 代理改造)
**分支**: feature/quant-agents
**任務**：
1. 改造 quant-analyst → quant-analyst-researcher
2. 調整 hft-researcher（已是researcher）
3. 改造 data-engineer → data-engineer-researcher
4. 改造 data-scientist → data-scientist-researcher
5. 改造 api-specialist → api-specialist-researcher
6. 合併 architect-analyst + developer-specialist → system-architect-researcher
7. 合併 quality-engineer + test-engineer + tech-lead → quality-researcher
8. 改造 context-manager → context-manager-researcher

**檔案位置**：
- Quant_Project_Template/.claude/agents/*.md

## 執行策略

### 第一階段（並行執行）
**時間**: 30-45分鐘

**EPE 線程**：
- 基於 docs/guides/explore-plan-execute-workflow.md 創建命令
- 每個命令包含：角色定位、觸發條件、工作流程、輸出格式

**Quant 線程**：
- 使用批量改造模式
- 保留量化交易專業術語
- 統一輸出格式

### 第二階段（整合）
**時間**: 15分鐘
1. 在各自 worktree 中提交變更
2. 切回主分支 feature/ai-framework-enhancement
3. 合併兩個分支的變更
4. 解決任何衝突（預期很少）
5. 測試整合效果

## 預期成果

### EPE 工作流程
- 4個新的命令文件
- 完整的三階段開發流程
- 與 SDD 整合的說明

### Quant 代理改造
- 10個改造完成的研究員代理
- 從14個精簡到10個
- 保留所有量化專業知識

## 協調要點
- 兩個任務獨立，衝突風險低
- EPE 主要在 General_Project_Template
- Quant 改造主要在 Quant_Project_Template
- 共用的只有進度追蹤文檔

## 下一步
1. 開始 EPE 命令創建
2. 同時進行 Quant 代理批量改造
3. 每完成一個里程碑就提交
4. 最後整合並測試