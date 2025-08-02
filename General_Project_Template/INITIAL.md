# Feature Specification Template

## FEATURE
[Describe the specific feature or requirement in detail. Be extremely specific about what needs to be built, including user flows, expected behaviors, and acceptance criteria.]

### Example:
```
Build a user authentication system that supports:
- Email/password login with secure password hashing
- OAuth integration (Google, GitHub)
- Session management with JWT tokens
- Password reset flow via email
- Rate limiting for login attempts
```

## EXAMPLES
[Reference existing code patterns, similar implementations, or examples in the examples/ folder. Include code snippets that demonstrate the desired patterns.]

### Example:
```javascript
// Reference existing auth middleware pattern from middleware/auth.js
export const requireAuth = async (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  // ... validation logic
};

// Similar implementation in projects/user-service/auth.js
```

## DOCUMENTATION
[List relevant documentation, API references, library docs, and external resources. Include specific sections or methods that are particularly relevant.]

### Example:
```
- bcrypt documentation: https://www.npmjs.com/package/bcrypt#usage
- JWT best practices: https://tools.ietf.org/html/rfc7519#section-4.1
- Express session middleware: https://expressjs.com/en/resources/middleware/session.html
- OAuth 2.0 flow: https://oauth.net/2/grant-types/authorization-code/
```

## OTHER CONSIDERATIONS
[Project-specific constraints, gotchas, performance requirements, security considerations, and potential edge cases.]

### Example:
```
- Password requirements: min 8 chars, must include uppercase, lowercase, number
- Session timeout: 24 hours for regular users, 1 hour for admin users
- Rate limiting: Max 5 login attempts per 15 minutes per IP
- GDPR compliance: Users must be able to delete their account and all associated data
- Database: Using PostgreSQL with Prisma ORM
- Security: All passwords must be hashed with bcrypt (min 10 rounds)
- Performance: Auth checks should complete within 100ms
```