# 量化交易項目 Git 工作流程指南

## 📋 概述

本文檔定義了量化交易AI協作開發項目的Git工作流程，針對金融領域的高風險特性，確保多實例協作的代碼管理和風險控制。

## 🌳 分支策略

### 主要分支結構

```
main (生產穩定版本)
├── develop (開發集成)
├── feature/[策略名稱] (策略開發)
├── role/[角色名稱] (角色專用)
├── hotfix/[修復名稱] (緊急修復)
├── release/[版本號] (發版準備)
└── backtest/[策略名稱] (回測分支)
```

### 分支命名規範

#### 策略分支 (Strategy Branches)
```bash
# 格式: feature/[strategy-type]-[name]
feature/momentum-rsi-crossover    # RSI動量交叉策略
feature/pairs-trading-cointegration # 配對交易協整策略
feature/mean-reversion-bollinger  # 布林帶均值回歸
feature/arbitrage-futures-spot    # 期現套利策略
```

#### 角色分支 (Role Branches)  
```bash
# 格式: role/[agent-name]-[date]
role/strategy-analyst-20240127    # 策略分析師專用分支
role/risk-manager-20240127        # 風控專家專用分支
role/data-engineer-20240127       # 數據工程師專用分支
```

#### 回測分支 (Backtest Branches)
```bash
# 格式: backtest/[strategy-name]-[period]
backtest/rsi-crossover-2020-2023  # RSI策略2020-2023回測
backtest/pairs-trading-validation # 配對交易驗證
```

## 🔄 量化交易特定工作流程

### 1. 策略開發流程

#### 創建策略分支
```bash
# 從develop分支創建策略分支
git checkout develop
git pull origin develop
git checkout -b feature/momentum-rsi-crossover

# 推送到遠程
git push -u origin feature/momentum-rsi-crossover
```

#### SDD規格驅動策略開發
```bash
# 1. 策略規格創建階段
git add .kiro/specs/momentum-rsi/spec.json
git commit -m "spec: 初始化RSI動量交叉策略規格

- 創建策略規格文件
- 設置初始狀態為requirements階段
- 準備回測目錄結構
- 設定風險參數框架"

# 2. 策略需求分析階段  
git add .kiro/specs/momentum-rsi/requirements.md
git commit -m "requirements(momentum-rsi): 完成策略BDD需求分析

- 定義RSI指標參數範圍 (14週期, 30/70閾值)
- 創建進場/出場條件Gherkin場景
- 識別市場條件和風險約束
- 設定最大回撤和夏普比率目標
- strategy-analyst: 策略邏輯驗證完成"

# 3. 風險評估和技術設計階段
git add .kiro/specs/momentum-rsi/design.md
git commit -m "design(momentum-rsi): 完成策略DDD技術設計

- 設計交易信號領域模型
- 定義訂單管理和倉位控制
- 實現風險管理規則和止損機制
- 設計回測框架和性能評估
- risk-manager: 風控設計已審核
- architect: 技術架構已確認"
```

#### 回測驗證流程
```bash
# 創建回測分支
git checkout -b backtest/momentum-rsi-validation
git commit -m "backtest: 建立RSI策略回測環境

- 準備2020-2023歷史數據
- 配置回測參數和基準
- 設定性能評估指標
- 建立風險分析框架"

# 回測結果提交
git add backtests/momentum-rsi/results.json
git add backtests/momentum-rsi/performance_report.md
git commit -m "backtest(momentum-rsi): 完成策略回測驗證

回測期間: 2020-01-01 到 2023-12-31
總收益率: 23.5%
最大回撤: -8.2%
夏普比率: 1.47
勝率: 58.3%

風險指標:
- VaR (95%): 2.1%
- 月度波動率: 12.3%
- 相關性分析: 與大盤相關性0.23

data-engineer: 數據品質驗證通過
test-engineer: 回測邏輯測試完成"
```

### 2. 風險管理工作流

#### 風險審查提交
```bash
# 風險評估提交
git add risk_assessments/momentum-rsi-risk.md
git commit -m "risk(momentum-rsi): 完成策略風險評估

風險分析結果:
- 市場風險: 中等 (股票beta 0.8)
- 流動性風險: 低 (大盤股票策略)
- 模型風險: 低-中等 (簡單技術指標)
- 操作風險: 低 (自動化執行)

風控措施:
- 單筆交易風險限額: 2%
- 日內最大虧損: 5%
- 月度最大回撤: 10%
- 強制止損: -3%

risk-manager: 風險評估通過
strategy-analyst: 風控參數確認"
```

#### 合規檢查
```bash
# 合規檢查提交
git add compliance/trading_rules_check.md
git commit -m "compliance: 策略合規性檢查

合規檢查項目:
✓ 無內幕交易邏輯
✓ 無市場操縱行為
✓ 符合融資融券規定
✓ 符合T+1交易規則
✓ 風險披露完整

監管要求:
- 符合證監會量化交易管理辦法
- 滿足交易所高頻交易規範
- 風險控制措施充分

api-specialist: API合規性驗證完成"
```

