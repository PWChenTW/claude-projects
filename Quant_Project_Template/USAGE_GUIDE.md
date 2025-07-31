# AI協作開發模板使用指南

## 📋 概述

這個模板整合了我們在對話中討論的所有AI協作最佳實踐：

1. **Claude-Claude Code 多實例協作** - 支援多個實例並行工作
2. **規格驅動開發 (SDD)** - 結構化的開發流程
3. **整合式方法論** - BDD + DDD + TDD 的完美結合
4. **Sub Agents 專業分工** - 10個專業AI助手
5. **Hooks 自動化** - 無需人工提醒的品質保證
6. **量化交易專業功能** - 針對金融領域優化

## 🎯 使用場景

### 適合的項目類型
✅ **量化交易系統開發**
✅ **複雜業務邏輯系統**
✅ **需要高代碼品質的項目**
✅ **團隊協作開發**
✅ **AI輔助開發探索**

### 不適合的項目類型
❌ 簡單的一次性腳本
❌ 純前端展示頁面
❌ 學習性質的小項目

## 🚀 快速開始三步驟

### Step 1: 複製模板
```bash
# 方式1: 直接複製目錄
cp -r /path/to/ai-collaboration-template my-new-project
cd my-new-project

# 方式2: 使用Git（如果已建立Git倉庫）
git clone [template-repo] my-new-project
cd my-new-project
```

### Step 2: 執行一鍵設置
```bash
# 運行設置腳本
./setup.sh

# 測試環境
./test_setup.sh
```

### Step 3: 初始化項目
```bash
# 啟動Claude Code
claude-code

# 初始化項目知識庫
> /steering-init

# 根據你的項目調整配置
> /steering-custom tech-stack "Python, FastAPI, PostgreSQL, Redis"
> /steering-custom business-domain "量化交易、風險管理"
```

## 🔄 開發工作流程

### 標準SDD流程

#### 1. 功能規格創建
```bash
> /spec-init "實現基於RSI的交易策略，當RSI低於30時開多倉，高於70時平倉"
```

系統會自動：
- 創建 `.kiro/specs/rsi-trading-strategy/` 目錄
- 生成 `spec.json` 狀態文件
- 準備BDD測試目錄

#### 2. 需求分析（BDD階段）
```bash
> /spec-requirements rsi-trading-strategy
```

**strategy-analyst** Sub Agent會：
- 分析策略邏輯
- 生成Gherkin場景
- 創建需求文檔
- 識別風險點

生成的文件：`.kiro/specs/rsi-trading-strategy/requirements.md`

#### 3. 技術設計（DDD階段）
人工審核需求後：
```bash
> /spec-design rsi-trading-strategy
```

系統會：
- 設計領域模型
- 定義實體和值對象
- 規劃系統架構
- 創建設計文檔

#### 4. 任務分解
設計審核通過後：
```bash
> /spec-tasks rsi-trading-strategy
```

生成具體的開發任務清單，包括：
- BDD測試任務
- TDD單元測試任務  
- DDD實體實現任務
- 整合測試任務

#### 5. 實施開發
任務清單確認後開始實施：
```bash
> 現在開始實施RSI交易策略
```

系統會自動：
- **test-engineer** 確保測試先行
- **risk-manager** 檢查風控措施
- **data-engineer** 處理數據需求
- **api-specialist** 優化API調用

### 多實例協作模式

#### 角色分工開發
```bash
# Terminal 1 - 策略架構師
claude-code --role architect
> 負責整體策略架構和核心邏輯設計

# Terminal 2 - 數據工程師  
claude-code --role data
> 使用 data-engineer 處理市場數據獲取和清洗

# Terminal 3 - 風控專家
claude-code --role risk
> 使用 risk-manager 實現風險管理和倉位控制

# Terminal 4 - 測試工程師
claude-code --role test
> 使用 test-engineer 建立完整的測試框架
```

#### 並行開發協調
1. **任務分配**：調度器自動分配任務給合適的實例
2. **分支管理**：每個角色在獨立分支工作
3. **定期同步**：使用Git merge整合進度
4. **衝突解決**：自動檢測並提醒處理衝突

## 🤖 Sub Agents 詳細使用

### strategy-analyst (策略分析師)
**最佳使用時機**：
- 策略構思階段
- 需求分析
- BDD場景設計
- 策略評估

**使用範例**：
```bash
> 使用 strategy-analyst 分析"雙均線交叉+成交量確認"的策略可行性

> 讓 strategy-analyst 為動量突破策略生成完整的BDD場景

> 請 strategy-analyst 評估這個策略在震蕩市場的表現
```

### risk-manager (風控專家)
**最佳使用時機**：
- 策略風險評估
- 倉位管理設計
- 風控規則制定
- 安全審查

