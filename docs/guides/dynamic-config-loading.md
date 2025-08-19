# 動態配置載入指南

## 概述

動態配置載入系統允許 Claude Code 根據任務類型和上下文自動載入相關配置，實現配置的層次化管理和智能選擇。

## 配置層次結構

```
優先級（高到低）：
1. Module-specific (./.claude.md)      # 模組級配置
2. Project-specific (./CLAUDE.md)      # 項目級配置  
3. Global (~/.claude/global.md)        # 全局級配置
```

## 配置繼承機制

### 繼承規則
```yaml
global.md:
  test_coverage: 60%
  
CLAUDE.md:
  test_coverage: 80%    # 覆蓋全局設置
  
module/.claude.md:
  test_coverage: 100%   # 覆蓋項目設置
```

### 合併策略
- **Replace**: 完全替換上級配置（默認）
- **Merge**: 合併對象和數組
- **Append**: 添加到現有列表
- **Prepend**: 插入到列表開頭

## 任務類型配置映射

### 根據任務自動載入
```javascript
const taskConfigs = {
  'ui-development': {
    load: ['ui-guidelines.md', 'component-patterns.md'],
    permissions: 'relaxed',
    review: 'automated'
  },
  
  'api-development': {
    load: ['api-standards.md', 'security-checklist.md'],
    permissions: 'standard',
    review: 'required'
  },
  
  'database-migration': {
    load: ['db-practices.md', 'migration-safety.md'],
    permissions: 'strict',
    review: 'mandatory'
  },
  
  'documentation': {
    load: ['doc-templates.md', 'writing-style.md'],
    permissions: 'relaxed',
    review: 'optional'
  }
};
```

## 實施配置驗證

### 配置驗證檢查
```python
# .claude/scripts/validate_config.py

def validate_configuration(config_path):
    """驗證配置文件的正確性"""
    
    checks = {
        'syntax': check_yaml_syntax,
        'schema': validate_against_schema,
        'conflicts': detect_conflicts,
        'completeness': check_required_fields
    }
    
    results = {}
    for check_name, check_func in checks.items():
        results[check_name] = check_func(config_path)
    
    return all(results.values()), results
```

### 配置架構定義
```yaml
# .claude/config-schema.yaml
type: object
required:
  - version
  - principles
properties:
  version:
    type: string
    pattern: '^\d+\.\d+\.\d+$'
  
  principles:
    type: object
    required:
      - safety
      - quality
    
  permissions:
    type: object
    properties:
      allowed:
        type: array
        items:
          type: string
      blocked:
        type: array
        items:
          type: string
  
  overrides:
    type: array
    items:
      type: object
      required:
        - setting
        - reason
        - scope
```

## 上下文感知載入

### 智能配置選擇
```python
def select_configuration(context):
    """根據上下文選擇配置"""
    
    # 分析當前任務
    task_type = analyze_task_type(context)
    file_location = get_file_location(context)
    risk_level = assess_risk_level(context)
    
    # 載入基礎配置
    config = load_global_config()
    
    # 層次化載入
    if project_config_exists():
        config = merge_configs(config, load_project_config())
    
    if module_config_exists(file_location):
        config = merge_configs(config, load_module_config(file_location))
    
    # 任務特定配置
    if task_type in task_specific_configs:
        config = merge_configs(config, task_specific_configs[task_type])
    
    # 風險調整
    if risk_level == 'high':
        config = apply_strict_mode(config)
    
    return config
```

### 配置快取機制
```python
class ConfigCache:
    """配置快取管理"""
    
    def __init__(self, ttl=3600):
        self.cache = {}
        self.ttl = ttl
    
    def get(self, key):
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry['timestamp'] < self.ttl:
                return entry['config']
        return None
    
    def set(self, key, config):
        self.cache[key] = {
            'config': config,
            'timestamp': time.time()
        }
    
    def invalidate(self, pattern=None):
        if pattern:
            # 使模式匹配的條目失效
            keys_to_remove = [k for k in self.cache if pattern in k]
            for key in keys_to_remove:
                del self.cache[key]
        else:
            # 清空整個快取
            self.cache.clear()
```

