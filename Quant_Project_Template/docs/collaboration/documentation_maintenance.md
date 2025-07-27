# 量化交易項目文檔維護指南

## 📋 概述

本指南定義了量化交易AI協作開發項目的文檔維護策略，確保交易策略文檔、風險評估報告、回測結果與代碼保持同步，並為團隊提供準確、實用的交易決策信息。

## 📚 量化交易文檔體系結構

### 1. 核心配置文檔
```
├── README.md                    # 項目概述和快速開始
├── CLAUDE.md                    # Claude Code 主配置
├── AI_COLLABORATION_TEMPLATE.md # 完整模板說明
└── USAGE_GUIDE.md              # 詳細使用指南
```

**維護責任**: 項目維護者
**更新頻率**: 重大變更時
**觸發條件**: 項目結構變化、新策略發布

### 2. 項目知識庫 (.kiro/steering/)
```
├── product.md          # 產品概述和目標
├── tech.md            # 技術架構決策
├── methodology.md     # 開發方法論
├── trading_rules.md   # 量化交易規則
└── collaboration.md   # 協作規範
```

**維護責任**: strategy-analyst + architect
**更新頻率**: 每週檢查
**觸發條件**: 交易規則變更、監管要求更新

### 3. 策略規格文檔 (.kiro/specs/)
```
[strategy-name]/
├── spec.json           # 規格狀態追蹤
├── requirements.md     # BDD需求文檔
├── design.md          # DDD設計文檔
├── tasks.md           # 具體任務清單
├── backtest_results.md # 回測結果摘要
└── risk_assessment.md  # 風險評估報告
```

**維護責任**: 對應的Sub Agents
**更新頻率**: 實時更新
**觸發條件**: SDD流程推進、策略參數變更、風險指標變化

### 4. 技術文檔 (docs/)
```
├── quick_reference/     # 快速參考指南
│   ├── technical_indicators.md # 技術指標
│   ├── risk_management.md      # 風險管理
│   ├── api_endpoints.md        # API接口
│   └── settlement_rules.md     # 結算規則
├── collaboration/       # 協作流程文檔
├── checklists/         # 檢查清單
└── examples/           # 使用範例
```

**維護責任**: 相關專業Sub Agents
**更新頻率**: 根據市場變化和使用反饋
**觸發條件**: API變更、監管更新、策略調整

### 5. 風險管理文檔 (risk_management/)
```
├── risk_limits.md      # 風險限額設定
├── position_sizing.md  # 倉位管理規則  
├── stress_testing.md   # 壓力測試結果
├── compliance/         # 合規檢查記錄
└── audit_trail/        # 風險審計路徑
```

**維護責任**: risk-manager
**更新頻率**: 每日檢查，重大事件即時更新
**觸發條件**: 風險事件、監管變化、市場異常

## 🔄 文檔生命週期管理

### 1. 創建階段

#### 策略文檔自動生成機制
```bash
# SDD策略規格文檔自動創建
> /spec-init "rsi-momentum" "基於RSI的動量交易策略"
# 自動創建：
# - .kiro/specs/rsi-momentum/spec.json
# - .kiro/specs/rsi-momentum/requirements.md (模板)
# - .kiro/specs/rsi-momentum/design.md (模板)
# - .kiro/specs/rsi-momentum/tasks.md (模板)
# - .kiro/specs/rsi-momentum/risk_assessment.md (模板)
```

#### 策略文檔模板
```markdown
# [策略名稱] 需求分析

## 文檔信息
- **創建時間**: {timestamp}
- **負責Agent**: strategy-analyst
- **當前狀態**: requirements
- **最後更新**: {timestamp}
- **風險等級**: 待評估

## 策略概述
[待strategy-analyst填寫]

## 交易邏輯
### 進場條件
[BDD場景待生成]

### 出場條件
[BDD場景待生成]

### 風控措施
[待risk-manager評估]

## 市場適用性
[待分析]

## 預期表現
- **目標收益**: 待設定
- **最大回撤**: 待設定
- **夏普比率**: 待測試

---
📝 本文檔由量化交易AI協作模板自動生成
🔄 請保持與實際策略需求同步
⚠️ 所有交易邏輯必須包含風險管理措施
```

### 2. 維護階段

#### 自動同步觸發
```yaml
# .claude/settings.json 中的文檔同步Hook
"PostToolUse": [
  {
    "matcher": {
      "tools": ["EditTool", "WriteTool"]
    },
    "hooks": [
      {
        "type": "conditional",
        "condition": "file_path.contains('strategy') or file_path.contains('backtest')",
        "action": "command",
        "command": "python .claude/scheduler/strategy_doc_sync.py \"$file_path\""
      }
    ]
  }
]
```