**使用範例**：
```bash
> 使用 risk-manager 為這個策略設計風控規則

> 讓 risk-manager 檢查我的倉位計算是否合理

> 請 risk-manager 分析這個策略的最大回撤風險
```

### data-engineer (數據工程師)
**最佳使用時機**：
- 數據獲取設計
- 數據清洗處理
- 特徵工程
- 數據品質檢查

**使用範例**：
```bash
> 使用 data-engineer 設計股票數據的清洗流程

> 讓 data-engineer 實現技術指標的計算模組

> 請 data-engineer 處理這批歷史數據中的異常值
```

### api-specialist (API專家)
**最佳使用時機**：
- API集成設計
- 性能優化
- 錯誤處理
- 限流管理

**使用範例**：
```bash
> 使用 api-specialist 設計券商API的調用策略

> 讓 api-specialist 優化數據獲取的性能

> 請 api-specialist 處理API限流問題
```

### test-engineer (測試工程師)
**最佳使用時機**：
- 測試策略設計
- 自動化測試
- 品質檢查
- 重構支援

**使用範例**：
```bash
> 使用 test-engineer 為策略邏輯設計測試套件

> 讓 test-engineer 檢查我的測試覆蓋率

> 請 test-engineer 創建性能基準測試
```

### tech-lead (量化技術主管)
**最佳使用時機**：
- 技術決策
- 性能優化
- 系統穩定性
- 架構審查

**使用範例**：
```bash
> 使用 tech-lead 審查交易系統架構

> 讓 tech-lead 評估系統延遲優化方案

> 請 tech-lead 制定技術標準
```

### context-manager (量化上下文管理專家)
**最佳使用時機**：
- 策略文檔管理
- 知識庫維護
- 市場情報整理
- 決策記錄

**使用範例**：
```bash
> 使用 context-manager 整理策略研究文檔

> 讓 context-manager 更新市場事件記錄

> 請 context-manager 維護策略變更歷史
```

### data-scientist (數據科學家)
**最佳使用時機**：
- 機器學習建模
- 統計分析
- 因子研究
- 預測模型

**使用範例**：
```bash
> 使用 data-scientist 開發預測模型

> 讓 data-scientist 進行因子相關性分析

> 請 data-scientist 優化特徵選擇
```

### hft-researcher (高頻交易研究員)
**最佳使用時機**：
- 市場微觀結構分析
- 延遲優化
- 訂單執行研究
- 高頻策略開發

**使用範例**：
```bash
> 使用 hft-researcher 分析訂單簿動態

> 讓 hft-researcher 優化執行算法

> 請 hft-researcher 評估網絡延遲影響
```

### quant-analyst (量化分析師)
**最佳使用時機**：
- 金融建模
- 衍生品定價
- 投資組合優化
- 風險建模

**使用範例**：
```bash
> 使用 quant-analyst 建立期權定價模型

> 讓 quant-analyst 優化投資組合配置

> 請 quant-analyst 分析風險敞口
```

## 🔧 Hooks 自動化功能

### 自動代碼格式化
**觸發時機**：每次編輯Python、JavaScript、TypeScript文件後
**效果**：
- Python文件自動運行Black格式化
- JS/TS文件自動運行Prettier格式化
- 終端顯示 "✓ Formatted [filename]"

### 敏感文件保護
**觸發時機**：嘗試編輯保護文件時
**保護文件**：`.env`、`credentials`、`api_keys`、`secrets`等
**效果**：阻止修改並顯示警告信息

### API調用審計
**觸發時機**：執行包含API調用的命令時
**記錄內容**：時間戳、命令、調用類型
**查看方式**：`python scripts/monitoring/view_api_audit.py`

### 風控檢查
**觸發時機**：每次Claude Code完成響應後
**檢查內容**：是否有缺少止損的交易代碼
**效果**：發現問題時顯示風險警告

## 📊 監控與維護

### 進度追蹤
```bash
# 查看整體項目進度
python scripts/monitoring/progress_tracker.py

# 查看特定功能進度
python scripts/monitoring/progress_tracker.py --feature rsi-strategy

# 查看調度器狀態
tail -f .claude/scheduler/logs/scheduler.log
```

### 性能監控
```bash
# 系統性能監控
python scripts/monitoring/performance_monitor.py

# API調用分析
python scripts/monitoring/view_api_audit.py

# 檢查環境健康度
./test_setup.sh
```

### 日誌管理
```bash
# Sub Agent活動日誌
grep "agent:" .claude/scheduler/logs/*.log

# Hooks執行日誌
grep "hook:" .claude/scheduler/logs/*.log

# 錯誤日誌
grep "ERROR" .claude/scheduler/logs/*.log
```

