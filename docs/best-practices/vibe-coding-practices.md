# Vibe Coding 最佳實踐指南

## 🎯 核心理念

> "讓 AI 處理葉節點，人類掌控核心架構"

Vibe Coding 是一種協作編程哲學，強調：
- **合理分工**：根據任務性質分配給人類或 AI
- **快速迭代**：在安全區域內快速實驗
- **驗證優先**：通過測試而非審查確保質量
- **漸進增強**：從簡單開始，逐步優化

## 📊 任務分類矩陣

### 決策框架

```python
def categorize_task(task):
    """任務分類決策樹"""
    
    # 評估維度
    impact = assess_impact(task)        # 系統影響範圍
    complexity = assess_complexity(task) # 技術複雜度
    risk = assess_risk(task)            # 潛在風險
    creativity = assess_creativity(task) # 創意需求
    
    # 分類邏輯
    if impact == "system-wide" or risk == "high":
        return "CORE"  # 核心架構 - 人類主導
    elif complexity == "low" and risk == "low":
        return "LEAF"  # 葉節點 - AI 自主
    else:
        return "BOUNDARY"  # 邊界層 - 協作開發
```

### 實踐範例

| 任務類型 | 分類 | AI 參與度 | 人類監督 | 範例 |
|---------|------|-----------|----------|------|
| UI 組件開發 | 🟢 葉節點 | 100% | 最小 | 按鈕、表單、模態框 |
| 工具函數 | 🟢 葉節點 | 100% | 最小 | 格式化、驗證、轉換 |
| API 端點 | 🟡 邊界層 | 70% | 標準 | CRUD操作、數據查詢 |
| 業務邏輯 | 🟡 邊界層 | 50% | 標準 | 計算、規則引擎 |
| 數據庫設計 | 🔴 核心 | 30% | 嚴格 | Schema、索引、關係 |
| 安全系統 | 🔴 核心 | 10% | 嚴格 | 認證、授權、加密 |

## 🟢 葉節點開發最佳實踐

### 1. UI 組件開發

#### ✅ 適合 AI 自主開發
```jsx
// 示例：創建一個可重用的 Card 組件
function Card({ title, content, footer, variant = 'default' }) {
  return (
    <div className={`card card-${variant}`}>
      <div className="card-header">
        <h3>{title}</h3>
      </div>
      <div className="card-body">
        {content}
      </div>
      {footer && (
        <div className="card-footer">
          {footer}
        </div>
      )}
    </div>
  );
}
```

**最佳實踐**：
- 提供清晰的設計規範
- 給出現有組件作為參考
- 定義 props 接口
- 要求包含使用示例

#### 實施流程
```bash
# 1. 提供規範
"創建一個 Card 組件，支持 title、content、footer，
有 default、primary、danger 三種變體"

# 2. AI 生成代碼
# 3. 自動運行測試
npm test Card.test.js

# 4. 視覺驗證
npm run storybook
```

### 2. 工具函數開發

#### ✅ 完美的 AI 任務
```javascript
// 示例：日期格式化函數
function formatDate(date, format = 'YYYY-MM-DD') {
  const d = new Date(date);
  
  const tokens = {
    'YYYY': d.getFullYear(),
    'MM': String(d.getMonth() + 1).padStart(2, '0'),
    'DD': String(d.getDate()).padStart(2, '0'),
    'HH': String(d.getHours()).padStart(2, '0'),
    'mm': String(d.getMinutes()).padStart(2, '0'),
    'ss': String(d.getSeconds()).padStart(2, '0')
  };
  
  return format.replace(/YYYY|MM|DD|HH|mm|ss/g, match => tokens[match]);
}

// 測試用例
describe('formatDate', () => {
  test('formats date correctly', () => {
    expect(formatDate('2025-01-19', 'YYYY-MM-DD')).toBe('2025-01-19');
    expect(formatDate('2025-01-19', 'DD/MM/YYYY')).toBe('19/01/2025');
  });
});
```

**最佳實踐**：
- 提供輸入輸出示例
- 要求編寫測試用例
- 指定錯誤處理方式
- 要求 JSDoc 註釋

### 3. 測試代碼編寫