#### 策略文檔同步檢查腳本
```python
#!/usr/bin/env python3
# .claude/scheduler/strategy_doc_sync.py

import sys
import os
import json
from datetime import datetime

def check_strategy_doc_sync(modified_file):
    """檢查修改的策略文件是否需要更新相關文檔"""
    
    print(f"🔄 策略文件 {modified_file} 已修改，檢查相關文檔同步...")
    
    # 檢查是否是策略核心文件
    if any(modified_file.startswith(path) for path in ['src/strategies/', 'src/domain/trading/']):
        
        # 查找相關策略規格文檔
        strategy_name = extract_strategy_name(modified_file)
        spec_path = f'.kiro/specs/{strategy_name}'
        
        if os.path.exists(spec_path):
            print(f"  📋 發現策略規格: {spec_path}")
            
            # 檢查風險評估是否需要更新
            risk_file = f'{spec_path}/risk_assessment.md'
            if os.path.exists(risk_file):
                risk_mtime = os.path.getmtime(risk_file)
                code_mtime = os.path.getmtime(modified_file)
                
                if code_mtime > risk_mtime:
                    print(f"  ⚠️ 風險評估文檔可能過期，建議更新")
                    print(f"     使用: > 請 risk-manager 重新評估 {strategy_name} 的風險")
            
            # 檢查回測結果
            backtest_file = f'{spec_path}/backtest_results.md'
            if os.path.exists(backtest_file):
                print(f"  📊 建議重新運行回測驗證策略變更")
                print(f"     使用: > 請對 {strategy_name} 運行增量回測")
            
            # 檢查API文檔
            if 'api' in modified_file.lower():
                print(f"  🔌 API變更檢測，相關文檔:")
                print(f"     - docs/quick_reference/api_endpoints.md")
                print(f"     - README.md (如果有公開API變更)")
        
        # 檢查技術指標文檔
        if any(indicator in modified_file.lower() for indicator in ['rsi', 'macd', 'bollinger', 'moving_average']):
            print(f"  📈 技術指標變更，檢查:")
            print(f"     - docs/quick_reference/technical_indicators.md")
        
        print(f"💡 建議使用: > 請檢查並更新 {strategy_name} 相關文檔")

def extract_strategy_name(file_path):
    """從文件路徑提取策略名稱"""
    # 簡化實現，實際應根據項目結構調整
    parts = file_path.split('/')
    for part in parts:
        if 'strategy' in part.lower() or 'trading' in part.lower():
            return part.replace('.py', '').replace('_strategy', '')
    return 'unknown'

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_strategy_doc_sync(sys.argv[1])
```

### 3. 版本控制

#### 策略文檔版本標記
```markdown
# RSI動量交叉策略 - 需求分析

**文檔版本**: v2.1.0
**最後更新**: 2024-01-27 15:30
**更新者**: strategy-analyst
**變更摘要**: 調整RSI參數範圍，添加成交量確認

## 版本歷史
- v2.1.0 (2024-01-27): 調整RSI參數範圍，添加成交量確認
- v2.0.0 (2024-01-25): 重大策略邏輯修改，更新止損機制
- v1.2.0 (2024-01-22): 添加多時間框架分析
- v1.1.0 (2024-01-20): 優化進場條件
- v1.0.0 (2024-01-15): 初始版本

## 策略參數變更記錄
- RSI週期: 14 → 21 (v2.1.0)
- 超買線: 70 → 75 (v2.1.0)
- 超賣線: 30 → 25 (v2.1.0)
- 成交量倍數: 新增 1.5x (v2.1.0)
```

#### Git提交關聯
```bash
# 策略文檔更新提交
git commit -m "docs(rsi-strategy): 更新RSI動量策略文檔 v2.1.0

策略參數調整:
- RSI週期調整為21，提高信號穩定性
- 調整超買超賣線至75/25，減少假信號
- 新增成交量確認，提高信號可靠性

風險影響評估:
- 預期交易頻率降低15%
- 信號準確率預期提升10%
- 最大回撤預期改善5%

關聯功能: src/strategies/rsi_momentum.py

strategy-analyst: 策略邏輯已驗證
risk-manager: 風險影響評估完成
data-engineer: 歷史數據回測準備就緒"

# 代碼和文檔同步提交
git commit -m "feat(rsi-strategy): 實現優化版RSI動量策略

代碼變更:
- 調整RSI計算週期至21
- 更新進場出場閾值
- 添加成交量確認邏輯
- 優化風控參數

文檔同步:
- 更新策略需求文檔 v2.1.0
- 同步技術設計文檔
- 更新API接口文檔
- 補充風險評估報告

回測結果:
- 夏普比率: 1.23 → 1.35
- 最大回撤: 8.5% → 7.2%
- 年化收益: 15.2% → 16.8%

Closes: #789
Docs-updated: rsi-momentum/requirements.md v2.1.0
Risk-assessed: 中等風險，符合投資組合要求"
```

