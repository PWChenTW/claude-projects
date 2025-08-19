# 程式碼模式庫

## 📚 模式分類

本模式庫收錄了經過驗證的程式碼模式，分為以下類別：

1. **架構模式** - 系統級設計模式
2. **API 模式** - RESTful 和 GraphQL 模式
3. **數據模式** - 數據處理和存儲模式
4. **安全模式** - 安全最佳實踐
5. **性能模式** - 優化技巧
6. **測試模式** - 測試策略

---

## 🏗️ 架構模式

### 1. 分層架構模式

```javascript
// 標準三層架構
project/
├── presentation/     // 展示層
│   ├── controllers/
│   ├── views/
│   └── validators/
├── business/        // 業務層
│   ├── services/
│   ├── rules/
│   └── workflows/
└── data/           // 數據層
    ├── repositories/
    ├── models/
    └── migrations/
```

#### 實施範例

```javascript
// presentation/controllers/UserController.js
class UserController {
  constructor(userService) {
    this.userService = userService;
  }
  
  async create(req, res) {
    try {
      const userData = req.body;
      const user = await this.userService.createUser(userData);
      res.status(201).json(user);
    } catch (error) {
      res.status(400).json({ error: error.message });
    }
  }
}

// business/services/UserService.js
class UserService {
  constructor(userRepository, emailService) {
    this.userRepository = userRepository;
    this.emailService = emailService;
  }
  
  async createUser(userData) {
    // 業務邏輯
    this.validateBusinessRules(userData);
    
    // 數據操作
    const user = await this.userRepository.create(userData);
    
    // 副作用
    await this.emailService.sendWelcome(user);
    
    return user;
  }
  
  validateBusinessRules(userData) {
    if (userData.age < 18) {
      throw new Error('User must be 18 or older');
    }
  }
}

// data/repositories/UserRepository.js
class UserRepository {
  async create(userData) {
    return await User.create(userData);
  }
  
  async findById(id) {
    return await User.findByPk(id);
  }
}
```

### 2. 事件驅動架構

```javascript
// 事件發射器模式
class EventBus {
  constructor() {
    this.events = {};
  }
  
  on(event, handler) {
    if (!this.events[event]) {
      this.events[event] = [];
    }
    this.events[event].push(handler);
  }
  
  emit(event, data) {
    if (!this.events[event]) return;
    
    this.events[event].forEach(handler => {
      try {
        handler(data);
      } catch (error) {
        console.error(`Error in event handler for ${event}:`, error);
      }
    });
  }
  
  off(event, handler) {
    if (!this.events[event]) return;
    
    this.events[event] = this.events[event].filter(h => h !== handler);
  }
}

// 使用範例
const eventBus = new EventBus();

// 訂閱事件
eventBus.on('user.created', async (user) => {
  await sendWelcomeEmail(user);
});

eventBus.on('user.created', async (user) => {
  await updateAnalytics(user);
});

// 發布事件
eventBus.emit('user.created', newUser);
```

### 3. 依賴注入模式

```javascript
// 依賴注入容器
class DIContainer {
  constructor() {
    this.services = {};
    this.singletons = {};
  }
  
  register(name, factory, options = {}) {
    this.services[name] = {
      factory,
      singleton: options.singleton || false
    };
  }
  
  get(name) {
    const service = this.services[name];
    
    if (!service) {
      throw new Error(`Service ${name} not found`);
    }
    
    if (service.singleton) {
      if (!this.singletons[name]) {
        this.singletons[name] = service.factory(this);
      }
      return this.singletons[name];
    }
    
    return service.factory(this);
  }
}

// 配置依賴
const container = new DIContainer();

container.register('db', () => new Database(), { singleton: true });
container.register('userRepo', (c) => new UserRepository(c.get('db')));
container.register('emailService', () => new EmailService(), { singleton: true });
container.register('userService', (c) => 
  new UserService(c.get('userRepo'), c.get('emailService'))
);

// 使用
const userService = container.get('userService');
```

---

## 🌐 API 模式

### 1. RESTful API 標準模式

