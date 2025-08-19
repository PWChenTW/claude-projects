# 團隊協作指南：多實例 AI 開發

## 🌟 概述

本指南幫助團隊有效協調多個 Claude 實例，實現高效並行開發。

## 📊 協作模式

### 1. 單實例模式
適用於：小型項目、單人開發
```yaml
模式: 單實例
優點:
  - 簡單直接
  - 無協調開銷
  - 上下文一致
缺點:
  - 無法並行
  - 受 token 限制
```

### 2. 多實例並行模式
適用於：中大型項目、團隊開發
```yaml
模式: 多實例
優點:
  - 高度並行
  - 分工明確
  - 效率倍增
挑戰:
  - 需要協調
  - 可能衝突
```

### 3. 混合模式
適用於：複雜項目、分階段開發
```yaml
模式: 混合
策略:
  - 核心架構：單實例
  - 功能開發：多實例
  - 測試驗證：並行實例
```

## 🔧 實施策略

### Step 1: 分工規劃

#### 按功能模組分工
```yaml
# .claude/team-allocation.yaml
allocation:
  instance_frontend:
    name: "Frontend Developer"
    branch: "feature/ui"
    modules:
      - src/components
      - src/styles
      - src/pages
    tasks:
      - UI component development
      - Style system
      - User interactions
    
  instance_backend:
    name: "Backend Developer"
    branch: "feature/api"
    modules:
      - src/api
      - src/services
      - src/database
    tasks:
      - API endpoints
      - Business logic
      - Database operations
    
  instance_testing:
    name: "Test Engineer"
    branch: "feature/tests"
    modules:
      - tests/
      - cypress/
      - __tests__/
    tasks:
      - Unit tests
      - Integration tests
      - E2E tests
```

#### 按層級分工
```yaml
allocation:
  instance_leaf:
    name: "Leaf Node Developer"
    focus: "葉節點任務"
    examples:
      - UI components
      - Utility functions
      - Test cases
    
  instance_boundary:
    name: "Boundary Layer Developer"
    focus: "邊界層任務"
    examples:
      - API development
      - Service integration
      - Data transformation
    
  instance_core:
    name: "Core Architect"
    focus: "核心架構"
    examples:
      - System design
      - Security
      - Performance optimization
```

### Step 2: 環境設置

#### Git Worktree 設置
```bash
#!/bin/bash
# setup-worktrees.sh

# 主倉庫
MAIN_REPO="/path/to/main/repo"

# 創建 worktree
git worktree add ../frontend feature/ui
git worktree add ../backend feature/api
git worktree add ../testing feature/tests

# 為每個實例創建配置
for instance in frontend backend testing; do
  cat > ../$instance/.claude/instance.config.json <<EOF
{
  "instance_name": "$instance",
  "branch": "feature/$instance",
  "auto_sync": true,
  "sync_interval": 300
}
EOF
done
```

#### 共享記憶配置
```python
# .claude/scripts/shared_memory.py
import json
import os
from datetime import datetime

class SharedMemory:
    """多實例共享記憶系統"""
    
    def __init__(self, instance_id):
        self.instance_id = instance_id
        self.memory_path = ".kiro/memory/shared/"
        
    def write(self, key, value):
        """寫入共享記憶"""
        data = {
            "value": value,
            "instance": self.instance_id,
            "timestamp": datetime.now().isoformat()
        }
        
        filepath = f"{self.memory_path}/{key}.json"
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
            
    def read(self, key):
        """讀取共享記憶"""
        filepath = f"{self.memory_path}/{key}.json"
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return None
        
    def broadcast(self, message):
        """廣播消息給所有實例"""
        self.write(f"broadcast_{datetime.now().timestamp()}", {
            "message": message,
            "type": "broadcast"
        })
```

### Step 3: 協調機制

