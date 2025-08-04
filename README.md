# Claude Projects Templates

This repository contains two AI-assisted development templates for use with Claude Code (claude.ai/code).

## Templates

### 1. General Project Template
General-purpose AI collaboration template for web apps, tools, games, and other software projects.

**Features:**
- Spec-Driven Development (SDD) framework
- Context Engineering principles
- Multi-instance collaboration
- Specialized Sub Agents
- Automated quality checks

### 2. Quant Project Template
Specialized template for quantitative trading and financial analysis projects.

**Features:**
- Trading strategy development workflow
- Risk management integration
- Backtesting framework
- Market data handling
- Performance analytics

## Quick Start

### Setting Up a New Project

```bash
# For general projects
cp -r General_Project_Template ~/my-new-project
cd ~/my-new-project
./setup.sh

# For quantitative projects
cp -r Quant_Project_Template ~/my-trading-strategy
cd ~/my-trading-strategy
./setup.sh
```

### Framework Versions

Each template now includes two framework versions:

1. **Optimized Framework** (Recommended)
   - Flexible and efficient
   - Smart task complexity detection
   - Simple tasks are handled directly
   - Complex tasks get expert consultation
   - Less process overhead

2. **Original Framework**
   - Structured workflow
   - Mandatory multi-stage delegation
   - Comprehensive documentation requirements
   - Suitable for large teams or compliance-heavy projects

You can choose your preferred framework version during `setup.sh`.

## Documentation

- `docs/framework_comparison.md` - Detailed comparison between framework versions
- `docs/framework_migration_guide.md` - Guide for migrating between versions
- `docs/framework_optimization_proposal.md` - Rationale behind the optimized version

## Core Principles

Both templates follow these core development principles:

1. **MVP First** - Start with the simplest working solution
2. **Critical Thinking** - Question requirements, provide better alternatives
3. **Pragmatism** - Avoid over-engineering, focus on real value

## Task Logging

Both templates include an automatic task logging system. After completing any significant task, Claude will update the task log at `.kiro/logs/task_log.md`.

## Learn More

For detailed information about each template, see their respective README files:
- `General_Project_Template/README.md`
- `Quant_Project_Template/README.md`

---

*These templates are designed to enhance AI-assisted development with Claude Code while maintaining flexibility and efficiency.*