#### ✅ AI 擅長生成測試
```javascript
// 示例：為認證服務生成測試
describe('AuthService', () => {
  let authService;
  
  beforeEach(() => {
    authService = new AuthService();
    jest.clearAllMocks();
  });
  
  describe('login', () => {
    test('should return token for valid credentials', async () => {
      const result = await authService.login('user@example.com', 'password123');
      expect(result).toHaveProperty('token');
      expect(result.token).toMatch(/^eyJ/); // JWT token pattern
    });
    
    test('should throw error for invalid credentials', async () => {
      await expect(
        authService.login('user@example.com', 'wrongpassword')
      ).rejects.toThrow('Invalid credentials');
    });
    
    test('should handle rate limiting', async () => {
      // 嘗試多次失敗登錄
      for (let i = 0; i < 5; i++) {
        await authService.login('user@example.com', 'wrong').catch(() => {});
      }
      
      await expect(
        authService.login('user@example.com', 'password123')
      ).rejects.toThrow('Too many attempts');
    });
  });
});
```

## 🟡 邊界層協作實踐

### 1. API 開發

#### 人類定義接口，AI 實現細節

**人類責任**：
```yaml
# API 規範定義
endpoint: POST /api/users
authentication: required
authorization: admin
request:
  body:
    email: string, required, unique
    name: string, required
    role: enum[user, admin], default=user
response:
  201:
    id: uuid
    email: string
    name: string
    role: string
    createdAt: datetime
  400: validation errors
  409: email already exists
```

**AI 實現**：
```javascript
// AI 根據規範生成實現
router.post('/api/users', 
  authenticate, 
  authorize('admin'),
  validate(userSchema),
  async (req, res) => {
    try {
      const { email, name, role = 'user' } = req.body;
      
      // 檢查郵箱唯一性
      const existing = await User.findOne({ email });
      if (existing) {
        return res.status(409).json({ 
          error: 'Email already exists' 
        });
      }
      
      // 創建用戶
      const user = await User.create({
        email,
        name,
        role,
        createdAt: new Date()
      });
      
      res.status(201).json({
        id: user.id,
        email: user.email,
        name: user.name,
        role: user.role,
        createdAt: user.createdAt
      });
      
    } catch (error) {
      logger.error('User creation failed:', error);
      res.status(500).json({ 
        error: 'Internal server error' 
      });
    }
  }
);
```

### 2. 業務邏輯實現

#### 人類設計規則，AI 編碼實現

**人類定義業務規則**：
```markdown
## 訂單折扣計算規則
1. VIP 客戶：9折
2. 訂單金額 > 1000：95折
3. 首次購買：9折
4. 優惠券：根據優惠券規則
5. 折扣可疊加，但總折扣不超過 7折
```

**AI 實現邏輯**：
```javascript
class DiscountCalculator {
  calculateDiscount(order, customer, coupons = []) {
    let discounts = [];
    
    // VIP 折扣
    if (customer.isVIP) {
      discounts.push({
        type: 'VIP',
        rate: 0.10,
        amount: order.subtotal * 0.10
      });
    }
    
    // 金額折扣
    if (order.subtotal > 1000) {
      discounts.push({
        type: 'AMOUNT',
        rate: 0.05,
        amount: order.subtotal * 0.05
      });
    }
    
    // 首購折扣
    if (customer.isFirstPurchase) {
      discounts.push({
        type: 'FIRST_PURCHASE',
        rate: 0.10,
        amount: order.subtotal * 0.10
      });
    }
    
    // 優惠券折扣
    coupons.forEach(coupon => {
      if (this.validateCoupon(coupon, order)) {
        discounts.push({
          type: 'COUPON',
          code: coupon.code,
          rate: coupon.discountRate,
          amount: order.subtotal * coupon.discountRate
        });
      }
    });
    
    // 計算總折扣（最多 30%）
    const totalDiscountRate = Math.min(
      discounts.reduce((sum, d) => sum + d.rate, 0),
      0.30
    );
    
    const totalDiscountAmount = order.subtotal * totalDiscountRate;
    
    return {
      discounts,
      totalRate: totalDiscountRate,
      totalAmount: totalDiscountAmount,
      finalPrice: order.subtotal - totalDiscountAmount
    };
  }
}
```

## 🔴 核心架構人類主導實踐

### 1. 數據庫架構設計

#### 人類設計，AI 輔助

**人類決策**：
```sql
-- 人類設計核心 schema
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    balance DECIMAL(10, 2) DEFAULT 0.00,
    currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(20) DEFAULT 'active',
    CONSTRAINT positive_balance CHECK (balance >= 0)
);

-- 關鍵索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_accounts_user ON accounts(user_id);
```

**AI 輔助任務**：
- 生成 migration 文件
- 創建 seed 數據
- 編寫 ORM 模型
- 生成 CRUD 操作

### 2. 安全系統實現

#### 人類掌控關鍵決策