#### 任務分配系統
```python
# .claude/scripts/task_coordinator.py
class TaskCoordinator:
    """任務協調器"""
    
    def __init__(self):
        self.tasks = self.load_tasks()
        self.instances = self.discover_instances()
        
    def assign_task(self, task_id, instance_id=None):
        """分配任務"""
        if instance_id:
            # 指定分配
            self.tasks[task_id]['assigned_to'] = instance_id
        else:
            # 自動分配
            instance = self.find_best_instance(task_id)
            self.tasks[task_id]['assigned_to'] = instance
            
        self.tasks[task_id]['status'] = 'assigned'
        self.save_tasks()
        
    def find_best_instance(self, task_id):
        """找到最合適的實例"""
        task = self.tasks[task_id]
        
        # 根據任務類型分配
        if 'ui' in task['type']:
            return 'instance_frontend'
        elif 'api' in task['type']:
            return 'instance_backend'
        elif 'test' in task['type']:
            return 'instance_testing'
            
        # 負載均衡
        return self.least_loaded_instance()
```

#### 衝突預防
```yaml
# .claude/conflict-prevention.yaml
strategies:
  file_locking:
    description: "文件級鎖定"
    implementation: |
      # 編輯前獲取鎖
      /lock-file src/api/users.js
      # 編輯文件
      # 釋放鎖
      /unlock-file src/api/users.js
  
  module_ownership:
    description: "模組所有權"
    rules:
      - Frontend owns: src/components/*, src/styles/*
      - Backend owns: src/api/*, src/services/*
      - Shared: src/utils/*, src/config/*
  
  merge_strategy:
    description: "合併策略"
    approach:
      - 頻繁小合併
      - 自動化測試門檻
      - 衝突立即解決
```

### Step 4: 同步機制

#### 定期同步腳本
```bash
#!/bin/bash
# sync-instances.sh

# 同步間隔（秒）
SYNC_INTERVAL=300

while true; do
    echo "=== 開始同步 $(date) ==="
    
    # 1. 拉取所有分支
    git fetch --all
    
    # 2. 更新共享記憶
    python .claude/scripts/memory_sync.py --type shared
    
    # 3. 合併無衝突的分支
    for branch in feature/ui feature/api feature/tests; do
        echo "嘗試合併 $branch..."
        if git merge origin/$branch --no-commit --no-ff; then
            git commit -m "Auto-merge $branch"
            echo "✓ 成功合併 $branch"
        else
            git merge --abort
            echo "✗ $branch 有衝突，需要手動解決"
        fi
    done
    
    # 4. 運行集成測試
    npm run test:integration
    
    # 5. 更新狀態儀表板
    python .claude/scripts/update_dashboard.py
    
    # 6. 廣播同步完成
    echo "同步完成" > .kiro/memory/shared/last_sync.txt
    
    sleep $SYNC_INTERVAL
done
```

#### 實時通信
```javascript
// .claude/scripts/realtime-sync.js
const WebSocket = require('ws');

class InstanceCommunicator {
  constructor(instanceId) {
    this.instanceId = instanceId;
    this.ws = new WebSocket('ws://localhost:8080');
    
    this.ws.on('open', () => {
      this.register();
    });
    
    this.ws.on('message', (data) => {
      this.handleMessage(JSON.parse(data));
    });
  }
  
  register() {
    this.send({
      type: 'register',
      instanceId: this.instanceId,
      capabilities: this.getCapabilities()
    });
  }
  
  broadcast(message) {
    this.send({
      type: 'broadcast',
      from: this.instanceId,
      message: message
    });
  }
  
  handleMessage(msg) {
    switch(msg.type) {
      case 'task_assigned':
        console.log(`新任務: ${msg.taskId}`);
        break;
      case 'sync_required':
        console.log('需要同步');
        this.performSync();
        break;
      case 'conflict_detected':
        console.log(`衝突檢測: ${msg.file}`);
        break;
    }
  }
}
```

## 📈 監控和報告

### 實例狀態儀表板
```python
# .claude/scripts/dashboard.py
def generate_dashboard():
    """生成實例狀態儀表板"""
    
    dashboard = """
╔════════════════════════════════════════════════════╗
║                 團隊協作儀表板                      ║
╠════════════════════════════════════════════════════╣
║ 實例狀態                                           ║
║ ├─ Frontend: 🟢 活躍 | 3 任務進行中               ║
║ ├─ Backend:  🟢 活躍 | 2 任務進行中                ║
║ └─ Testing:  🟡 空閒 | 0 任務進行中                ║
╠════════════════════════════════════════════════════╣
║ 任務進度                                           ║
║ ├─ 總任務: 45                                      ║
║ ├─ 已完成: 28 (62%)                                ║
║ ├─ 進行中: 12 (27%)                                ║
║ └─ 待分配: 5 (11%)                                 ║
╠════════════════════════════════════════════════════╣
║ 最近活動                                           ║
║ ├─ 10:23 Frontend 完成 UI-234                      ║
║ ├─ 10:15 Backend 開始 API-567                      ║
║ └─ 10:05 Testing 完成測試套件                      ║
╠════════════════════════════════════════════════════╣
║ 系統健康                                           ║
║ ├─ 測試通過率: 95%                                 ║
║ ├─ 代碼覆蓋率: 87%                                 ║
║ └─ 構建狀態: ✅ 成功                               ║
╚════════════════════════════════════════════════════╝
    """
    
    return dashboard
```