## 配置熱重載

### 文件監控
```python
import watchdog.observers
import watchdog.events

class ConfigWatcher(watchdog.events.FileSystemEventHandler):
    """監控配置文件變化"""
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
    
    def on_modified(self, event):
        if event.src_path.endswith('.md'):
            print(f"配置文件已更新: {event.src_path}")
            self.config_manager.reload_config(event.src_path)
    
    def start_watching(self, paths):
        observer = watchdog.observers.Observer()
        for path in paths:
            observer.schedule(self, path, recursive=True)
        observer.start()
        return observer
```

### 平滑過渡
```python
def reload_configuration(config_path):
    """平滑重載配置"""
    
    # 載入新配置
    new_config = load_config(config_path)
    
    # 驗證新配置
    is_valid, validation_results = validate_configuration(new_config)
    
    if not is_valid:
        log_error(f"配置驗證失敗: {validation_results}")
        return False
    
    # 備份當前配置
    backup_current_config()
    
    try:
        # 應用新配置
        apply_config(new_config)
        
        # 驗證應用結果
        if not verify_config_applied(new_config):
            rollback_config()
            return False
        
        # 清理快取
        config_cache.invalidate()
        
        log_info("配置重載成功")
        return True
        
    except Exception as e:
        log_error(f"配置重載失敗: {e}")
        rollback_config()
        return False
```

## 使用示例

### 1. 項目初始化
```bash
# 創建項目配置
cat > CLAUDE.md << EOF
# Project Configuration

## Override Global Settings
- test_coverage: 85%  # Higher than global 60%
- review_required: true  # All changes need review

## Project-Specific Rules
- framework: React
- style_guide: airbnb
- deployment: kubernetes
EOF
```

### 2. 模組配置
```bash
# 創建模組特定配置
cat > src/payments/.claude.md << EOF
# Payment Module Configuration

## Security Override
- review_level: strict
- test_coverage: 100%
- security_scan: mandatory

## Restricted Operations
- no_direct_db_access: true
- audit_all_changes: true
EOF
```

### 3. 任務觸發配置
```python
# 任務開始時
def on_task_start(task_description):
    # 分析任務類型
    task_type = classify_task(task_description)
    
    # 載入相應配置
    config = load_config_for_task(task_type)
    
    # 應用配置
    apply_task_config(config)
    
    # 記錄配置使用
    log_config_usage(task_type, config)
```

## 配置管理命令

### CLI 工具
```bash
# 查看當前配置
claude-config show

# 驗證配置
claude-config validate

# 查看配置層次
claude-config hierarchy

# 測試配置載入
claude-config test --task "create API endpoint"

# 清理配置快取
claude-config cache clear
```

## 故障排除

### 常見問題

#### 配置未生效
```bash
# 檢查配置優先級
claude-config hierarchy --verbose

# 查看實際載入的配置
claude-config debug --task "current"
```

#### 配置衝突
```bash
# 檢測配置衝突
claude-config conflicts

# 解決建議
claude-config resolve --interactive
```

#### 性能問題
```bash
# 分析配置載入時間
claude-config profile

# 優化建議
claude-config optimize
```

## 最佳實踐

### 1. 保持簡潔
- 全局配置：通用原則和標準
- 項目配置：項目特定需求
- 模組配置：僅必要的覆蓋

### 2. 文檔化覆蓋
```markdown
## Override Justification
Setting: test_coverage
Original: 60%
Override: 100%
Reason: Payment processing requires maximum reliability
```

### 3. 版本控制
- 將配置文件納入版本控制
- 記錄配置變更歷史
- 使用語義化版本號

### 4. 定期審查
- 月度：審查項目配置
- 季度：審查全局配置
- 年度：全面配置審計

---

*版本: 1.0.0*
*最後更新: 2025-01-19*