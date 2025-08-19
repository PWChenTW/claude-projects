# 外部工具整合指南

## 概述
本指南說明如何整合和配置外部工具，增強 Claude Code 的能力。

## GitHub CLI (gh) 整合

### 安裝配置
```bash
# macOS
brew install gh

# Linux
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# 認證
gh auth login
```

### 常用命令整合
```python
# .claude/tools/github_integration.py

class GitHubIntegration:
    """GitHub CLI 整合"""
    
    def create_pr(self, title, body, base='main'):
        """創建 Pull Request"""
        cmd = f'gh pr create --title "{title}" --body "{body}" --base {base}'
        return run_command(cmd)
    
    def review_pr(self, pr_number):
        """查看 PR 詳情"""
        cmd = f'gh pr view {pr_number}'
        return run_command(cmd)
    
    def list_issues(self, labels=None):
        """列出 Issues"""
        cmd = 'gh issue list'
        if labels:
            cmd += f' --label {",".join(labels)}'
        return run_command(cmd)
    
    def create_release(self, tag, title, notes):
        """創建 Release"""
        cmd = f'gh release create {tag} --title "{title}" --notes "{notes}"'
        return run_command(cmd)
```

### Claude 命令映射
```markdown
# .claude/commands/github.md

## GitHub 操作命令

### 創建 PR
/gh-pr "Title" "Description"

### 查看 Issues
/gh-issues [--label bug]

### 創建 Release
/gh-release v1.0.0 "Release Title" "Release Notes"
```

## Puppeteer 整合（截圖功能）

### 安裝配置
```bash
# 安裝 Puppeteer
npm install puppeteer

# 或使用 puppeteer-core（更輕量）
npm install puppeteer-core
```

### 截圖工具實現
```javascript
// .claude/tools/screenshot.js

const puppeteer = require('puppeteer');

class ScreenshotTool {
    async captureWebPage(url, outputPath) {
        const browser = await puppeteer.launch({
            headless: 'new',
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        
        const page = await browser.newPage();
        
        // 設置視窗大小
        await page.setViewport({
            width: 1920,
            height: 1080,
            deviceScaleFactor: 2
        });
        
        await page.goto(url, {
            waitUntil: 'networkidle2'
        });
        
        // 截圖
        await page.screenshot({
            path: outputPath,
            fullPage: true
        });
        
        await browser.close();
        
        return outputPath;
    }
    
    async captureElement(url, selector, outputPath) {
        const browser = await puppeteer.launch({
            headless: 'new'
        });
        
        const page = await browser.newPage();
        await page.goto(url);
        
        // 等待元素出現
        await page.waitForSelector(selector);
        
        // 截取特定元素
        const element = await page.$(selector);
        await element.screenshot({ path: outputPath });
        
        await browser.close();
        
        return outputPath;
    }
    
    async generatePDF(url, outputPath) {
        const browser = await puppeteer.launch({
            headless: 'new'
        });
        
        const page = await browser.newPage();
        await page.goto(url, {
            waitUntil: 'networkidle2'
        });
        
        // 生成 PDF
        await page.pdf({
            path: outputPath,
            format: 'A4',
            printBackground: true,
            margin: {
                top: '20px',
                right: '20px',
                bottom: '20px',
                left: '20px'
            }
        });
        
        await browser.close();
        
        return outputPath;
    }
}

module.exports = ScreenshotTool;
```

### 整合到 Claude 命令
```python
# .claude/commands/screenshot.md

## 截圖命令

### 網頁截圖
/screenshot <url> [--full-page] [--pdf]

### 元素截圖
/screenshot <url> --selector "#header" 

### 批量截圖
/screenshot-batch urls.txt --output-dir ./screenshots/
```

## 測試框架整合

### Jest 整合
```javascript
// .claude/tools/jest_integration.js

class JestIntegration {
    async runTests(pattern) {
        const cmd = `npx jest ${pattern} --json`;
        const result = await execCommand(cmd);
        return JSON.parse(result);
    }
    
    async runWithCoverage() {
        const cmd = 'npx jest --coverage --json';
        const result = await execCommand(cmd);
        return this.formatCoverageReport(JSON.parse(result));
    }
    
    async watchMode(pattern) {
        const cmd = `npx jest ${pattern} --watch`;
        return spawnCommand(cmd);
    }
    
    formatCoverageReport(data) {
        return {
            summary: data.coverageMap,
            uncoveredFiles: this.findUncoveredFiles(data),
            suggestions: this.generateCoverageSuggestions(data)
        };
    }
}
```

### Pytest 整合
```python
# .claude/tools/pytest_integration.py

import subprocess
import json

class PytestIntegration:
    def run_tests(self, path='.', markers=None):
        """運行 pytest 測試"""
        cmd = ['pytest', path, '--json-report', '--json-report-file=report.json']
        
        if markers:
            cmd.extend(['-m', markers])
        
        subprocess.run(cmd)
        
        with open('report.json') as f:
            return json.load(f)
    
    def run_with_coverage(self, path='.'):
        """運行測試並生成覆蓋率報告"""
        cmd = [
            'pytest', path,
            '--cov=.',
            '--cov-report=json',
            '--cov-report=term'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        with open('coverage.json') as f:
            coverage_data = json.load(f)
        
        return {
            'tests': result.returncode == 0,
            'coverage': coverage_data,
            'output': result.stdout
        }
    
    def run_specific_test(self, test_path):
        """運行特定測試"""
        cmd = ['pytest', test_path, '-v']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'errors': result.stderr
        }
```

## 權限管理配置

