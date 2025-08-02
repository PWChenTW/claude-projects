# Data Validation Patterns

## Overview
Comprehensive data validation patterns for ensuring data integrity and security.

## Schema-Based Validation (Joi)

```javascript
const Joi = require('joi');

// User registration schema
const userRegistrationSchema = Joi.object({
  email: Joi.string()
    .email()
    .lowercase()
    .required()
    .messages({
      'string.email': 'Please provide a valid email address',
      'any.required': 'Email is required'
    }),
  
  password: Joi.string()
    .min(8)
    .pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/)
    .required()
    .messages({
      'string.pattern.base': 'Password must contain uppercase, lowercase, number and special character'
    }),
  
  confirmPassword: Joi.string()
    .valid(Joi.ref('password'))
    .required()
    .messages({
      'any.only': 'Passwords do not match'
    }),
  
  profile: Joi.object({
    firstName: Joi.string().min(2).max(50).required(),
    lastName: Joi.string().min(2).max(50).required(),
    dateOfBirth: Joi.date().max('now').required(),
    phone: Joi.string().pattern(/^\+?[\d\s-]+$/).optional()
  })
});

// Validation middleware
const validate = (schema) => {
  return (req, res, next) => {
    const { error, value } = schema.validate(req.body, {
      abortEarly: false,
      stripUnknown: true
    });
    
    if (error) {
      const errors = error.details.reduce((acc, detail) => {
        const path = detail.path.join('.');
        acc[path] = detail.message;
        return acc;
      }, {});
      
      return res.status(400).json({
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid input data',
          details: errors
        }
      });
    }
    
    req.validatedData = value;
    next();
  };
};
```

## Type-Safe Validation (TypeScript + Zod)

```typescript
import { z } from 'zod';

// Define schemas
const AddressSchema = z.object({
  street: z.string().min(1),
  city: z.string().min(1),
  state: z.string().length(2),
  zipCode: z.string().regex(/^\d{5}(-\d{4})?$/)
});

const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  username: z.string().min(3).max(20).regex(/^[a-zA-Z0-9_]+$/),
  age: z.number().int().min(0).max(150),
  roles: z.array(z.enum(['user', 'admin', 'moderator'])),
  address: AddressSchema.optional(),
  metadata: z.record(z.string(), z.any()).optional()
});

// Type inference
type User = z.infer<typeof UserSchema>;

// Validation function
function validateUser(data: unknown): User {
  try {
    return UserSchema.parse(data);
  } catch (error) {
    if (error instanceof z.ZodError) {
      throw new ValidationError('Invalid user data', error.errors);
    }
    throw error;
  }
}

// Safe parsing
function safeValidateUser(data: unknown) {
  const result = UserSchema.safeParse(data);
  if (!result.success) {
    return { success: false, errors: result.error.errors };
  }
  return { success: true, data: result.data };
}
```

## Custom Validators

```javascript
// Custom validation functions
const validators = {
  isStrongPassword(password) {
    const minLength = 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*]/.test(password);
    
    return {
      isValid: password.length >= minLength && hasUpperCase && 
               hasLowerCase && hasNumbers && hasSpecialChar,
      strength: [hasUpperCase, hasLowerCase, hasNumbers, hasSpecialChar]
        .filter(Boolean).length,
      feedback: {
        minLength: password.length >= minLength,
        hasUpperCase,
        hasLowerCase,
        hasNumbers,
        hasSpecialChar
      }
    };
  },

  isValidCreditCard(number) {
    // Remove spaces and dashes
    const cleaned = number.replace(/[\s-]/g, '');
    
    // Check if only digits
    if (!/^\d+$/.test(cleaned)) return false;
    
    // Luhn algorithm
    let sum = 0;
    let isEven = false;
    
    for (let i = cleaned.length - 1; i >= 0; i--) {
      let digit = parseInt(cleaned[i]);
      
      if (isEven) {
        digit *= 2;
        if (digit > 9) {
          digit -= 9;
        }
      }
      
      sum += digit;
      isEven = !isEven;
    }
    
    return sum % 10 === 0;
  },

  isValidEmail(email) {
    // RFC 5322 compliant regex
    const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
    
    // Additional checks
    const isValidFormat = emailRegex.test(email);
    const hasValidLength = email.length <= 254; // RFC 5321
    const [localPart, domain] = email.split('@');
    const hasValidLocalLength = localPart?.length <= 64; // RFC 5321
    
    return isValidFormat && hasValidLength && hasValidLocalLength;
  }
};
```

## Sanitization Patterns

