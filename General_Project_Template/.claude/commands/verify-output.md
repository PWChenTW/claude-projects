# /verify-output - 驗證輸出

## 用途
全面驗證 AI 生成的代碼和輸出，確保質量、安全性和符合規範。

## 語法
```
/verify-output [target] [options]
```

### 參數
- `target`: 驗證目標
  - `last`: 最近生成的輸出
  - `file:<path>`: 特定文件
  - `pr`: 當前 PR 的所有更改
  - `feature:<name>`: 特定功能的所有文件
- `options`:
  - `--level`: 驗證級別 (basic|standard|strict)
  - `--fix`: 自動修復發現的問題
  - `--report`: 生成詳細報告

## 驗證層級

### Basic (葉節點)
```python
BASIC_CHECKS = {
    'syntax': check_syntax_errors,
    'lint': run_linter,
    'format': check_formatting,
    'imports': verify_imports
}
```

### Standard (邊界層)
```python
STANDARD_CHECKS = {
    **BASIC_CHECKS,
    'types': run_type_checker,
    'tests': run_unit_tests,
    'coverage': check_test_coverage,
    'complexity': analyze_complexity
}
```

### Strict (核心架構)
```python
STRICT_CHECKS = {
    **STANDARD_CHECKS,
    'security': run_security_scan,
    'performance': run_performance_tests,
    'integration': run_integration_tests,
    'accessibility': check_accessibility,
    'documentation': verify_documentation
}
```

## 驗證流程

### 1. 預檢查
```python
def pre_verification(target):
    """驗證前的準備工作"""
    
    # 確定驗證範圍
    files = identify_files(target)
    
    # 確定驗證級別
    level = determine_verification_level(files)
    
    # 載入配置
    config = load_verification_config(level)
    
    # 創建快照
    snapshot = create_snapshot(files)
    
    return {
        'files': files,
        'level': level,
        'config': config,
        'snapshot': snapshot
    }
```

### 2. 執行驗證
```python
def execute_verification(context):
    """執行驗證檢查"""
    
    results = {}
    
    for check_name, check_func in context['config']['checks'].items():
        try:
            result = check_func(context['files'])
            results[check_name] = {
                'status': 'passed' if result['success'] else 'failed',
                'details': result['details'],
                'severity': result.get('severity', 'info')
            }
        except Exception as e:
            results[check_name] = {
                'status': 'error',
                'details': str(e),
                'severity': 'critical'
            }
    
    return results
```

### 3. 分析結果
```python
def analyze_results(results):
    """分析驗證結果"""
    
    analysis = {
        'total_checks': len(results),
        'passed': sum(1 for r in results.values() if r['status'] == 'passed'),
        'failed': sum(1 for r in results.values() if r['status'] == 'failed'),
        'errors': sum(1 for r in results.values() if r['status'] == 'error'),
        'critical_issues': [],
        'warnings': [],
        'suggestions': []
    }
    
    for check, result in results.items():
        if result['severity'] == 'critical':
            analysis['critical_issues'].append({
                'check': check,
                'details': result['details']
            })
        elif result['severity'] == 'warning':
            analysis['warnings'].append({
                'check': check,
                'details': result['details']
            })
    
    # 生成建議
    analysis['suggestions'] = generate_suggestions(results)
    
    return analysis
```

## 驗證項目詳解

### 代碼質量
```python
def check_code_quality(files):
    """檢查代碼質量"""
    
    metrics = {
        'complexity': [],
        'duplication': [],
        'maintainability': []
    }
    
    for file in files:
        # 圈複雜度
        complexity = calculate_cyclomatic_complexity(file)
        if complexity > 10:
            metrics['complexity'].append({
                'file': file,
                'value': complexity,
                'threshold': 10
            })
        
        # 代碼重複
        duplication = detect_duplication(file)
        if duplication > 0.1:  # 10%
            metrics['duplication'].append({
                'file': file,
                'percentage': duplication * 100
            })
        
        # 可維護性指數
        maintainability = calculate_maintainability_index(file)
        if maintainability < 60:
            metrics['maintainability'].append({
                'file': file,
                'score': maintainability,
                'threshold': 60
            })
    
    return {
        'success': all(len(v) == 0 for v in metrics.values()),
        'details': metrics,
        'severity': 'warning'
    }
```

### 安全檢查
```python
def security_scan(files):
    """安全漏洞掃描"""
    
    vulnerabilities = []
    
    patterns = {
        'sql_injection': r'query\s*\(\s*["\'].*\+.*["\']',
        'xss': r'innerHTML\s*=\s*[^\'"]',
        'hardcoded_secrets': r'(api_key|password|secret)\s*=\s*["\'][^"\']+["\']',
        'weak_crypto': r'md5|sha1',
        'eval_usage': r'\beval\s*\('
    }
    
    for file in files:
        content = read_file(file)
        
        for vuln_type, pattern in patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                vulnerabilities.append({
                    'file': file,
                    'type': vuln_type,
                    'matches': matches,
                    'severity': get_severity(vuln_type)
                })
    
    return {
        'success': len(vulnerabilities) == 0,
        'details': vulnerabilities,
        'severity': 'critical' if vulnerabilities else 'info'
    }
```