**人類定義安全策略**：
```javascript
// 人類定義核心安全策略
const securityPolicy = {
  password: {
    minLength: 12,
    requireUppercase: true,
    requireNumbers: true,
    requireSpecialChars: true,
    bcryptRounds: 12
  },
  
  session: {
    duration: '24h',
    refreshToken: true,
    sameSite: 'strict',
    secure: true,
    httpOnly: true
  },
  
  rateLimit: {
    login: {
      max: 5,
      window: '15m',
      blockDuration: '1h'
    },
    api: {
      max: 100,
      window: '1m'
    }
  },
  
  cors: {
    origin: process.env.ALLOWED_ORIGINS?.split(',') || [],
    credentials: true
  }
};
```

**AI 可以實現的部分**：
- 輸入驗證函數
- 日誌記錄
- 錯誤消息格式化
- 測試用例

## 📈 成功指標

### 量化 Vibe Coding 效果

```python
metrics = {
    "development_speed": {
        "before": "2 features/week",
        "after": "5 features/week",
        "improvement": "150%"
    },
    
    "bug_rate": {
        "before": "3 bugs/feature",
        "after": "0.5 bugs/feature",
        "improvement": "83% reduction"
    },
    
    "code_review_time": {
        "before": "2 hours/PR",
        "after": "30 minutes/PR",
        "improvement": "75% reduction"
    },
    
    "developer_satisfaction": {
        "before": 6.5,
        "after": 8.5,
        "improvement": "+2.0 points"
    }
}
```

### 關鍵績效指標

1. **自主開發成功率**
   - 目標：> 95% 的葉節點任務無需人工干預
   - 測量：成功完成的 AI 任務 / 總 AI 任務

2. **首次通過率**
   - 目標：> 90% 的代碼首次通過測試
   - 測量：首次測試通過 / 總提交

3. **返工率**
   - 目標：< 5% 的代碼需要重寫
   - 測量：重寫代碼行 / 總代碼行

## 🚀 實施路線圖

### Week 1: 評估和準備
```markdown
- [ ] 識別系統層級
- [ ] 標記核心架構
- [ ] 定義葉節點
- [ ] 設置驗證框架
```

### Week 2: 試點項目
```markdown
- [ ] 選擇試點功能
- [ ] 應用 Vibe Coding
- [ ] 測量指標
- [ ] 收集反饋
```

### Week 3: 擴展應用
```markdown
- [ ] 擴大應用範圍
- [ ] 優化流程
- [ ] 培訓團隊
- [ ] 建立規範
```

### Week 4: 全面推廣
```markdown
- [ ] 全團隊採用
- [ ] 持續監控
- [ ] 迭代改進
- [ ] 分享經驗
```

## 💡 專家建議

### 來自實踐者的智慧

> "不要試圖讓 AI 理解複雜的業務邏輯，而是將業務邏輯分解為 AI 能理解的小塊。" - 資深架構師

> "驗證比審查更重要。如果測試通過了，代碼就是好的。" - DevOps 主管

> "讓 AI 處理無聊的部分，這樣你就可以專注於有趣的部分。" - 全棧開發者

### 避免的陷阱

1. **過度依賴**：不要讓 AI 處理關鍵決策
2. **忽視測試**：始終要有完整的測試覆蓋
3. **跳過驗證**：每個 AI 輸出都要驗證
4. **模糊指令**：給 AI 清晰、具體的指令

## 📚 進階資源

### 深入學習
- [Vibe Coding 理論基礎](./vibe-coding-theory.md)
- [層級架構設計指南](../architecture/layered-design.md)
- [自動化測試策略](../testing/automation-strategy.md)

### 工具和模板
- [任務分類工具](../tools/task-classifier.md)
- [驗證檢查清單](../checklists/verification.md)
- [Vibe Coding 模板](../templates/vibe-coding/)

### 案例研究
- [電商平台重構案例](../case-studies/ecommerce-refactor.md)
- [SaaS 產品開發案例](../case-studies/saas-development.md)
- [移動應用開發案例](../case-studies/mobile-app.md)

## 🎯 行動呼籲

### 立即開始
1. 識別一個葉節點任務
2. 讓 AI 完全自主開發
3. 運行自動化測試
4. 評估結果

### 本週目標
- 將 3 個功能轉為 Vibe Coding 模式
- 測量開發時間節省
- 收集團隊反饋

### 本月計劃
- 建立 Vibe Coding 工作流程
- 培訓全體開發團隊
- 實施自動化驗證

---

*版本: 1.0.0*
*最後更新: 2025-01-19*
*貢獻者: AI 協作框架團隊*

**加入社群**: 分享您的 Vibe Coding 經驗和最佳實踐！