```javascript
// 標準 CRUD 端點
class ResourceController {
  // GET /resources
  async index(req, res) {
    const { page = 1, limit = 20, sort = '-createdAt', ...filters } = req.query;
    
    const resources = await this.service.findAll({
      page: parseInt(page),
      limit: parseInt(limit),
      sort,
      filters
    });
    
    res.json({
      data: resources.data,
      meta: {
        page: resources.page,
        limit: resources.limit,
        total: resources.total,
        pages: Math.ceil(resources.total / resources.limit)
      }
    });
  }
  
  // GET /resources/:id
  async show(req, res) {
    const resource = await this.service.findById(req.params.id);
    
    if (!resource) {
      return res.status(404).json({ error: 'Resource not found' });
    }
    
    res.json({ data: resource });
  }
  
  // POST /resources
  async create(req, res) {
    const resource = await this.service.create(req.body);
    res.status(201).json({ data: resource });
  }
  
  // PUT /resources/:id
  async update(req, res) {
    const resource = await this.service.update(req.params.id, req.body);
    res.json({ data: resource });
  }
  
  // DELETE /resources/:id
  async destroy(req, res) {
    await this.service.delete(req.params.id);
    res.status(204).send();
  }
}
```

### 2. GraphQL Resolver 模式

```javascript
// GraphQL resolver 模式
const resolvers = {
  Query: {
    user: async (_, { id }, { dataSources }) => {
      return dataSources.userAPI.getUser(id);
    },
    
    users: async (_, { page, limit }, { dataSources }) => {
      return dataSources.userAPI.getUsers({ page, limit });
    }
  },
  
  Mutation: {
    createUser: async (_, { input }, { dataSources }) => {
      return dataSources.userAPI.createUser(input);
    },
    
    updateUser: async (_, { id, input }, { dataSources }) => {
      return dataSources.userAPI.updateUser(id, input);
    }
  },
  
  User: {
    posts: async (user, _, { dataSources }) => {
      return dataSources.postAPI.getPostsByUserId(user.id);
    },
    
    fullName: (user) => {
      return `${user.firstName} ${user.lastName}`;
    }
  }
};
```

### 3. API 版本控制模式

```javascript
// 路由版本控制
app.use('/api/v1', v1Routes);
app.use('/api/v2', v2Routes);

// Header 版本控制
app.use((req, res, next) => {
  const version = req.headers['api-version'] || 'v1';
  req.apiVersion = version;
  next();
});

// 控制器版本處理
class UserController {
  async getUser(req, res) {
    const { apiVersion } = req;
    
    if (apiVersion === 'v1') {
      return this.getUserV1(req, res);
    } else if (apiVersion === 'v2') {
      return this.getUserV2(req, res);
    }
    
    res.status(400).json({ error: 'Unsupported API version' });
  }
}
```

---

## 📊 數據模式

### 1. Repository 模式

```javascript
// 基礎 Repository
class BaseRepository {
  constructor(model) {
    this.model = model;
  }
  
  async findAll(options = {}) {
    const {
      where = {},
      order = [['createdAt', 'DESC']],
      limit = 20,
      offset = 0,
      include = []
    } = options;
    
    return this.model.findAndCountAll({
      where,
      order,
      limit,
      offset,
      include
    });
  }
  
  async findById(id, options = {}) {
    return this.model.findByPk(id, options);
  }
  
  async create(data) {
    return this.model.create(data);
  }
  
  async update(id, data) {
    const [updated, [instance]] = await this.model.update(data, {
      where: { id },
      returning: true
    });
    
    return instance;
  }
  
  async delete(id) {
    return this.model.destroy({ where: { id } });
  }
}

// 擴展 Repository
class UserRepository extends BaseRepository {
  constructor() {
    super(User);
  }
  
  async findByEmail(email) {
    return this.model.findOne({ where: { email } });
  }
  
  async findActiveUsers() {
    return this.findAll({
      where: { status: 'active' }
    });
  }
}
```

### 2. 數據遷移模式

```javascript
// Migration 模式
class Migration {
  constructor(name, version) {
    this.name = name;
    this.version = version;
  }
  
  async up() {
    throw new Error('up method must be implemented');
  }
  
  async down() {
    throw new Error('down method must be implemented');
  }
}

// 實施範例
class CreateUsersTable extends Migration {
  constructor() {
    super('create-users-table', '20250119001');
  }
  
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('users', {
      id: {
        type: Sequelize.UUID,
        defaultValue: Sequelize.UUIDV4,
        primaryKey: true
      },
      email: {
        type: Sequelize.STRING,
        unique: true,
        allowNull: false
      },
      password: {
        type: Sequelize.STRING,
        allowNull: false
      },
      createdAt: {
        type: Sequelize.DATE,
        allowNull: false
      },
      updatedAt: {
        type: Sequelize.DATE,
        allowNull: false
      }
    });
    
    await queryInterface.addIndex('users', ['email']);
  }
  
  async down(queryInterface) {
    await queryInterface.dropTable('users');
  }
}
```

### 3. 快取模式