### 性能分析
```python
def performance_analysis(files):
    """性能分析"""
    
    issues = []
    
    for file in files:
        # 大O複雜度分析
        complexity_issues = analyze_time_complexity(file)
        
        # 內存使用分析
        memory_issues = analyze_memory_usage(file)
        
        # 數據庫查詢分析
        query_issues = analyze_database_queries(file)
        
        issues.extend(complexity_issues + memory_issues + query_issues)
    
    return {
        'success': len(issues) == 0,
        'details': issues,
        'severity': 'warning'
    }
```

## 自動修復

### 可自動修復的問題
```python
AUTO_FIXABLE = {
    'formatting': fix_formatting,
    'imports': fix_imports,
    'lint_errors': fix_lint_errors,
    'simple_types': fix_simple_type_errors,
    'trailing_spaces': fix_trailing_spaces,
    'missing_semicolons': fix_missing_semicolons
}
```

### 修復流程
```python
def auto_fix(results, files):
    """自動修復發現的問題"""
    
    fixed = []
    failed_to_fix = []
    
    for check, result in results.items():
        if result['status'] == 'failed' and check in AUTO_FIXABLE:
            try:
                fix_result = AUTO_FIXABLE[check](files)
                if fix_result['success']:
                    fixed.append({
                        'issue': check,
                        'files_fixed': fix_result['files']
                    })
                else:
                    failed_to_fix.append({
                        'issue': check,
                        'reason': fix_result['reason']
                    })
            except Exception as e:
                failed_to_fix.append({
                    'issue': check,
                    'reason': str(e)
                })
    
    return {
        'fixed': fixed,
        'failed': failed_to_fix,
        'requires_manual': identify_manual_fixes(results)
    }
```

## 報告生成

### 驗證報告格式
```markdown
# 驗證報告

## 摘要
- **目標**: feature/user-auth
- **級別**: Standard
- **時間**: 2025-01-19 14:30:22
- **結果**: ⚠️ 需要注意

## 統計
- ✅ 通過: 12/15
- ❌ 失敗: 2/15
- ⚠️ 警告: 1/15

## 詳細結果

### ✅ 通過的檢查
- Syntax: 無錯誤
- Linting: 符合規範
- Types: 類型正確
- Tests: 15/15 通過
- Coverage: 82% (目標 80%)

### ❌ 失敗的檢查

#### Security Scan
**嚴重性**: 🔴 Critical
**問題**: 發現硬編碼的 API 密鑰
**文件**: src/config.js:15
**建議**: 使用環境變量替代

#### Performance
**嚴重性**: 🟡 Warning
**問題**: O(n²) 複雜度算法
**文件**: src/utils/sort.js:23
**建議**: 使用更高效的排序算法

### 🔧 自動修復

已修復:
- ✅ 格式化問題 (3 個文件)
- ✅ Import 排序 (2 個文件)

需要手動修復:
- ❌ 安全問題需要手動處理
- ❌ 性能優化需要重新設計

## 建議

1. **立即修復**: 移除硬編碼的密鑰
2. **優化建議**: 重構排序算法
3. **改進空間**: 增加更多單元測試

## 下一步

```bash
# 查看具體問題
/verify-output file:src/config.js --detailed

# 嘗試自動修復
/verify-output last --fix

# 重新驗證
/verify-output feature:user-auth --level strict
```
```

## 持續驗證

### Git Hook 集成
```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🔍 驗證輸出..."
claude-code verify-output pr --level standard

if [ $? -ne 0 ]; then
    echo "❌ 驗證失敗，請修復問題後重試"
    exit 1
fi

echo "✅ 驗證通過"
```

### CI/CD 集成
```yaml
# .github/workflows/verify.yml
name: Output Verification

on: [push, pull_request]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run verification
        run: |
          claude-code verify-output pr --level strict --report
      - name: Upload report
        uses: actions/upload-artifact@v2
        with:
          name: verification-report
          path: verification-report.html
```

## 最佳實踐

### Do's ✅
- 每次生成代碼後驗證
- 使用適當的驗證級別
- 修復所有 critical 問題
- 保存驗證報告

### Don'ts ❌
- 不要忽略安全警告
- 不要跳過測試
- 不要降低驗證標準
- 不要手動修復可自動修復的問題

---

*命令版本: 1.0.0*
*最後更新: 2025-01-19*