## 📊 風險管理文檔特殊要求

### 1. 風險評估文檔
```markdown
# [策略名稱] 風險評估報告

## 評估信息
- **評估日期**: {timestamp}
- **評估者**: risk-manager
- **策略版本**: v1.0.0
- **評估有效期**: 30天

## 風險分類評估

### 市場風險
- **等級**: 中等
- **Beta值**: 0.75
- **相關性**: 與大盤相關性0.45
- **敏感度**: 利率敏感度低

### 流動性風險  
- **等級**: 低
- **標的池**: 大型股票，日均成交額>1億
- **持倉集中度**: 單一持倉<5%
- **平倉時間**: 預期<30分鐘

### 模型風險
- **等級**: 中等
- **模型複雜度**: 簡單技術指標組合
- **過擬合風險**: 低
- **參數穩定性**: 高

### 操作風險
- **等級**: 低
- **自動化程度**: 90%
- **人工干預點**: 僅風險事件
- **錯誤處理**: 完善

## 風控措施

### 倉位控制
- **單策略最大倉位**: 30%
- **單股最大權重**: 5%
- **行業集中度限制**: 單行業<20%

### 止損機制
- **固定止損**: -3%
- **追蹤止損**: 2%
- **時間止損**: 10個交易日
- **波動率止損**: 2倍ATR

### 風險限額
- **日內最大虧損**: 5%
- **月度最大回撤**: 10%
- **年度目標回撤**: <15%
- **VaR限額(95%)**: 2%

## 壓力測試

### 歷史情景
- **2008金融危機**: 最大回撤-12.3%
- **2020疫情崩盤**: 最大回撤-8.7%
- **2015股災**: 最大回撤-15.2%

### 假設情景
- **利率急升200bp**: 預期虧損-6%
- **市場波動率翻倍**: 預期虧損-8%
- **流動性枯竭**: 平倉時間延長至2小時

## 監控指標

### 實時監控
- **實時PnL**: 每秒更新
- **倉位監控**: 每分鐘檢查
- **風險指標**: 每5分鐘計算

### 每日報告
- **日度VaR**: 計算並記錄
- **夏普比率**: 滾動30日
- **最大回撤**: 實時更新

### 每週審查
- **策略表現分析**
- **風險限額使用率**
- **市場環境適應性**

---
⚠️ 本風險評估具有時效性，策略參數變更後需重新評估
📊 所有風險指標需與實際交易表現持續對比驗證
🔔 超過風險限額時自動觸發警報和強制平倉
```

### 2. 回測結果文檔
```markdown
# [策略名稱] 回測結果報告

## 回測配置
- **回測期間**: 2020-01-01 至 2023-12-31
- **初始資金**: 1,000,000
- **基準指數**: 滬深300
- **交易成本**: 0.1%
- **滑點假設**: 0.05%

## 核心表現指標

### 收益指標
- **總收益率**: 67.8%
- **年化收益率**: 18.9%
- **基準收益率**: 23.4%
- **超額收益**: -4.5%
- **信息比率**: -0.23

### 風險指標
- **最大回撤**: -12.3%
- **年化波動率**: 16.8%
- **夏普比率**: 1.12
- **卡爾瑪比率**: 1.54
- **索提諾比率**: 1.68

### 交易統計
- **總交易次數**: 1,247
- **勝率**: 56.7%
- **平均持倉期**: 5.3天
- **盈虧比**: 1.34
- **最大連續虧損**: 8次

## 月度表現分析

### 最佳月份
- **2021年3月**: +8.9%
- **2020年7月**: +7.2%  
- **2022年11月**: +6.8%

### 最差月份
- **2022年4月**: -9.2%
- **2020年3月**: -8.1%
- **2021年9月**: -6.7%

### 月度勝率
- **總體月度勝率**: 65.3%
- **牛市月度勝率**: 78.9%
- **熊市月度勝率**: 45.2%

## 市場環境分析

### 不同市場表現
```
市場狀態    | 收益率 | 夏普比率 | 最大回撤
-----------|--------|----------|----------
牛市       | 24.3%  | 1.67     | -6.2%
熊市       | -2.1%  | 0.15     | -12.3%
震蕩市場   | 8.7%   | 1.02     | -8.9%
```

### 行業暴露分析
- **金融**: 23.4%平均權重，15.6%收益貢獻
- **科技**: 18.9%平均權重，28.2%收益貢獻
- **消費**: 16.7%平均權重，12.3%收益貢獻

## 風險分解

### 收益歸因
- **選股能力**: +2.3%
- **時機選擇**: -1.8%
- **行業配置**: +0.7%
- **交易成本**: -1.1%

### 風險歸因
- **市場風險**: 67.8%
- **行業風險**: 18.9%
- **個股風險**: 13.3%

## 改進建議

### 策略優化
1. **降低熊市暴露**: 考慮添加宏觀經濟指標過濾
2. **提高時機選擇**: 優化進場出場時點
3. **成本控制**: 降低交易頻率，減少成本

### 風險管理
1. **動態止損**: 考慮基於波動率的動態止損
2. **倉位管理**: 根據市場環境調整倉位大小
3. **相關性控制**: 加強持倉間相關性監控

---
📊 回測結果僅供參考，實際交易可能存在差異
🔄 建議每季度重新回測，驗證策略有效性
⚠️ 策略參數變更後必須重新進行回測驗證
```