### 3. 生產部署流程

#### 預生產驗證
```bash
# 創建發布分支
git checkout develop
git checkout -b release/momentum-rsi-v1.0.0

# 生產前檢查
git add deployment/production_checklist.md
git commit -m "release: 準備RSI策略v1.0.0生產部署

生產前檢查清單:
✓ 回測結果驗證 (夏普比率 1.47)
✓ 風險管理測試通過
✓ API連接穩定性測試
✓ 錯誤處理機制驗證
✓ 監控和報警設置

部署參數:
- 初始資金: 100萬
- 最大倉位: 80%
- 風險限額: 日內5%, 月度10%
- 監控頻率: 1分鐘

risk-manager: 生產風控設置確認
api-specialist: 券商API集成測試通過"
```

#### 生產部署
```bash
# 合併到main分支
git checkout main
git merge --no-ff release/momentum-rsi-v1.0.0
git tag -a "v1.0.0-momentum-rsi" -m "RSI動量交叉策略 v1.0.0

策略特性:
- RSI(14) 超買超賣策略
- 30/70 進場出場閾值
- 2% 個股風險限額
- 自動止損 -3%

回測性能:
- 年化收益: 23.5%
- 最大回撤: -8.2%
- 夏普比率: 1.47
- 交易勝率: 58.3%

風險控制:
- VaR(95%): 2.1%
- 日內風險限額: 5%
- 月度風險限額: 10%
- 實時監控和報警

合規狀態: 已通過"

git push origin main
git push origin --tags
```

## 📝 量化交易提交信息規範

### 提交類型 (Type)
```
strategy:   策略開發
backtest:   回測相關
risk:       風險管理
data:       數據處理
api:        API集成
monitor:    監控相關
compliance: 合規檢查
deploy:     部署相關
fix:        錯誤修復
docs:       文檔更新
```

### 提交信息格式
```
<type>(<strategy-name>): <subject>

<body>

<performance-metrics>
<risk-metrics>
<footer>
```

### 提交信息示例
```bash
# 策略實現
git commit -m "strategy(momentum-rsi): 實現RSI動量交叉核心邏輯

- 實現RSI(14)指標計算
- 添加30/70超買超賣判斷
- 實現進場出場信號生成
- 集成止損和止盈邏輯

性能指標:
- 信號準確率: 初步測試65%
- 平均持倉期: 3.2天

風險控制:
- 單筆最大風險: 2%
- 實時止損: -3%

Tested-by: test-engineer
Reviewed-by: risk-manager"

# 回測提交
git commit -m "backtest(pairs-trading): 完成配對交易策略回測

回測參數:
- 標的池: 滬深300成分股
- 協整檢驗: ADF測試 p<0.05
- 配對數量: 15對
- 回測期間: 2021-2024

回測結果:
- 總收益率: 31.2%
- 年化收益: 9.8%
- 最大回撤: -6.3%
- 夏普比率: 1.83
- 卡爾瑪比率: 1.56

風險分析:
- 月度勝率: 71.2%
- 平均持倉: 8.5天
- 最大單日虧損: -2.1%

Data-quality: validated
Risk-assessment: approved"

# 風險管理
git commit -m "risk(portfolio): 更新投資組合風險管理規則

風險限額調整:
- 單策略最大權重: 30% → 25%
- 相關性上限: 0.7 → 0.6
- 集中度限制: 加強行業分散

新增風控措施:
- 實時Greeks監控
- 動態對沖機制
- 尾部風險預警

風險模型更新:
- 集成蒙特卡羅VaR
- 添加壓力測試場景
- 流動性風險評估

Impact-assessment: 預期風險降低15%
Approved-by: risk-manager"
```

## 🔄 自動化風險工作流

### Git Hooks 風險集成

#### Pre-commit Hook (風險檢查)
```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🔍 運行交易策略風險檢查..."

# 檢查是否包含風險管理代碼
if grep -r "buy\|sell\|order" src/ --include="*.py"; then
    if ! grep -r "stop_loss\|risk_limit\|position_size" src/ --include="*.py"; then
        echo "❌ 警告: 發現交易邏輯但缺少風險管理!"
        echo "請確保包含止損、風險限額或倉位控制邏輯"
        exit 1
    fi
fi

# 檢查回測結果
if [ -d "backtests/" ]; then
    if ! find backtests/ -name "*results*" -mtime -7 | grep -q .; then
        echo "⚠️  警告: 回測結果超過7天未更新"
        echo "建議重新運行回測驗證"
    fi
fi

# 運行策略驗證
if [ -f "scripts/strategy_validator.py" ]; then
    if ! python scripts/strategy_validator.py; then
        echo "❌ 策略驗證失敗"
        exit 1
    fi
fi

echo "✅ 風險檢查通過"
```

