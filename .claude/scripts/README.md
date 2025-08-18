# 記憶管理系統使用指南

## 概述

記憶管理系統提供了完整的知識持久化和管理功能，包括同步、備份、查詢和清理。

## 🚀 快速開始

### 初始設置
```bash
# 設置自動更新機制
python .claude/scripts/memory_auto_update.py setup

# 檢查系統狀態
python .claude/scripts/memory_auto_update.py status
```

## 📚 腳本功能

### 1. memory_sync.py - 記憶同步
同步各種來源的信息到記憶系統。

```bash
# 同步所有內容
python .claude/scripts/memory_sync.py --type all

# 只同步進度
python .claude/scripts/memory_sync.py --type progress

# 只同步研究文檔
python .claude/scripts/memory_sync.py --type research

# 只同步決策記錄
python .claude/scripts/memory_sync.py --type decisions

# 只同步規格狀態
python .claude/scripts/memory_sync.py --type specs
```

### 2. memory_backup.py - 記憶備份
創建和管理記憶系統備份。

```bash
# 創建備份
python .claude/scripts/memory_backup.py backup

# 創建命名備份
python .claude/scripts/memory_backup.py backup --name "重要里程碑"

# 列出所有備份
python .claude/scripts/memory_backup.py list

# 恢復備份
python .claude/scripts/memory_backup.py restore --name memory_backup_20250118_120000

# 自動備份（保留最近7個）
python .claude/scripts/memory_backup.py auto --max-backups 7

# 導出記憶為可讀格式
python .claude/scripts/memory_backup.py export --target ./memory_export
```

### 3. memory_query.py - 記憶查詢
搜索和查詢記憶系統內容。

```bash
# 搜索關鍵詞
python .claude/scripts/memory_query.py search "EPE"
python .claude/scripts/memory_query.py search "決策" --memory-type project

# 查詢進度
python .claude/scripts/memory_query.py progress

# 查詢決策記錄
python .claude/scripts/memory_query.py decisions

# 查詢最近研究
python .claude/scripts/memory_query.py research --days 7

# 查詢規格狀態
python .claude/scripts/memory_query.py specs

# 生成記憶地圖
python .claude/scripts/memory_query.py map

# 智能查詢（自動判斷類型）
python .claude/scripts/memory_query.py smart "最近的進度如何"
```

### 4. memory_cleanup.py - 記憶清理
清理和優化記憶系統空間。

```bash
# 清理會話記憶（歸檔）
python .claude/scripts/memory_cleanup.py session

# 清理舊研究文檔（超過30天）
python .claude/scripts/memory_cleanup.py research --days 30

# 清理重複決策記錄
python .claude/scripts/memory_cleanup.py duplicates

# 清理空目錄
python .claude/scripts/memory_cleanup.py empty

# 分析記憶使用情況
python .claude/scripts/memory_cleanup.py analyze

# 自動清理（智能模式）
python .claude/scripts/memory_cleanup.py auto

# 直接刪除而不歸檔
python .claude/scripts/memory_cleanup.py session --no-archive
```

### 5. memory_auto_update.py - 自動更新系統
整合所有功能，提供自動化更新。

```bash
# 設置自動更新
python .claude/scripts/memory_auto_update.py setup

# 檢查狀態
python .claude/scripts/memory_auto_update.py status

# 手動觸發各種更新
python .claude/scripts/memory_auto_update.py task --task "功能完成"
python .claude/scripts/memory_auto_update.py spec-init --feature "新功能"
python .claude/scripts/memory_auto_update.py git-commit
python .claude/scripts/memory_auto_update.py daily-cleanup
python .claude/scripts/memory_auto_update.py session-end

# 測試自動更新系統
python .claude/scripts/memory_auto_update.py test
```

## 🔄 自動化工作流程

### Hook 觸發點

1. **任務完成時**
   - 同步進度狀態
   - 同步研究文檔
   - 創建任務快照

2. **規格初始化時**
   - 同步規格狀態
   - 記錄到會話記憶

3. **Git 提交時**
   - 全面同步記憶
   - 自動備份

4. **每日維護**（建議 2:00 AM）
   - 清理舊研究文檔
   - 清理空目錄
   - 分析使用情況

5. **會話結束時**
   - 最終同步
   - 清理會話記憶
   - 生成記憶報告

### 配置文件

配置保存在 `.claude/settings.json`：

```json
{
  "hooks": {
    "post-task": "python .claude/scripts/memory_auto_update.py task",
    "post-spec-init": "python .claude/scripts/memory_auto_update.py spec-init",
    "pre-session-end": "python .claude/scripts/memory_auto_update.py session-end"
  },
  "memory": {
    "auto_sync": true,
    "auto_backup": true,
    "backup_retention": 7,
    "research_retention_days": 30
  }
}
```

## 📊 記憶系統結構

```
.kiro/memory/
├── global/           # 跨專案持久知識
│   ├── decisions_*.md
│   └── learnings.md
├── project/          # 當前專案記憶
│   ├── enhancement-progress.md
│   ├── decisions.md
│   ├── progress_summary.json
│   └── memory_report.md
└── session/          # 當前會話臨時記憶
    ├── research_findings.json
    ├── specs_status.json
    └── active_specs.json
```

## 🛠️ 故障排除

### 常見問題

**Q: 腳本執行失敗**
```bash
# 確保 Python 路徑正確
which python3
# 更新腳本中的 shebang 行
```

**Q: 權限錯誤**
```bash
# 給腳本添加執行權限
chmod +x .claude/scripts/*.py
```

**Q: 記憶系統空間不足**
```bash
# 執行深度清理
python .claude/scripts/memory_cleanup.py auto --no-archive
```

**Q: 備份恢復失敗**
```bash
# 檢查備份完整性
tar -tzf .kiro/backups/memory_backup_*.tar.gz
```

## 📈 最佳實踐

1. **定期備份**
   - 每日自動備份
   - 重要里程碑手動備份

2. **及時清理**
   - 會話結束清理臨時記憶
   - 每月清理舊研究文檔

3. **有效查詢**
   - 使用智能查詢節省時間
   - 定期生成記憶地圖了解全局

4. **監控使用**
   - 每週分析記憶使用情況
   - 及時清理大文件和舊文件

## 🔗 相關文檔

- [EPE 工作流程](../../docs/guides/explore-plan-execute-workflow.md)
- [SDD 整合指南](../../docs/guides/epe-sdd-integration-guide.md)
- [專案記憶結構](../../.kiro/memory/README.md)

## 📝 版本記錄

- **v1.0.0** (2025-01-18)
  - 初始版本發布
  - 完整的 CRUD 功能
  - 自動化機制實施

---

如有問題或建議，請更新此文檔。