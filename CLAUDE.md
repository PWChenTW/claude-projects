# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a template repository containing two AI-assisted development templates:
1. **General_Project_Template/** - General-purpose AI collaboration template for web apps, tools, games, etc.
2. **Quant_Project_Template/** - Specialized template for quantitative trading and financial analysis

## Commands

### Template Setup
```bash
# Copy and set up a new project from a template
cp -r General_Project_Template ~/my-new-project
cd ~/my-new-project
./setup.sh

# Or for quantitative projects
cp -r Quant_Project_Template ~/my-trading-strategy
cd ~/my-trading-strategy
./setup.sh
```

### Template Testing
```bash
# After setup, verify the environment
./test_setup.sh
```

### Development Commands (within a project created from template)
```bash
# Start AI collaboration
claude-code

# Initialize a new feature with Spec-Driven Development (SDD)
/spec-init [feature-name] [description]

# Context Engineering Commands
/spec-generate-prp [feature-name]  # Generate implementation blueprint
/spec-ultrathink [feature-name]    # Deep analysis before implementation

# Validate feature context completeness
python .claude/scheduler/context_validator.py [feature-name]

# Check project progress
python .claude/scheduler/spec_scheduler.py report

# View command statistics
python scripts/monitoring/view_command_audit.py
```

## Architecture

### Template Structure
Each template follows a Spec-Driven Development (SDD) approach enhanced with Context Engineering principles:
- **Context-first development** with comprehensive feature context requirements
- **Multi-instance collaboration** support for different roles
- **Sub Agents** for specialized tasks
- **Automated quality checks** including context validation
- **Knowledge base** in `.kiro/` directory with context engineering guidelines

### Sub Agents by Template

**General Template Sub Agents:**
- `business-analyst`: Requirements analysis, BDD scenarios, UX design
- `architect`: System architecture, DDD modeling, tech selection
- `data-specialist`: Data structures, algorithms, performance optimization
- `integration-specialist`: API design, external services, system integration
- `test-engineer`: Test strategy, automation, code quality
- `tech-lead`: Technical leadership, code review, team coordination
- `context-manager`: Knowledge management, documentation, project memory

**Quant Template Sub Agents:**
- `strategy-analyst`: Strategy requirements, BDD scenarios, risk assessment
- `risk-manager`: Risk rules, position sizing, capital management
- `data-engineer`: Data acquisition, technical indicators, feature engineering
- `api-specialist`: API integration, performance, error handling
- `test-engineer`: Test strategy, automation, code quality
- `tech-lead`: Trading system leadership, performance optimization
- `context-manager`: Strategy knowledge, market intelligence, research docs
- `data-scientist`: Machine learning, statistical modeling, predictions
- `hft-researcher`: Market microstructure, latency optimization, order execution
- `quant-analyst`: Financial modeling, derivatives pricing, portfolio optimization

### Key Directories
- `.claude/`: AI collaboration configuration
  - `agents/`: Sub Agent definitions
  - `commands/`: Slash command implementations (including context engineering commands)
  - `scheduler/`: Task scheduling, quality checks, and context validation
  - `settings.json`: Hooks configuration
- `.kiro/`: Project knowledge base
  - `steering/`: Core project knowledge (product, tech, methodology, context engineering principles)
  - `specs/`: Feature specifications with SDD workflow and implementation blueprints
- `docs/`: Documentation and quick references
  - `examples/`: Code patterns and implementation examples for context
- `scripts/monitoring/`: Audit and monitoring tools
- `INITIAL.md`: Feature specification template following context engineering format