#### Post-commit Hook (風險通知)
```bash
#!/bin/bash
# .git/hooks/post-commit

# 檢查是否為策略相關提交
if git log --format=%B -n 1 | grep -E "strategy|backtest|risk"; then
    echo "📊 策略變更通知已發送到風控團隊"
    
    # 自動生成風險評估報告
    if [ -f "scripts/risk_reporter.py" ]; then
        python scripts/risk_reporter.py --latest-commit
    fi
fi
```

### 分支保護規則

#### Main分支保護 (生產策略)
```yaml
# .github/branch_protection.yml
main:
  protect: true
  required_status_checks:
    strict: true
    contexts:
      - "backtest-validation"
      - "risk-assessment"
      - "compliance-check"
      - "performance-benchmarks"
  enforce_admins: true
  required_pull_request_reviews:
    required_approving_review_count: 3  # 需要風控專家審核
    required_review_from_code_owners: true
    dismiss_stale_reviews: true
  restrictions:
    users: ["risk-manager", "lead-trader"]
```

## 📊 量化交易工作流監控

### 策略開發進度追蹤
```bash
# 策略開發狀態腳本
#!/bin/bash
# scripts/strategy_status.sh

echo "📈 量化策略開發狀態"
echo "==================="

# 檢查活躍策略分支
echo "🚀 開發中的策略:"
git branch -r | grep "feature/" | while read branch; do
    strategy_name=$(echo $branch | cut -d'/' -f2)
    last_commit=$(git log -1 --format="%cd" --date=short "$branch")
    echo "  $strategy_name (最後更新: $last_commit)"
    
    # 檢查回測狀態
    if git show "$branch" --name-only | grep -q "backtests/"; then
        echo "    ✓ 包含回測結果"
    else
        echo "    ⚠ 缺少回測驗證"
    fi
done

# 檢查風險評估狀態
echo "🛡️ 風險評估狀態:"
for spec in .kiro/specs/*/; do
    if [ -d "$spec" ]; then
        spec_name=$(basename "$spec")
        if [ -f "$spec/risk_assessment.md" ]; then
            echo "  $spec_name: 風險評估完成"
        else
            echo "  $spec_name: ⚠ 待風險評估"
        fi
    fi
done

# 檢查生產部署
echo "🎯 生產環境策略:"
git tag | grep -E "v[0-9]+" | tail -5 | while read tag; do
    tag_date=$(git log -1 --format="%cd" --date=short "$tag")
    echo "  $tag (部署日期: $tag_date)"
done
```

### 回測結果追蹤
```bash
# 回測監控腳本
#!/bin/bash
# scripts/backtest_monitor.sh

echo "📊 回測結果監控"
echo "==============="

# 統計回測分支
echo "🔬 回測分支統計:"
backtest_count=$(git branch -r | grep "backtest/" | wc -l)
echo "  總回測分支數: $backtest_count"

# 最新回測結果
echo "📈 最新回測結果:"
find backtests/ -name "*.json" -mtime -30 | while read result_file; do
    strategy=$(dirname "$result_file" | xargs basename)
    echo "  $strategy:"
    
    if command -v jq >/dev/null 2>&1; then
        # 提取關鍵指標
        returns=$(jq -r '.total_return // "N/A"' "$result_file")
        sharpe=$(jq -r '.sharpe_ratio // "N/A"' "$result_file")
        max_dd=$(jq -r '.max_drawdown // "N/A"' "$result_file")
        
        echo "    總收益: $returns"
        echo "    夏普比率: $sharpe"
        echo "    最大回撤: $max_dd"
    fi
done
```

### 風險指標監控
```bash
# 風險監控腳本  
#!/bin/bash
# scripts/risk_monitor.sh

echo "🛡️ 風險指標監控"
echo "==============="

# 檢查風險文件更新
echo "📋 風險評估文件:"
find . -name "*risk*" -type f -mtime -7 | while read risk_file; do
    echo "  $risk_file (最近更新)"
done

# 策略風險統計
echo "⚠️ 風險狀態統計:"
total_strategies=$(find .kiro/specs/ -type d -mindepth 1 | wc -l)
risk_assessed=$(find .kiro/specs/ -name "risk_assessment.md" | wc -l)
echo "  總策略數: $total_strategies"
echo "  已風險評估: $risk_assessed"
echo "  評估覆蓋率: $(($risk_assessed * 100 / $total_strategies))%"

# 檢查風險限額合規
echo "📊 風險限額檢查:"
if [ -f "config/risk_limits.json" ]; then
    echo "  ✓ 風險限額配置存在"
    # 可以加入具體限額檢查邏輯
else
    echo "  ❌ 缺少風險限額配置"
fi
```

這個量化交易Git工作流程確保了：
- 🔄 **策略開發的規範化流程**
- 🛡️ **風險管理的強制性檢查**  
- 📊 **回測驗證的完整追蹤**
- 🎯 **生產部署的嚴格控制**
- 📈 **性能指標的持續監控**