# API Integration Patterns

## Overview
Best practices and patterns for integrating with external APIs and building robust API clients.

## API Client Base Class

```javascript
class ApiClient {
  constructor(baseURL, options = {}) {
    this.baseURL = baseURL;
    this.timeout = options.timeout || 30000;
    this.headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };
    this.interceptors = {
      request: [],
      response: []
    };
  }

  // Add request interceptor
  addRequestInterceptor(interceptor) {
    this.interceptors.request.push(interceptor);
  }

  // Add response interceptor
  addResponseInterceptor(interceptor) {
    this.interceptors.response.push(interceptor);
  }

  // Process interceptors
  async processRequestInterceptors(config) {
    for (const interceptor of this.interceptors.request) {
      config = await interceptor(config);
    }
    return config;
  }

  async processResponseInterceptors(response) {
    for (const interceptor of this.interceptors.response) {
      response = await interceptor(response);
    }
    return response;
  }

  // Main request method
  async request(endpoint, options = {}) {
    let config = {
      method: 'GET',
      ...options,
      headers: {
        ...this.headers,
        ...options.headers
      }
    };

    // Process request interceptors
    config = await this.processRequestInterceptors(config);

    const url = `${this.baseURL}${endpoint}`;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url, {
        ...config,
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      // Process response interceptors
      const processedResponse = await this.processResponseInterceptors(response);

      if (!processedResponse.ok) {
        throw new ApiError(
          `API request failed: ${processedResponse.statusText}`,
          processedResponse.status,
          await processedResponse.text()
        );
      }

      return processedResponse.json();
    } catch (error) {
      clearTimeout(timeoutId);
      
      if (error.name === 'AbortError') {
        throw new ApiError('Request timeout', 408);
      }
      
      throw error;
    }
  }

  // Convenience methods
  get(endpoint, options = {}) {
    return this.request(endpoint, { ...options, method: 'GET' });
  }

  post(endpoint, data, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  put(endpoint, data, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  delete(endpoint, options = {}) {
    return this.request(endpoint, { ...options, method: 'DELETE' });
  }
}
```

## Authentication Patterns

```javascript
// Bearer token authentication
class AuthenticatedApiClient extends ApiClient {
  constructor(baseURL, options = {}) {
    super(baseURL, options);
    this.token = null;
    
    // Add auth interceptor
    this.addRequestInterceptor(async (config) => {
      if (this.token) {
        config.headers.Authorization = `Bearer ${this.token}`;
      }
      return config;
    });
  }

  setToken(token) {
    this.token = token;
  }

  async refreshToken(refreshToken) {
    const response = await this.post('/auth/refresh', { refreshToken });
    this.token = response.accessToken;
    return response;
  }
}

// API key authentication
class ApiKeyClient extends ApiClient {
  constructor(baseURL, apiKey, options = {}) {
    super(baseURL, {
      ...options,
      headers: {
        ...options.headers,
        'X-API-Key': apiKey
      }
    });
  }
}

// OAuth 2.0 client
class OAuth2Client {
  constructor(config) {
    this.clientId = config.clientId;
    this.clientSecret = config.clientSecret;
    this.redirectUri = config.redirectUri;
    this.authorizationUrl = config.authorizationUrl;
    this.tokenUrl = config.tokenUrl;
    this.scopes = config.scopes || [];
  }

  getAuthorizationUrl(state) {
    const params = new URLSearchParams({
      client_id: this.clientId,
      redirect_uri: this.redirectUri,
      response_type: 'code',
      scope: this.scopes.join(' '),
      state
    });

    return `${this.authorizationUrl}?${params}`;
  }

  async exchangeCodeForToken(code) {
    const response = await fetch(this.tokenUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': `Basic ${Buffer.from(`${this.clientId}:${this.clientSecret}`).toString('base64')}`
      },
      body: new URLSearchParams({
        grant_type: 'authorization_code',
        code,
        redirect_uri: this.redirectUri
      })
    });

    if (!response.ok) {
      throw new Error('Failed to exchange code for token');
    }

    return response.json();
  }
}
```

## Retry and Circuit Breaker Patterns

```javascript
// Retry logic with exponential backoff
class RetryableApiClient extends ApiClient {
  constructor(baseURL, options = {}) {
    super(baseURL, options);
    this.maxRetries = options.maxRetries || 3;
    this.retryDelay = options.retryDelay || 1000;
    this.retryableStatuses = new Set([408, 429, 500, 502, 503, 504]);
  }

  async requestWithRetry(endpoint, options = {}, retryCount = 0) {
    try {
      return await this.request(endpoint, options);
    } catch (error) {
      if (
        retryCount < this.maxRetries &&
        (this.retryableStatuses.has(error.status) || !error.status)
      ) {
        const delay = this.retryDelay * Math.pow(2, retryCount);
        await new Promise(resolve => setTimeout(resolve, delay));
        
        return this.requestWithRetry(endpoint, options, retryCount + 1);
      }
      
      throw error;
    }
  }
}

// Circuit breaker pattern
class CircuitBreaker {
  constructor(options = {}) {
    this.failureThreshold = options.failureThreshold || 5;
    this.resetTimeout = options.resetTimeout || 60000;
    this.monitoringPeriod = options.monitoringPeriod || 10000;
    
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
    this.failures = 0;
    this.lastFailureTime = null;
    this.successCount = 0;
    this.requestCount = 0;
  }

  async execute(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime > this.resetTimeout) {
        this.state = 'HALF_OPEN';
        this.failures = 0;
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.failures = 0;
    
    if (this.state === 'HALF_OPEN') {
      this.successCount++;
      if (this.successCount >= 3) {
        this.state = 'CLOSED';
        this.successCount = 0;
      }
    }
  }

  onFailure() {
    this.failures++;
    this.lastFailureTime = Date.now();
    
    if (this.failures >= this.failureThreshold) {
      this.state = 'OPEN';
    }
  }
}
```