### 協作效率指標
```python
metrics = {
    "並行效率": {
        "定義": "實際加速比 / 理論加速比",
        "目標": "> 0.7",
        "當前": "0.82"
    },
    
    "衝突率": {
        "定義": "衝突次數 / 提交次數",
        "目標": "< 0.05",
        "當前": "0.03"
    },
    
    "同步延遲": {
        "定義": "平均同步時間",
        "目標": "< 5分鐘",
        "當前": "3.2分鐘"
    },
    
    "任務完成率": {
        "定義": "按時完成任務 / 總任務",
        "目標": "> 0.9",
        "當前": "0.94"
    }
}
```

## 🎯 最佳實踐

### 1. 明確分工
- 每個實例有清晰的責任範圍
- 避免重疊和空白區域
- 定期審查和調整分工

### 2. 頻繁同步
- 小步快跑，頻繁提交
- 自動化同步流程
- 及時解決衝突

### 3. 統一規範
- 代碼風格一致
- 命名規則統一
- 測試標準相同

### 4. 有效溝通
- 使用共享記憶系統
- 廣播重要變更
- 定期團隊同步會

### 5. 監控預警
- 實時監控各實例狀態
- 衝突預警機制
- 性能瓶頸檢測

## 💻 實戰範例

### 案例：開發電商功能
```bash
# Instance 1: Frontend
cd ../frontend
/spec-init product-listing "產品列表頁面"
/explore product-listing --focus ui
/execute product-listing

# Instance 2: Backend
cd ../backend
/spec-init product-api "產品API"
/explore product-api --focus api
/execute product-api

# Instance 3: Testing
cd ../testing
/spec-init product-tests "產品功能測試"
/plan product-tests --comprehensive
/execute product-tests

# 主實例：協調和集成
cd ../main
./sync-instances.sh
npm run test:integration
git merge --no-ff feature/ui feature/api feature/tests
```

## 🚨 故障排除

### 問題 1：頻繁衝突
```bash
# 解決方案
1. 檢查分工是否明確
2. 增加同步頻率
3. 使用文件鎖定機制
```

### 問題 2：實例間通信失敗
```bash
# 診斷
cat .kiro/memory/shared/last_sync.txt
ps aux | grep sync-instances

# 修復
killall sync-instances.sh
./sync-instances.sh &
```

### 問題 3：性能下降
```python
# 檢查並行效率
python .claude/scripts/check_efficiency.py

# 優化建議
if efficiency < 0.5:
    print("考慮減少實例數量")
elif conflicts > 0.1:
    print("需要更好的任務分配")
```

## 📋 檢查清單

### 開始協作前
- [ ] 定義清晰的分工
- [ ] 設置 Git worktree
- [ ] 配置共享記憶
- [ ] 啟動同步腳本
- [ ] 測試通信機制

### 協作過程中
- [ ] 定期檢查儀表板
- [ ] 及時解決衝突
- [ ] 保持代碼同步
- [ ] 運行集成測試
- [ ] 更新任務狀態

### 協作結束後
- [ ] 合併所有分支
- [ ] 完整測試驗證
- [ ] 清理臨時文件
- [ ] 總結經驗教訓
- [ ] 更新最佳實踐

## 🔗 相關資源

- [Git Worktree 指南](./git-worktree.md)
- [共享記憶系統](./shared-memory.md)
- [衝突解決策略](./conflict-resolution.md)
- [自動化測試集成](./test-integration.md)

---

*版本: 1.0.0*
*最後更新: 2025-01-19*
*適用於: Claude Code 多實例協作*

**需要幫助？** 查看 [FAQ](../faq/team-collaboration.md) 或聯繫支援團隊。