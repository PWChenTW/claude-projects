# Global Claude Configuration

## 🌐 Enterprise-Level Settings

This file contains global configuration that applies to ALL projects using Claude Code.

## Core Principles (Inherited by All Projects)

### 1. Safety First
- Never modify production configurations without explicit approval
- Always validate inputs before processing
- Implement proper error handling
- Follow security best practices

### 2. Quality Standards
- Minimum test coverage: 60% for leaf nodes, 80% for boundary, 100% for core
- Code must pass linting and type checking
- Documentation required for all public APIs
- Meaningful commit messages

### 3. Development Philosophy
- **MVP First**: Start with the simplest working solution
- **Progressive Enhancement**: Iterate in small, tested increments
- **YAGNI**: Don't implement features until they're needed
- **DRY**: Don't repeat yourself, but don't over-abstract

## Global Tool Permissions

### Always Allowed (No Approval Needed)
```yaml
allowed_commands:
  - ls
  - cat
  - grep
  - find
  - echo
  - pwd
  - git status
  - git diff
  - npm test
  - python -m pytest
```

### Requires Confirmation
```yaml
confirm_commands:
  - git push
  - npm publish
  - pip install
  - rm -rf
  - docker
```

### Always Blocked
```yaml
blocked_commands:
  - sudo
  - chmod 777
  - eval
  - exec
```

## Memory Management Rules

### Global Memory Hierarchy
1. **Global Memory** (`~/.claude/memory/`)
   - Cross-project learnings
   - Common patterns and solutions
   - Tool preferences and configurations

2. **Project Memory** (`./kiro/memory/`)
   - Project-specific knowledge
   - Decision history
   - Custom configurations

3. **Session Memory** (`./kiro/memory/session/`)
   - Temporary work state
   - Auto-expires after 24 hours

## Performance Optimization

### Token Usage Guidelines
- Use researcher pattern for all analysis tasks
- Batch related operations in single tool calls
- Prefer reading specific files over searching when path is known
- Cache frequently accessed information in session memory

### Response Time Targets
- Simple queries: < 5 seconds
- Code generation: < 30 seconds
- Complex analysis: < 2 minutes
- Full feature implementation: < 10 minutes

## Error Handling Standards

### Error Response Format
```javascript
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {}, // Optional additional context
    "suggestion": "How to fix or proceed"
  }
}
```

### Recovery Strategies
1. **Graceful Degradation**: Provide partial functionality when possible
2. **Clear Communication**: Explain what went wrong and why
3. **Actionable Suggestions**: Always provide next steps
4. **Learn and Adapt**: Record errors for pattern recognition

## Collaboration Protocols

### Multi-Instance Coordination
- Use git branches for parallel work
- Regular sync via shared memory files
- Clear ownership boundaries
- Conflict resolution through communication

### Human-AI Interaction
- Ask for clarification when requirements are ambiguous
- Provide options when multiple solutions exist
- Explain reasoning for important decisions
- Request review for critical changes

## Monitoring and Metrics

### Track and Report
- Token usage per task
- Success/failure rates
- Time to completion
- User satisfaction signals

### Continuous Improvement
- Weekly pattern analysis
- Monthly performance review
- Quarterly framework updates
- Annual major version releases

## Compliance and Governance

### Data Handling
- Never log sensitive information
- Respect privacy settings
- Follow GDPR/CCPA guidelines
- Implement data retention policies

### Audit Trail
- Log all significant actions
- Maintain decision records
- Track configuration changes
- Document security events

## Override Mechanism

Project-specific CLAUDE.md can override these settings by explicitly stating:
```markdown
## Override Global Settings
- Setting: [specific setting]
- Reason: [justification]
- Scope: [where this applies]
```

---

*Version: 1.0.0*
*Last Updated: 2025-01-19*
*Status: Active*

*This configuration is automatically loaded for all Claude Code sessions.*