# /memory-save - 保存當前狀態

## 用途
快速保存當前工作狀態到記憶系統，便於後續恢復或參考。

## 語法
```
/memory-save [type] [description]
```

### 參數
- `type`: 保存類型 (snapshot|checkpoint|milestone)
  - `snapshot`: 快速快照，自動過期
  - `checkpoint`: 檢查點，保留7天
  - `milestone`: 里程碑，永久保存
- `description`: 狀態描述

## 執行流程

### 1. 收集當前狀態
```python
def collect_current_state():
    state = {
        'timestamp': datetime.now().isoformat(),
        'branch': get_current_branch(),
        'uncommitted_changes': get_uncommitted_changes(),
        'active_tasks': get_active_todos(),
        'recent_files': get_recently_modified_files(),
        'session_notes': read_session_notes()
    }
    return state
```

### 2. 分類保存
```python
def save_by_type(state, save_type, description):
    if save_type == 'snapshot':
        path = f".kiro/memory/session/snapshots/{timestamp}.json"
        ttl = 24 * 3600  # 24 hours
    elif save_type == 'checkpoint':
        path = f".kiro/memory/project/checkpoints/{timestamp}.json"
        ttl = 7 * 24 * 3600  # 7 days
    elif save_type == 'milestone':
        path = f".kiro/memory/project/milestones/{timestamp}.json"
        ttl = None  # Permanent
    
    save_state(path, state, ttl)
```

### 3. 生成恢復指令
```python
def generate_restore_command(save_id):
    return f"""
    # To restore this state:
    /memory-load {save_id}
    
    # To view without restoring:
    /memory-view {save_id}
    """
```

## 保存格式

### Snapshot (JSON)
```json
{
  "id": "snap-20250119-143022",
  "type": "snapshot",
  "description": "Before refactoring auth module",
  "timestamp": "2025-01-19T14:30:22",
  "state": {
    "branch": "feature/auth-refactor",
    "files_modified": ["src/auth.js", "tests/auth.test.js"],
    "todos": ["Refactor auth", "Update tests"],
    "notes": "Consider OAuth integration"
  },
  "ttl": 86400
}
```

### Checkpoint (Markdown + JSON)
```markdown
# Checkpoint: auth-refactor-phase1
Date: 2025-01-19 14:30:22
Branch: feature/auth-refactor

## Progress
- ✅ Separated auth logic
- ✅ Created auth service
- ⏳ Writing tests

## Decisions
- Use JWT for tokens
- 24-hour token expiry
- Redis for session storage

## Next Steps
1. Complete unit tests
2. Integration tests
3. Documentation

---
[Full state in checkpoint-12345.json]
```

### Milestone (Complete Archive)
```
milestones/
├── 2025-01-19-auth-complete/
│   ├── summary.md
│   ├── state.json
│   ├── decisions.md
│   ├── code-snippets/
│   └── test-results/
```

## 使用場景

### 1. 開始複雜任務前
```bash
/memory-save checkpoint "Before starting payment integration"
# Output: Checkpoint saved as 'check-20250119-143022'
```

### 2. 完成重要功能後
```bash
/memory-save milestone "Authentication system complete"
# Output: Milestone saved as 'mile-20250119-143022'
```

### 3. 臨時中斷工作
```bash
/memory-save snapshot "Lunch break"
# Output: Snapshot saved as 'snap-20250119-143022'
```

## 自動保存規則

### 觸發條件
- 每小時自動快照
- 重大文件修改後
- 測試全部通過時
- Git commit 前

### 保存策略
```python
AUTO_SAVE_RULES = {
    'hourly': {
        'type': 'snapshot',
        'condition': lambda: time_since_last_save() > 3600
    },
    'major_change': {
        'type': 'checkpoint',
        'condition': lambda: files_changed_count() > 10
    },
    'tests_pass': {
        'type': 'checkpoint',
        'condition': lambda: all_tests_passing()
    },
    'pre_commit': {
        'type': 'checkpoint',
        'condition': lambda: git_staging_area_not_empty()
    }
}
```

## 整合其他命令

### 與 /memory-load 配合
```bash
# 保存當前狀態
/memory-save checkpoint "Feature half done"
# Returns: check-12345

# 稍後恢復
/memory-load check-12345
```

### 與 /context-push 配合
```bash
# 保存並推送上下文
/memory-save checkpoint "Ready for review"
/context-push "Please review auth changes"
```

## 清理策略

### 自動清理
- Snapshots: 24小時後
- Checkpoints: 7天後（除非標記為重要）
- Milestones: 永不自動刪除

### 手動清理
```bash
# 清理過期快照
/memory-clean snapshots

# 清理舊檢查點
/memory-clean checkpoints --older-than 7d

# 查看空間使用
/memory-usage
```

## 錯誤處理

### 常見錯誤
```python
ERROR_HANDLERS = {
    'disk_full': "清理舊快照或增加存儲空間",
    'invalid_type': "使用 snapshot、checkpoint 或 milestone",
    'save_failed': "檢查文件權限和路徑",
    'duplicate_id': "自動生成新ID並重試"
}
```

## 最佳實踐

### Do's ✅
- 在開始複雜任務前保存
- 使用描述性的說明
- 定期清理舊快照
- 為重要節點創建里程碑

### Don'ts ❌
- 不要保存敏感信息
- 不要依賴快照超過24小時
- 不要忽略清理提醒
- 不要覆蓋里程碑

---

*命令版本: 1.0.0*
*最後更新: 2025-01-19*