### 分層權限系統
```yaml
# .claude/permissions.yaml

levels:
  relaxed:
    description: "開發和測試環境"
    allowed:
      - all read operations
      - write to non-critical paths
      - execute test commands
    blocked:
      - production deployments
      - database migrations
      - security configurations
    
  standard:
    description: "一般開發任務"
    allowed:
      - read all files
      - write to src/ and tests/
      - execute build and test
    requires_confirmation:
      - git push
      - npm publish
      - API calls to production
    blocked:
      - system modifications
      - production configs
    
  strict:
    description: "生產和安全相關"
    allowed:
      - read non-sensitive files
      - write to designated areas only
    requires_confirmation:
      - all write operations
      - all external API calls
      - all git operations
    blocked:
      - access to secrets
      - production database
      - system commands
```

### 自動批准規則
```python
# .claude/tools/permission_manager.py

class PermissionManager:
    def __init__(self, level='standard'):
        self.level = level
        self.rules = self.load_rules(level)
    
    def check_permission(self, action, resource):
        """檢查權限"""
        
        # 檢查是否在允許列表
        if self.is_allowed(action, resource):
            return {'allowed': True, 'require_confirmation': False}
        
        # 檢查是否需要確認
        if self.requires_confirmation(action, resource):
            return {'allowed': True, 'require_confirmation': True}
        
        # 檢查是否被阻止
        if self.is_blocked(action, resource):
            return {'allowed': False, 'reason': self.get_block_reason(action, resource)}
        
        # 默認行為
        return {'allowed': False, 'reason': 'No explicit permission'}
    
    def auto_approve_patterns(self):
        """自動批准的模式"""
        return [
            r'^git status',
            r'^git diff',
            r'^npm test',
            r'^ls ',
            r'^cat ',
            r'^echo ',
            r'^pwd$'
        ]
    
    def escalate_permission(self, reason):
        """權限提升請求"""
        return {
            'request': 'permission_escalation',
            'current_level': self.level,
            'reason': reason,
            'requires': 'user_approval'
        }
```

### 白名單配置
```json
// .claude/whitelist.json
{
  "commands": {
    "always_allowed": [
      "ls",
      "pwd",
      "echo",
      "cat",
      "grep",
      "find",
      "git status",
      "git diff",
      "npm test",
      "pytest"
    ],
    "auto_approved_patterns": [
      "^git log",
      "^npm run [a-z-]+$",
      "^python -m pytest",
      "^node [a-z-]+\\.js$"
    ],
    "requires_confirmation": [
      "git push",
      "git merge",
      "npm publish",
      "rm -rf",
      "docker",
      "kubectl"
    ]
  },
  "paths": {
    "writable": [
      "src/**",
      "tests/**",
      "docs/**",
      ".claude/**"
    ],
    "readable": [
      "**"
    ],
    "restricted": [
      ".env",
      "**/*.key",
      "**/*.pem",
      "**/secrets/**"
    ]
  }
}
```

## 工具鏈配置

### 統一工具配置
```javascript
// .claude/toolchain.config.js

module.exports = {
  // 代碼質量工具
  quality: {
    linter: 'eslint',
    formatter: 'prettier',
    typeChecker: 'typescript'
  },
  
  // 測試工具
  testing: {
    unit: 'jest',
    e2e: 'cypress',
    coverage: 'nyc'
  },
  
  // 構建工具
  build: {
    bundler: 'webpack',
    transpiler: 'babel',
    minifier: 'terser'
  },
  
  // 外部服務
  external: {
    github: {
      cli: 'gh',
      api: 'octokit'
    },
    screenshot: 'puppeteer',
    monitoring: 'datadog'
  },
  
  // 自動化配置
  automation: {
    preCommit: ['lint', 'test'],
    prePush: ['test', 'build'],
    ci: ['lint', 'test', 'build', 'deploy']
  }
};
```

## 整合測試

### 工具整合測試
```python
# .claude/tests/test_tool_integration.py

def test_github_cli_available():
    """測試 GitHub CLI 是否可用"""
    result = subprocess.run(['gh', '--version'], capture_output=True)
    assert result.returncode == 0

def test_puppeteer_installation():
    """測試 Puppeteer 是否正確安裝"""
    result = subprocess.run(['node', '-e', "require('puppeteer')"], capture_output=True)
    assert result.returncode == 0

def test_permission_system():
    """測試權限系統"""
    pm = PermissionManager('standard')
    
    # 測試允許的操作
    assert pm.check_permission('read', 'src/index.js')['allowed']
    
    # 測試需要確認的操作
    result = pm.check_permission('execute', 'git push')
    assert result['allowed'] and result['require_confirmation']
    
    # 測試被阻止的操作
    assert not pm.check_permission('write', '.env')['allowed']
```

## 故障排除

### 常見問題

#### GitHub CLI 認證失敗
```bash
# 重新認證
gh auth logout
gh auth login

# 檢查狀態
gh auth status
```

#### Puppeteer 啟動失敗
```bash
# 安裝系統依賴（Linux）
sudo apt-get install -y \
  libnss3 \
  libatk-bridge2.0-0 \
  libx11-xcb1 \
  libxcomposite1

# 使用無沙盒模式
puppeteer.launch({
  args: ['--no-sandbox', '--disable-setuid-sandbox']
})
```

#### 權限被拒絕
```python
# 檢查當前權限級別
print(permission_manager.level)

# 請求權限提升
permission_manager.escalate_permission("Need to access production API")
```

---

*版本: 1.0.0*
*最後更新: 2025-01-19*