```javascript
// 快取裝飾器模式
function cacheable(ttl = 3600) {
  return function(target, propertyKey, descriptor) {
    const originalMethod = descriptor.value;
    
    descriptor.value = async function(...args) {
      const cacheKey = `${target.constructor.name}:${propertyKey}:${JSON.stringify(args)}`;
      
      // 嘗試從快取獲取
      const cached = await cache.get(cacheKey);
      if (cached) {
        return JSON.parse(cached);
      }
      
      // 執行原方法
      const result = await originalMethod.apply(this, args);
      
      // 存入快取
      await cache.set(cacheKey, JSON.stringify(result), ttl);
      
      return result;
    };
    
    return descriptor;
  };
}

// 使用範例
class UserService {
  @cacheable(600) // 快取 10 分鐘
  async getUser(id) {
    return await this.userRepository.findById(id);
  }
  
  @cacheable(3600) // 快取 1 小時
  async getPopularUsers() {
    return await this.userRepository.findPopular();
  }
}
```

---

## 🔐 安全模式

### 1. 認證中間件模式

```javascript
// JWT 認證中間件
const authenticate = async (req, res, next) => {
  try {
    const token = req.headers.authorization?.split(' ')[1];
    
    if (!token) {
      return res.status(401).json({ error: 'No token provided' });
    }
    
    const payload = jwt.verify(token, process.env.JWT_SECRET);
    
    // 獲取用戶信息
    const user = await User.findByPk(payload.userId);
    
    if (!user) {
      return res.status(401).json({ error: 'User not found' });
    }
    
    // 附加到請求
    req.user = user;
    req.userId = user.id;
    
    next();
  } catch (error) {
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({ error: 'Token expired' });
    }
    
    return res.status(401).json({ error: 'Invalid token' });
  }
};

// 角色授權中間件
const authorize = (...roles) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Unauthorized' });
    }
    
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    
    next();
  };
};

// 使用
router.post('/admin/users',
  authenticate,
  authorize('admin', 'superadmin'),
  createUser
);
```

### 2. 輸入驗證模式

```javascript
// 驗證中間件工廠
const validate = (schema) => {
  return (req, res, next) => {
    const { error, value } = schema.validate(req.body, {
      abortEarly: false,
      stripUnknown: true
    });
    
    if (error) {
      const errors = error.details.map(detail => ({
        field: detail.path.join('.'),
        message: detail.message
      }));
      
      return res.status(400).json({ errors });
    }
    
    // 替換為清理後的值
    req.body = value;
    next();
  };
};

// Schema 定義
const userSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().min(8).required(),
  name: Joi.string().min(2).max(50).required(),
  age: Joi.number().integer().min(18).max(120)
});

// 使用
router.post('/users',
  validate(userSchema),
  createUser
);
```

### 3. 速率限制模式

```javascript
// 速率限制器
class RateLimiter {
  constructor(options = {}) {
    this.windowMs = options.windowMs || 15 * 60 * 1000; // 15 分鐘
    this.max = options.max || 100; // 最大請求數
    this.storage = new Map();
  }
  
  middleware() {
    return (req, res, next) => {
      const key = this.getKey(req);
      const now = Date.now();
      
      // 獲取或創建記錄
      let record = this.storage.get(key);
      
      if (!record || now - record.resetTime > this.windowMs) {
        record = {
          count: 0,
          resetTime: now
        };
      }
      
      // 檢查限制
      if (record.count >= this.max) {
        const retryAfter = Math.ceil((record.resetTime + this.windowMs - now) / 1000);
        
        res.set('Retry-After', retryAfter);
        return res.status(429).json({
          error: 'Too many requests',
          retryAfter
        });
      }
      
      // 增加計數
      record.count++;
      this.storage.set(key, record);
      
      // 設置響應頭
      res.set('X-RateLimit-Limit', this.max);
      res.set('X-RateLimit-Remaining', this.max - record.count);
      res.set('X-RateLimit-Reset', new Date(record.resetTime + this.windowMs).toISOString());
      
      next();
    };
  }
  
  getKey(req) {
    // 可以基於 IP、用戶 ID 等
    return req.ip || req.userId || 'anonymous';
  }
}

// 使用
const limiter = new RateLimiter({
  windowMs: 15 * 60 * 1000,
  max: 5 // 15 分鐘內最多 5 次
});

router.post('/login', limiter.middleware(), login);
```

---

## ⚡ 性能模式

### 1. 批量處理模式

