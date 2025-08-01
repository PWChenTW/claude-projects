# 核心開發原則 (所有 Sub Agents 必須遵守)

## 🎯 MVP 優先原則

### 第一原則：從簡單開始
- **最小可行方案**：永遠選擇能解決問題的最簡單方案
- **推遲複雜決策**：不確定的設計留到真正需要時
- **快速驗證**：盡快讓功能運行並獲得反饋
- **避免過度工程**：不要為了「可能的未來需求」而設計

### 第二原則：漸進式改進
- **第一版只需要**：核心功能、基本架構、簡單實現
- **第二版再考慮**：性能優化、擴展性、設計模式
- **第三版才需要**：高級特性、自動化、複雜集成

### 第三原則：批判性思考
- **質疑需求**：這真的是必要的嗎？有更簡單的方案嗎？
- **挑戰假設**：不要盲目接受，要驗證假設
- **提供替代**：如果有更好的方案，主動提出
- **誠實反饋**：發現問題直接指出，不要迴避

### 第四原則：實用主義
- **YAGNI**：You Aren't Gonna Need It - 只做當前需要的
- **KISS**：Keep It Simple, Stupid - 簡單就是美
- **夠用就好**：不追求技術完美，追求業務價值
- **快速交付**：可用的產品勝過完美的計劃

## ⚠️ 避免的陷阱

### 技術陷阱
- ❌ 過度抽象和設計模式濫用
- ❌ 過早的性能優化
- ❌ 不必要的技術堆疊
- ❌ 為了用新技術而用新技術

### 需求陷阱
- ❌ 範圍蔓延 - 不斷加入新功能
- ❌ 完美主義 - 追求 100% 而非 80%
- ❌ 過度規劃 - 計劃太遠的未來
- ❌ 忽視反饋 - 不聽用戶的聲音

## 💡 實踐建議

### 開始前問自己
1. 這是解決核心問題的最簡單方案嗎？
2. 能在一週內完成第一版嗎？
3. 用戶真的需要這個功能嗎？
4. 有沒有現成的解決方案？

### 實施時提醒自己
1. 保持簡單，拒絕複雜
2. 快速迭代，持續改進
3. 關注價值，而非技術
4. 聽取反饋，靈活調整

### 完成後檢查
1. 代碼是否容易理解？
2. 功能是否真的可用？
3. 是否解決了核心問題？
4. 下一步改進方向是什麼？

## 🚀 記住

> "過早的優化是萬惡之源" - Donald Knuth

> "完美是良好的敵人" - 伏爾泰

> "簡單是可靠的先決條件" - Edsger W. Dijkstra

**我們的目標**：快速交付可用的產品，通過真實反饋持續改進，而不是一開始就追求完美。