## 🤖 Sub Agent文檔責任分工

### strategy-analyst
**負責文檔**:
- `.kiro/specs/*/requirements.md`
- `docs/examples/trading_scenarios.md`
- 策略邏輯和業務流程文檔

**維護任務**:
- 確保BDD場景準確反映交易邏輯
- 更新策略需求變更
- 維護交易規則的可追溯性

### risk-manager  
**負責文檔**:
- `.kiro/specs/*/risk_assessment.md`
- `risk_management/`目錄下所有文檔
- `docs/quick_reference/risk_management.md`

**維護任務**:
- 實時更新風險評估報告
- 維護風險限額和監控規則
- 記錄風險事件和處理措施

### data-engineer
**負責文檔**:
- 數據清洗和特徵工程文檔
- `docs/quick_reference/technical_indicators.md`
- 回測數據品質報告

**維護任務**:
- 文檔化數據處理邏輯
- 更新技術指標計算方法
- 維護數據來源和品質說明

### api-specialist
**負責文檔**:
- API集成文檔
- `docs/quick_reference/api_endpoints.md`
- 錯誤處理和限流文檔

**維護任務**:
- 保持API文檔與實現同步
- 更新券商API變更影響
- 維護錯誤碼和響應格式文檔

### test-engineer
**負責文檔**:
- 測試策略文檔
- 回測和測試用例文檔
- `docs/checklists/`相關內容

**維護任務**:
- 更新測試覆蓋率報告
- 維護測試環境設置文檔
- 記錄測試最佳實踐

## 📈 量化交易文檔指標追蹤

### 關鍵指標
```python
# 量化文檔指標腳本
#!/usr/bin/env python3
# scripts/quant_doc_metrics.py

def calculate_quant_doc_metrics():
    """計算量化交易文檔相關指標"""
    
    metrics = {
        'total_strategies': 0,
        'risk_assessed_strategies': 0,
        'backtested_strategies': 0,
        'outdated_docs': 0,
        'missing_risk_docs': 0,
        'avg_backtest_age_days': 0
    }
    
    # 統計策略總數
    strategy_dirs = [d for d in os.listdir('.kiro/specs/') 
                    if os.path.isdir(f'.kiro/specs/{d}')]
    metrics['total_strategies'] = len(strategy_dirs)
    
    # 計算風險評估覆蓋率
    risk_assessed = 0
    backtested = 0
    
    for strategy_dir in strategy_dirs:
        strategy_path = f'.kiro/specs/{strategy_dir}'
        
        # 檢查風險評估
        risk_file = f'{strategy_path}/risk_assessment.md'
        if os.path.exists(risk_file):
            risk_assessed += 1
        
        # 檢查回測結果
        backtest_file = f'{strategy_path}/backtest_results.md'
        if os.path.exists(backtest_file):
            backtested += 1
    
    metrics['risk_assessed_strategies'] = risk_assessed
    metrics['backtested_strategies'] = backtested
    
    # 計算覆蓋率
    if strategy_dirs:
        metrics['risk_assessment_coverage'] = (risk_assessed / len(strategy_dirs)) * 100
        metrics['backtest_coverage'] = (backtested / len(strategy_dirs)) * 100
    
    return metrics

if __name__ == "__main__":
    metrics = calculate_quant_doc_metrics()
    print("📊 量化交易文檔指標報告")
    print("=" * 30)
    for key, value in metrics.items():
        print(f"{key}: {value}")
```

### 改進目標
- 風險評估覆蓋率: > 100% (所有策略必須有風險評估)
- 回測覆蓋率: > 95%
- 文檔時效性: < 7天未更新的風險文檔 < 5%
- 策略文檔完整性: > 95%

這個量化交易文檔維護體系確保了：
- 📊 **完整的策略文檔追蹤**
- 🛡️ **強制性風險評估覆蓋**
- 🔄 **自動化同步機制**
- 📈 **量化的質量指標**
- ⚠️ **風險感知的文檔管理**