## 🎯 高級應用技巧

### 1. 自定義Sub Agent
創建專門的Sub Agent處理特殊需求：

```markdown
<!-- .claude/agents/my-specialist.md -->
---
name: my-specialist
description: 我的專業領域專家，處理特定業務邏輯
tools: Read, Write, Analysis
---

你是[領域]專家，專門負責...
```

### 2. 擴展Hooks功能
在`.claude/settings.json`中添加新的Hook：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python my_custom_validator.py"
          }
        ]
      }
    ]
  }
}
```

### 3. 自定義Slash Commands
創建項目特定的命令：

```markdown
<!-- .claude/commands/deploy-strategy.md -->
# 部署策略

將策略部署到生產環境：

1. 執行完整測試套件
2. 檢查風控配置
3. 備份當前策略
4. 更新配置參數
5. 監控初始運行
```

### 4. 集成外部工具
在Hooks中集成外部工具：

```bash
# 代碼品質檢查
"command": "flake8 $file && mypy $file"

# 安全掃描  
"command": "bandit -r src/"

# 性能分析
"command": "python -m cProfile -o profile.out $script"
```

## 💡 最佳實踐總結

### 開發流程最佳實踐
1. **永遠從規格開始** - 使用`/spec-init`創建每個新功能
2. **遵循SDD階段** - 不要跳過需求分析和設計審核
3. **善用Sub Agents** - 讓專業的Agent處理專業的任務
4. **信任自動化** - 依賴Hooks而非人工提醒
5. **頻繁提交** - 保持Git歷史清晰可追溯

### 協作管理最佳實踐
1. **明確角色分工** - 每個實例專注特定領域
2. **統一術語** - 使用相同的業務語言
3. **定期同步** - 避免重複工作和衝突
4. **文檔先行** - 重要決策都要文檔化

### 品質保證最佳實踐
1. **測試驅動** - 關鍵邏輯先寫測試
2. **行為描述** - 用BDD描述業務邏輯
3. **持續驗證** - 利用Hooks自動檢查
4. **風險意識** - 交易邏輯必須有風控

### 效能優化最佳實踐
1. **Agent專業化** - 避免過於通用的Agent
2. **Hook輕量化** - 保持Hook邏輯簡單快速
3. **上下文管理** - 利用獨立上下文保持聚焦
4. **資源監控** - 定期檢查系統資源使用

## 🆘 常見問題解決

### Q: Sub Agent沒有被自動調用？
A: 
1. 檢查agent的description是否包含觸發關鍵詞
2. 嘗試顯式調用：「使用 [agent-name] 來...」
3. 確認`.claude/agents/`目錄中有對應的md文件

### Q: Hooks沒有觸發？
A:
1. 檢查`.claude/settings.json`語法是否正確
2. 確認matcher模式匹配工具名稱
3. 查看Claude Code輸出中的Hook錯誤信息

### Q: 任務調度器無法工作？
A:
1. 檢查`.claude/scheduler/logs/scheduler.log`
2. 確認Python依賴已安裝（psutil, schedule）
3. 重新運行`./setup.sh`

### Q: Git衝突如何處理？
A:
1. 使用分支隔離：每個實例使用獨立分支
2. 定期合併：`git merge feature-branch`
3. 解決衝突後重新分配任務

### Q: 如何添加新的開發方法論？
A:
1. 在`.kiro/steering/methodology.md`中說明
2. 創建對應的slash command
3. 在CLAUDE.md中添加觸發規則
4. 訓練Sub Agent理解新方法

## 🔄 升級與維護

### 模板更新
```bash
# 備份當前配置
cp -r .claude .claude.backup
cp CLAUDE.md CLAUDE.md.backup

# 下載新版本模板
# 合併更新內容

# 測試更新後的環境
./test_setup.sh
```

### 性能調優
```bash
# 監控Agent響應時間
python scripts/monitoring/performance_monitor.py

# 優化Hook執行效率
# 檢查Hook命令的執行時間

# 清理日誌文件
find .claude/scheduler/logs/ -name "*.log" -mtime +30 -delete
```

### 團隊同步
```bash
# 將優秀的Agent提升到用戶級別
cp .claude/agents/my-great-agent.md ~/.claude/agents/

# 分享Hook配置
# 將.claude/settings.json加入版本控制

# 更新團隊文檔
# 定期更新.kiro/steering/中的項目知識
```

---

🎉 **享受高效的AI協作開發體驗！**

這個模板為你提供了完整的AI協作開發環境。通過合理使用Sub Agents、遵循SDD流程、利用自動化Hooks，你將體驗到前所未有的開發效率和代碼品質。

每個新項目都基於這個模板開始，讓AI成為你最得力的開發夥伴！