```javascript
const sanitizers = {
  // HTML sanitization
  sanitizeHtml(input) {
    const map = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#x27;',
      '/': '&#x2F;'
    };
    return input.replace(/[&<>"'/]/g, (char) => map[char]);
  },

  // SQL injection prevention
  sanitizeSqlInput(input) {
    // Use parameterized queries instead!
    // This is just for demonstration
    return input.replace(/['";\\]/g, '');
  },

  // File name sanitization
  sanitizeFileName(fileName) {
    return fileName
      .replace(/[^a-zA-Z0-9.-]/g, '_') // Replace invalid chars
      .replace(/\.{2,}/g, '.') // Remove multiple dots
      .replace(/^\.+|\.+$/g, ''); // Remove leading/trailing dots
  },

  // Phone number normalization
  normalizePhoneNumber(phone) {
    // Remove all non-digits
    const digits = phone.replace(/\D/g, '');
    
    // Format as needed
    if (digits.length === 10) {
      return `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6)}`;
    }
    
    return digits;
  },

  // URL sanitization
  sanitizeUrl(url) {
    try {
      const parsed = new URL(url);
      
      // Allow only http(s) protocols
      if (!['http:', 'https:'].includes(parsed.protocol)) {
        throw new Error('Invalid protocol');
      }
      
      // Remove credentials
      parsed.username = '';
      parsed.password = '';
      
      return parsed.toString();
    } catch {
      throw new ValidationError('Invalid URL');
    }
  }
};
```

## Form Validation (React)

```jsx
import { useState, useCallback } from 'react';
import { z } from 'zod';

// Validation hook
function useFormValidation(schema) {
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});

  const validate = useCallback((data) => {
    try {
      schema.parse(data);
      setErrors({});
      return true;
    } catch (error) {
      if (error instanceof z.ZodError) {
        const newErrors = error.errors.reduce((acc, err) => {
          const path = err.path.join('.');
          acc[path] = err.message;
          return acc;
        }, {});
        setErrors(newErrors);
      }
      return false;
    }
  }, [schema]);

  const validateField = useCallback((name, value) => {
    try {
      const fieldSchema = schema.shape[name];
      if (fieldSchema) {
        fieldSchema.parse(value);
        setErrors(prev => ({ ...prev, [name]: undefined }));
      }
    } catch (error) {
      if (error instanceof z.ZodError) {
        setErrors(prev => ({ ...prev, [name]: error.errors[0].message }));
      }
    }
  }, [schema]);

  const touch = useCallback((name) => {
    setTouched(prev => ({ ...prev, [name]: true }));
  }, []);

  return { errors, touched, validate, validateField, touch };
}

// Form component
function RegistrationForm() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: ''
  });

  const schema = z.object({
    email: z.string().email('Invalid email address'),
    password: z.string().min(8, 'Password must be at least 8 characters'),
    confirmPassword: z.string()
  }).refine((data) => data.password === data.confirmPassword, {
    message: "Passwords don't match",
    path: ["confirmPassword"]
  });

  const { errors, touched, validate, validateField, touch } = useFormValidation(schema);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    if (touched[name]) {
      validateField(name, value);
    }
  };

  const handleBlur = (e) => {
    const { name, value } = e.target;
    touch(name);
    validateField(name, value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validate(formData)) {
      // Submit form
      console.log('Form is valid', formData);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        name="email"
        value={formData.email}
        onChange={handleChange}
        onBlur={handleBlur}
        className={errors.email && touched.email ? 'error' : ''}
      />
      {errors.email && touched.email && (
        <span className="error-message">{errors.email}</span>
      )}
      
      {/* Other fields... */}
    </form>
  );
}
```

## API Request Validation

```javascript
// Express middleware for different content types
const validateRequest = {
  body: (schema) => validate(schema, 'body'),
  query: (schema) => validate(schema, 'query'),
  params: (schema) => validate(schema, 'params'),
  
  // Combined validation
  all: (schemas) => async (req, res, next) => {
    try {
      if (schemas.body) {
        req.body = await schemas.body.parseAsync(req.body);
      }
      if (schemas.query) {
        req.query = await schemas.query.parseAsync(req.query);
      }
      if (schemas.params) {
        req.params = await schemas.params.parseAsync(req.params);
      }
      next();
    } catch (error) {
      next(error);
    }
  }
};

// Usage
router.post('/users',
  validateRequest.all({
    body: UserSchema,
    query: z.object({
      sendEmail: z.boolean().optional()
    })
  }),
  async (req, res) => {
    // Handler with validated data
  }
);
```

## Best Practices

1. **Validate at boundaries** - Always validate data at system boundaries (API endpoints, form submissions)
2. **Fail fast** - Validate as early as possible in the data flow
3. **Provide clear error messages** - Help users understand what went wrong
4. **Use schema validation** - Define schemas once, use everywhere
5. **Sanitize user input** - Never trust user input, always sanitize
6. **Type safety** - Use TypeScript/Zod for compile-time type checking
7. **Client and server validation** - Always validate on the server, client validation is for UX
8. **Consistent error format** - Use the same error structure throughout the application
9. **Don't over-validate** - Balance between security and user experience
10. **Keep validation DRY** - Reuse validation schemas and functions