```javascript
// 批量處理器
class BatchProcessor {
  constructor(options = {}) {
    this.batchSize = options.batchSize || 100;
    this.flushInterval = options.flushInterval || 1000;
    this.queue = [];
    this.processing = false;
    
    // 定期刷新
    setInterval(() => this.flush(), this.flushInterval);
  }
  
  async add(item) {
    this.queue.push(item);
    
    if (this.queue.length >= this.batchSize) {
      await this.flush();
    }
  }
  
  async flush() {
    if (this.processing || this.queue.length === 0) {
      return;
    }
    
    this.processing = true;
    const batch = this.queue.splice(0, this.batchSize);
    
    try {
      await this.processBatch(batch);
    } catch (error) {
      console.error('Batch processing error:', error);
      // 可以選擇重新加入隊列
      this.queue.unshift(...batch);
    } finally {
      this.processing = false;
    }
  }
  
  async processBatch(batch) {
    // 實施批量處理邏輯
    throw new Error('processBatch must be implemented');
  }
}

// 使用範例
class DatabaseBatchWriter extends BatchProcessor {
  async processBatch(batch) {
    await db.bulkInsert('logs', batch);
  }
}

const writer = new DatabaseBatchWriter();
await writer.add({ level: 'info', message: 'User logged in' });
```

### 2. 連接池模式

```javascript
// 通用連接池
class ConnectionPool {
  constructor(factory, options = {}) {
    this.factory = factory;
    this.min = options.min || 2;
    this.max = options.max || 10;
    this.idleTimeout = options.idleTimeout || 30000;
    
    this.pool = [];
    this.activeConnections = 0;
    this.waitingQueue = [];
    
    // 初始化最小連接
    this.initialize();
  }
  
  async initialize() {
    for (let i = 0; i < this.min; i++) {
      const conn = await this.createConnection();
      this.pool.push(conn);
    }
  }
  
  async acquire() {
    // 有可用連接
    if (this.pool.length > 0) {
      const conn = this.pool.pop();
      this.activeConnections++;
      return conn;
    }
    
    // 可以創建新連接
    if (this.activeConnections < this.max) {
      const conn = await this.createConnection();
      this.activeConnections++;
      return conn;
    }
    
    // 需要等待
    return new Promise((resolve) => {
      this.waitingQueue.push(resolve);
    });
  }
  
  release(conn) {
    this.activeConnections--;
    
    // 有等待的請求
    if (this.waitingQueue.length > 0) {
      const resolve = this.waitingQueue.shift();
      this.activeConnections++;
      resolve(conn);
      return;
    }
    
    // 返回池中
    this.pool.push(conn);
    
    // 設置空閒超時
    setTimeout(() => {
      if (this.pool.length > this.min) {
        const index = this.pool.indexOf(conn);
        if (index !== -1) {
          this.pool.splice(index, 1);
          conn.close();
        }
      }
    }, this.idleTimeout);
  }
  
  async createConnection() {
    return await this.factory();
  }
}

// 使用
const dbPool = new ConnectionPool(
  () => createDatabaseConnection(),
  { min: 5, max: 20 }
);

const conn = await dbPool.acquire();
try {
  await conn.query('SELECT * FROM users');
} finally {
  dbPool.release(conn);
}
```

### 3. 懶加載模式

```javascript
// 懶加載代理
function lazy(factory) {
  let instance = null;
  
  return new Proxy({}, {
    get(target, prop) {
      if (!instance) {
        instance = factory();
      }
      return instance[prop];
    },
    
    set(target, prop, value) {
      if (!instance) {
        instance = factory();
      }
      instance[prop] = value;
      return true;
    }
  });
}

// 使用範例
const expensiveService = lazy(() => {
  console.log('Initializing expensive service...');
  return new ExpensiveService();
});

// 只有在實際使用時才初始化
expensiveService.doSomething(); // 這時才初始化
```

---

## 🧪 測試模式

### 1. 測試工廠模式

```javascript
// 測試數據工廠
class Factory {
  static seq = 0;
  
  static build(type, overrides = {}) {
    const factories = {
      user: () => ({
        id: ++this.seq,
        email: `user${this.seq}@example.com`,
        name: `User ${this.seq}`,
        password: 'hashedpassword',
        createdAt: new Date(),
        ...overrides
      }),
      
      post: () => ({
        id: ++this.seq,
        title: `Post ${this.seq}`,
        content: 'Lorem ipsum dolor sit amet',
        authorId: 1,
        published: false,
        createdAt: new Date(),
        ...overrides
      })
    };
    
    return factories[type]();
  }
  
  static async create(type, overrides = {}) {
    const data = this.build(type, overrides);
    // 實際創建到數據庫
    return await models[type].create(data);
  }
}

// 使用
describe('UserService', () => {
  test('creates user', async () => {
    const userData = Factory.build('user', { 
      email: 'test@example.com' 
    });
    
    const user = await userService.create(userData);
    
    expect(user.email).toBe('test@example.com');
  });
});
```