## Rate Limiting and Throttling

```javascript
// Token bucket rate limiter
class RateLimiter {
  constructor(capacity, refillRate) {
    this.capacity = capacity;
    this.tokens = capacity;
    this.refillRate = refillRate; // tokens per second
    this.lastRefill = Date.now();
  }

  async acquire(tokens = 1) {
    this.refill();
    
    if (this.tokens >= tokens) {
      this.tokens -= tokens;
      return true;
    }
    
    // Calculate wait time
    const waitTime = ((tokens - this.tokens) / this.refillRate) * 1000;
    await new Promise(resolve => setTimeout(resolve, waitTime));
    
    return this.acquire(tokens);
  }

  refill() {
    const now = Date.now();
    const timePassed = (now - this.lastRefill) / 1000;
    const tokensToAdd = timePassed * this.refillRate;
    
    this.tokens = Math.min(this.capacity, this.tokens + tokensToAdd);
    this.lastRefill = now;
  }
}

// API client with rate limiting
class RateLimitedApiClient extends ApiClient {
  constructor(baseURL, options = {}) {
    super(baseURL, options);
    this.rateLimiter = new RateLimiter(
      options.rateLimit || 60,
      options.refillRate || 1
    );
  }

  async request(endpoint, options = {}) {
    await this.rateLimiter.acquire();
    return super.request(endpoint, options);
  }
}
```

## Caching Strategies

```javascript
// Simple in-memory cache
class CacheManager {
  constructor(options = {}) {
    this.cache = new Map();
    this.ttl = options.ttl || 300000; // 5 minutes default
    this.maxSize = options.maxSize || 100;
  }

  set(key, value, ttl = this.ttl) {
    // Implement LRU if cache is full
    if (this.cache.size >= this.maxSize) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }

    this.cache.set(key, {
      value,
      expiry: Date.now() + ttl
    });
  }

  get(key) {
    const item = this.cache.get(key);
    
    if (!item) return null;
    
    if (Date.now() > item.expiry) {
      this.cache.delete(key);
      return null;
    }
    
    return item.value;
  }

  clear() {
    this.cache.clear();
  }
}

// Cached API client
class CachedApiClient extends ApiClient {
  constructor(baseURL, options = {}) {
    super(baseURL, options);
    this.cache = new CacheManager(options.cache);
  }

  async get(endpoint, options = {}) {
    const cacheKey = `GET:${endpoint}:${JSON.stringify(options)}`;
    
    // Check cache first
    const cached = this.cache.get(cacheKey);
    if (cached) {
      return cached;
    }
    
    // Make request and cache result
    const result = await super.get(endpoint, options);
    this.cache.set(cacheKey, result);
    
    return result;
  }
}
```

## Webhook Handling

```javascript
// Webhook receiver with signature verification
class WebhookReceiver {
  constructor(secret) {
    this.secret = secret;
  }

  verifySignature(payload, signature, algorithm = 'sha256') {
    const crypto = require('crypto');
    const expectedSignature = crypto
      .createHmac(algorithm, this.secret)
      .update(payload)
      .digest('hex');
    
    return crypto.timingSafeEqual(
      Buffer.from(signature),
      Buffer.from(expectedSignature)
    );
  }

  // Express middleware
  middleware() {
    return (req, res, next) => {
      const signature = req.headers['x-webhook-signature'];
      const payload = JSON.stringify(req.body);
      
      if (!this.verifySignature(payload, signature)) {
        return res.status(401).json({ error: 'Invalid signature' });
      }
      
      next();
    };
  }
}

// Webhook event processor
class WebhookProcessor {
  constructor() {
    this.handlers = new Map();
  }

  on(eventType, handler) {
    if (!this.handlers.has(eventType)) {
      this.handlers.set(eventType, []);
    }
    this.handlers.get(eventType).push(handler);
  }

  async process(event) {
    const handlers = this.handlers.get(event.type) || [];
    
    for (const handler of handlers) {
      try {
        await handler(event);
      } catch (error) {
        console.error(`Error processing webhook event ${event.type}:`, error);
        // Implement retry logic or dead letter queue
      }
    }
  }
}
```

## GraphQL Client

```javascript
class GraphQLClient {
  constructor(endpoint, options = {}) {
    this.endpoint = endpoint;
    this.headers = options.headers || {};
  }

  async query(query, variables = {}, options = {}) {
    const response = await fetch(this.endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...this.headers,
        ...options.headers
      },
      body: JSON.stringify({
        query,
        variables
      })
    });

    const result = await response.json();

    if (result.errors) {
      throw new GraphQLError(result.errors);
    }

    return result.data;
  }

  // Batch queries
  async batchQuery(queries) {
    const batchedQuery = queries.map((q, i) => 
      `query${i}: ${q.query}`
    ).join('\n');

    const response = await this.query(`{ ${batchedQuery} }`);
    
    return queries.map((_, i) => response[`query${i}`]);
  }
}
```

## Best Practices

1. **Use timeout for all requests** - Prevent hanging requests
2. **Implement retry logic** - Handle transient failures gracefully
3. **Add circuit breakers** - Prevent cascading failures
4. **Cache responses** - Reduce API calls and improve performance
5. **Validate webhook signatures** - Ensure webhook authenticity
6. **Handle rate limits** - Respect API rate limits
7. **Use interceptors** - Centralize cross-cutting concerns
8. **Log API interactions** - For debugging and monitoring
9. **Version your API clients** - Handle API version changes
10. **Document integration points** - Include examples and error scenarios