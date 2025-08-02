# Error Handling Patterns

## Overview
Consistent error handling patterns used throughout the application.

## Standard Error Response Format

```javascript
// Standard error response structure
{
  error: {
    code: 'USER_NOT_FOUND',
    message: 'The requested user does not exist',
    details: {
      userId: '12345'
    }
  },
  timestamp: '2024-01-15T10:30:00Z'
}
```

## Custom Error Classes

```javascript
// Base error class
class AppError extends Error {
  constructor(message, code, statusCode) {
    super(message);
    this.code = code;
    this.statusCode = statusCode;
    this.timestamp = new Date().toISOString();
  }
}

// Specific error types
class ValidationError extends AppError {
  constructor(message, details) {
    super(message, 'VALIDATION_ERROR', 400);
    this.details = details;
  }
}

class NotFoundError extends AppError {
  constructor(resource, id) {
    super(`${resource} not found`, 'NOT_FOUND', 404);
    this.details = { resource, id };
  }
}

class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized access') {
    super(message, 'UNAUTHORIZED', 401);
  }
}
```

## Express Error Middleware

```javascript
// Global error handler
const errorHandler = (err, req, res, next) => {
  // Log error
  logger.error({
    error: err.message,
    stack: err.stack,
    url: req.url,
    method: req.method,
    ip: req.ip
  });

  // Handle known errors
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: {
        code: err.code,
        message: err.message,
        details: err.details
      },
      timestamp: err.timestamp
    });
  }

  // Handle validation errors (e.g., from Joi)
  if (err.name === 'ValidationError') {
    return res.status(400).json({
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Invalid input',
        details: err.details
      }
    });
  }

  // Default error response
  res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred'
    }
  });
};
```

## Async Error Handling

```javascript
// Async route wrapper
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

// Usage in routes
router.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await User.findById(req.params.id);
  if (!user) {
    throw new NotFoundError('User', req.params.id);
  }
  res.json(user);
}));
```

## Database Error Handling

```javascript
// Repository pattern with error handling
class UserRepository {
  async findById(id) {
    try {
      const user = await db.query('SELECT * FROM users WHERE id = ?', [id]);
      return user[0];
    } catch (error) {
      // Log database error
      logger.error('Database error', { error, query: 'findById', id });
      
      // Transform to app error
      if (error.code === 'ER_NO_REFERENCED_ROW') {
        throw new NotFoundError('User', id);
      }
      
      throw new AppError('Database operation failed', 'DB_ERROR', 500);
    }
  }
}
```

## Client-Side Error Handling

```javascript
// API client with error handling
class ApiClient {
  async request(url, options = {}) {
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        }
      });

      if (!response.ok) {
        const error = await response.json();
        throw new ApiError(
          error.error.message,
          error.error.code,
          response.status
        );
      }

      return response.json();
    } catch (error) {
      // Network errors
      if (error instanceof TypeError) {
        throw new NetworkError('Network request failed');
      }
      
      throw error;
    }
  }
}

// React error boundary
class ErrorBoundary extends React.Component {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    // Log to error reporting service
    errorReporter.log({ error, errorInfo });
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback error={this.state.error} />;
    }

    return this.props.children;
  }
}
```

## Validation Error Handling

```javascript
// Input validation with detailed errors
const validateUser = (data) => {
  const schema = Joi.object({
    email: Joi.string().email().required(),
    password: Joi.string().min(8).required(),
    age: Joi.number().min(18).max(120)
  });

  const { error, value } = schema.validate(data, { abortEarly: false });
  
  if (error) {
    const details = error.details.reduce((acc, item) => {
      acc[item.path[0]] = item.message;
      return acc;
    }, {});
    
    throw new ValidationError('Invalid user data', details);
  }
  
  return value;
};
```

## Best Practices

1. **Always use custom error classes** for known error types
2. **Log errors with context** (user ID, request ID, etc.)
3. **Don't expose sensitive information** in error messages
4. **Use appropriate HTTP status codes**
5. **Provide actionable error messages** to users
6. **Handle errors at the appropriate level** (controller, service, repository)
7. **Use error boundaries** in React applications
8. **Implement retry logic** for transient failures
9. **Monitor and alert** on error rates
10. **Document error codes** in API documentation