### 2. Mock 模式

```javascript
// Mock 創建器
class MockBuilder {
  constructor() {
    this.mocks = {};
  }
  
  mock(name, implementation) {
    this.mocks[name] = jest.fn(implementation);
    return this.mocks[name];
  }
  
  mockClass(ClassName) {
    const mockMethods = {};
    
    Object.getOwnPropertyNames(ClassName.prototype)
      .filter(name => name !== 'constructor')
      .forEach(method => {
        mockMethods[method] = jest.fn();
      });
    
    return mockMethods;
  }
  
  restore() {
    Object.values(this.mocks).forEach(mock => {
      mock.mockRestore();
    });
  }
}

// 使用
describe('OrderService', () => {
  let mockBuilder;
  let orderService;
  
  beforeEach(() => {
    mockBuilder = new MockBuilder();
    
    const mockRepo = mockBuilder.mockClass(OrderRepository);
    mockRepo.findById.mockResolvedValue({ id: 1, total: 100 });
    
    const mockEmail = mockBuilder.mock('sendEmail', async () => true);
    
    orderService = new OrderService(mockRepo, mockEmail);
  });
  
  afterEach(() => {
    mockBuilder.restore();
  });
  
  test('processes order', async () => {
    const result = await orderService.process(1);
    expect(result).toBeDefined();
  });
});
```

### 3. 集成測試模式

```javascript
// 測試環境設置
class TestEnvironment {
  async setup() {
    // 創建測試數據庫
    this.db = await this.createTestDatabase();
    
    // 運行遷移
    await this.runMigrations();
    
    // 種子數據
    await this.seedData();
    
    // 啟動服務器
    this.server = await this.startServer();
    
    return {
      db: this.db,
      server: this.server,
      request: supertest(this.server)
    };
  }
  
  async teardown() {
    await this.server.close();
    await this.db.close();
    await this.dropTestDatabase();
  }
  
  async createTestDatabase() {
    const dbName = `test_${Date.now()}`;
    await exec(`createdb ${dbName}`);
    return new Database({ database: dbName });
  }
  
  async runMigrations() {
    await exec('npm run migrate:test');
  }
  
  async seedData() {
    // 創建基礎測試數據
  }
  
  async startServer() {
    return app.listen(0); // 隨機端口
  }
}

// 使用
describe('API Integration Tests', () => {
  let env;
  
  beforeAll(async () => {
    env = await new TestEnvironment().setup();
  });
  
  afterAll(async () => {
    await env.teardown();
  });
  
  test('GET /api/users', async () => {
    const response = await env.request
      .get('/api/users')
      .expect(200);
    
    expect(response.body.data).toBeArray();
  });
});
```

---

## 📋 使用指南

### 選擇合適的模式

```javascript
function selectPattern(requirements) {
  const patterns = {
    'need-separation-of-concerns': 'Layered Architecture',
    'need-loose-coupling': 'Event-Driven Architecture',
    'need-testability': 'Dependency Injection',
    'need-api-consistency': 'RESTful Patterns',
    'need-data-abstraction': 'Repository Pattern',
    'need-security': 'Security Patterns',
    'need-performance': 'Performance Patterns',
    'need-reliable-tests': 'Testing Patterns'
  };
  
  return requirements.map(req => patterns[req]);
}
```

### 組合模式

多個模式可以組合使用：

```javascript
// 組合範例：DI + Repository + Cache
class CachedUserRepository extends UserRepository {
  constructor(cache) {
    super();
    this.cache = cache;
  }
  
  @cacheable(600)
  async findById(id) {
    return super.findById(id);
  }
}

container.register('cache', () => new RedisCache());
container.register('userRepo', (c) => 
  new CachedUserRepository(c.get('cache'))
);
```

### 模式演化

隨著項目成長，模式也需要演化：

```markdown
## 演化路徑
1. 簡單函數 → 類 → 服務
2. 直接調用 → 事件 → 消息隊列
3. 同步 → 異步 → 響應式
4. 單體 → 模組化 → 微服務
```

---

*模式庫版本: 1.0.0*
*最後更新: 2025-01-19*
*貢獻新模式: [GitHub](https://github.com/ai-collab/patterns)*