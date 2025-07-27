# AI協作開發模板使用指南

## 📁 模板結構

現在您有兩個乾淨的AI協作開發模板：

1. **`Quant_Project_Template/`** - 量化交易專用模板
2. **`General_Project_Template/`** - 通用項目模板

## 🚀 正確使用方式

### 創建新項目

```bash
# 方法1: 複製量化交易模板
cp -r Quant_Project_Template ~/my-trading-strategy
cd ~/my-trading-strategy
./setup.sh

# 方法2: 複製通用模板
cp -r General_Project_Template ~/my-web-app
cd ~/my-web-app
./setup.sh

# 方法3: 直接在當前目錄使用
cd /path/to/your/project
cp -r /Users/chenpowen/Python\ Projects/claude/General_Project_Template/* .
./setup.sh
```

### setup.sh 會創建的文件

✅ **這些文件應該在新項目中創建**：
- `.gitignore` - Git忽略規則
- `.kiro/steering/*.md` - 項目知識庫文檔
- `src/domain/__init__.py` - Python模組初始化
- `tests/test_example.py` - 示例測試文件
- 各種配置和文檔文件

## 🎯 模板特色對比

| 特性 | 量化交易模板 | 通用模板 |
|------|-------------|----------|
| **適用場景** | 量化交易、金融分析 | Web應用、工具、遊戲等 |
| **Sub Agents** | strategy-analyst, risk-manager, data-engineer, api-specialist, test-engineer | business-analyst, architect, data-specialist, integration-specialist, test-engineer |
| **專業檢查** | 風控檢查、止損驗證 | 代碼品質、安全檢查 |
| **示例文檔** | RSI策略、風險管理 | API設計、設計模式 |

## 📋 開始使用流程

1. **複製模板到新目錄**
2. **運行 `./setup.sh`** 創建項目結構
3. **運行 `./test_setup.sh`** 驗證環境
4. **啟動 `claude-code`** 開始AI協作
5. **使用 `/spec-init [功能名稱] [描述]`** 創建第一個功能

## ⚠️ 重要提醒

- **模板目錄保持乾淨**：不要直接在模板目錄中運行 setup.sh
- **每個新項目都複製一份**：確保模板可重複使用
- **setup.sh 是設計好的**：會創建標準項目文件，這是正常的

## 🔧 維護模板

如需更新模板：
1. 修改模板目錄中的配置文件
2. 測試更新後的 setup.sh
3. 確保模板目錄保持乾淨狀態

---

現在您的模板已經準備就緒，可以開始創建各種AI協作項目了！🎉