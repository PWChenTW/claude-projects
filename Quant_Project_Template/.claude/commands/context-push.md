# /context-push - 推入新上下文

## 用途
將新的上下文信息推入工作記憶，幫助 AI 理解當前任務背景和需求變化。

## 語法
```
/context-push [context-type] "[context-content]"
```

### 參數
- `context-type`: 上下文類型
  - `requirement`: 新需求或需求變更
  - `constraint`: 新限制或約束條件
  - `decision`: 重要決策或方向調整
  - `discovery`: 新發現或重要信息
  - `priority`: 優先級變更
- `context-content`: 上下文內容描述

## 執行流程

### 1. 驗證上下文
```python
def validate_context(context_type, content):
    """驗證上下文的有效性和相關性"""
    
    # 檢查類型
    if context_type not in VALID_CONTEXT_TYPES:
        raise ValueError(f"Invalid context type: {context_type}")
    
    # 檢查內容
    if len(content) < 10:
        raise ValueError("Context content too short")
    
    if len(content) > 1000:
        raise ValueError("Context content too long, please summarize")
    
    # 檢查重複
    if is_duplicate_context(content):
        raise ValueError("Similar context already exists")
    
    return True
```

### 2. 處理上下文
```python
def process_context(context_type, content):
    """處理並分類上下文"""
    
    context = {
        'id': generate_context_id(),
        'type': context_type,
        'content': content,
        'timestamp': datetime.now().isoformat(),
        'impact': assess_impact(content),
        'related': find_related_contexts(content)
    }
    
    # 根據類型處理
    if context_type == 'requirement':
        update_requirements(context)
    elif context_type == 'constraint':
        update_constraints(context)
    elif context_type == 'decision':
        record_decision(context)
    
    return context
```

### 3. 更新工作記憶
```python
def update_working_memory(context):
    """更新當前工作記憶"""
    
    # 更新 current.md
    update_current_context(context)
    
    # 更新 session memory
    add_to_session_memory(context)
    
    # 觸發相關動作
    trigger_context_actions(context)
```

## 上下文格式

### Requirement Context
```markdown
## 新需求 [REQ-001]
時間: 2025-01-19 14:30
影響: 高

### 內容
用戶要求添加批量導入功能

### 影響分析
- 需要新的 API 端點
- 需要文件解析邏輯
- 需要進度顯示界面

### 相關任務
- [ ] 設計文件格式
- [ ] 實現解析器
- [ ] 創建 UI 組件
```

### Constraint Context
```markdown
## 新約束 [CON-001]
時間: 2025-01-19 14:30
類型: 技術限制

### 內容
必須支持 IE11 瀏覽器

### 影響
- 不能使用 ES6+ 語法
- 需要 polyfills
- 需要額外測試

### 調整方案
1. 使用 Babel 轉譯
2. 添加必要的 polyfills
3. 設置 IE11 測試環境
```

### Decision Context
```markdown
## 決策記錄 [DEC-001]
時間: 2025-01-19 14:30
決策者: Team Lead

### 決策
採用 PostgreSQL 替代 MySQL

### 理由
1. 更好的 JSON 支持
2. 更強的並發處理
3. 更豐富的數據類型

### 影響
- 需要遷移現有數據
- 需要更新 ORM 配置
- 需要團隊培訓
```

## 上下文棧管理

### 推入規則
```python
CONTEXT_STACK = []
MAX_STACK_SIZE = 10

def push_context(context):
    global CONTEXT_STACK
    
    # 添加到棧頂
    CONTEXT_STACK.insert(0, context)
    
    # 維護棧大小
    if len(CONTEXT_STACK) > MAX_STACK_SIZE:
        archived = CONTEXT_STACK.pop()
        archive_context(archived)
    
    # 重新計算優先級
    recalculate_priorities()
```

### 上下文優先級
```python
def calculate_priority(context):
    """計算上下文優先級"""
    
    score = 0
    
    # 類型權重
    type_weights = {
        'requirement': 5,
        'constraint': 4,
        'decision': 3,
        'discovery': 2,
        'priority': 1
    }
    score += type_weights.get(context['type'], 0)
    
    # 時間衰減
    age = time_since(context['timestamp'])
    score -= age / 3600  # 每小時減1分
    
    # 影響範圍
    score += context['impact'] * 2
    
    return max(0, score)
```

## 智能關聯

### 關聯檢測
```python
def find_related_contexts(new_context):
    """找出相關的上下文"""
    
    related = []
    
    for existing in CONTEXT_STACK:
        similarity = calculate_similarity(new_context, existing)
        
        if similarity > 0.7:
            related.append({
                'id': existing['id'],
                'similarity': similarity,
                'type': existing['type']
            })
    
    return sorted(related, key=lambda x: x['similarity'], reverse=True)
```

### 衝突檢測
```python
def detect_conflicts(new_context):
    """檢測上下文衝突"""
    
    conflicts = []
    
    for existing in CONTEXT_STACK:
        if is_conflicting(new_context, existing):
            conflicts.append({
                'with': existing['id'],
                'reason': analyze_conflict(new_context, existing),
                'resolution': suggest_resolution(new_context, existing)
            })
    
    return conflicts
```

## 使用場景

### 1. 需求變更
```bash
/context-push requirement "Add export to PDF functionality"
# AI acknowledges and adjusts plan
```

### 2. 發現限制
```bash
/context-push constraint "Database queries must complete within 100ms"
# AI considers performance in implementation
```

### 3. 技術決策
```bash
/context-push decision "Use React Query for data fetching instead of Redux"
# AI updates implementation approach
```

### 4. 新發現
```bash
/context-push discovery "Found existing utility function for date formatting"
# AI reuses existing code
```

## 自動上下文推送

### 觸發規則
```python
AUTO_PUSH_TRIGGERS = {
    'test_failure': {
        'condition': lambda: test_failed(),
        'action': lambda: push_context('constraint', get_test_failure_details())
    },
    'performance_issue': {
        'condition': lambda: response_time() > 1000,
        'action': lambda: push_context('discovery', get_performance_metrics())
    },
    'security_warning': {
        'condition': lambda: security_scan_failed(),
        'action': lambda: push_context('constraint', get_security_issues())
    }
}
```

## 上下文查詢

### 查看當前棧
```bash
/context-stack
# Shows current context stack with priorities
```

### 搜索歷史
```bash
/context-search "payment"
# Finds all contexts related to payment
```

### 清理過期
```bash
/context-clean --older-than 1h
# Removes contexts older than 1 hour
```

## 最佳實踐

### Do's ✅
- 及時推送重要變更
- 使用清晰的描述
- 標記影響範圍
- 關聯相關任務

### Don'ts ❌
- 不要推送瑣碎信息
- 不要重複推送
- 不要忽略衝突警告
- 不要超過長度限制

## 與其他命令集成

### 與記憶系統
```bash
# 推送上下文並保存狀態
/context-push decision "Switch to TypeScript"
/memory-save checkpoint "After TypeScript decision"
```

### 與任務管理
```bash
# 推送新需求並分解任務
/context-push requirement "Add user notifications"
/task-split "user-notifications"
```

---

*命令版本: 1.0.0*
*最後更新: 2025-01-19*