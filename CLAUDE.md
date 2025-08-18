# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a template repository containing two AI-assisted development templates:
1. **General_Project_Template/** - General-purpose AI collaboration template for web apps, tools, games, etc.
2. **Quant_Project_Template/** - Specialized template for quantitative trading and financial analysis

## Framework Versions

Each template now includes two framework versions:
- **CLAUDE.md** - Original structured framework with strict delegation rules
- **CLAUDE_OPTIMIZED.md** - Optimized flexible framework balancing structure and freedom

Choose based on your project needs:
- Use optimized version for most projects (recommended)
- Use original version for large teams or compliance-heavy projects

See `docs/framework_comparison.md` for detailed comparison

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

# Initialize a new feature (two options)
/spec-init-simple [feature-name] [description]  # Simplified flow (recommended)
/spec-init [feature-name] [description]         # Full SDD flow

# Context Engineering Commands
/spec-generate-prp [feature-name]  # Generate implementation blueprint
/spec-ultrathink [feature-name]    # Deep analysis before implementation

# Validate feature context completeness
python .claude/scheduler/context_validator.py [feature-name]

# Check project progress
python .claude/scheduler/spec_scheduler.py report         # Detailed report
python .claude/scheduler/spec_scheduler_simple.py report  # Quick overview

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
  - `logs/`: Task execution logs and weekly archives
- `docs/`: Documentation and quick references
  - `examples/`: Code patterns and implementation examples for context
- `scripts/monitoring/`: Audit and monitoring tools
- `INITIAL.md`: Feature specification template following context engineering format

## Task Logging Requirements

### Mandatory Task Documentation

Claude MUST update the task log after completing any of the following:
- **Code changes**: Creating, modifying, or deleting code files
- **Feature implementation**: Completing a feature or sub-feature
- **Bug fixes**: Resolving any bugs or issues
- **Architecture decisions**: Making design or architecture changes
- **Documentation updates**: Creating or updating significant documentation
- **Configuration changes**: Modifying project configuration files

### Task Log Update Process

1. **After completing a task**, run:
   ```bash
   python .claude/scripts/update_task_log.py
   ```
   Or for quick logging:
   ```bash
   python .claude/scripts/update_task_log.py "Task description" "file1.py,file2.md" "Summary point 1;Summary point 2" "Task type"
   ```

2. **Required information**:
   - Task description (concise, 5-10 words)
   - Task type: Feature Development/Bug Fix/Refactoring/Documentation Update/Testing/Other
   - Affected files (main files modified or created)
   - Summary points (3-5 key changes)
   - Related tags (optional, e.g., #feature-name)

3. **Automatic archiving**: Logs are automatically archived every Sunday to `.kiro/logs/archive/`

### Example Task Log Entry

```markdown
### 2024-01-20 15:45
**Task**: Implement user authentication system
**Type**: Feature Development
**Affected files**: 
- `src/auth/login.py`
- `src/auth/middleware.py`
- `tests/test_auth.py`
**Summary**: 
- Added JWT-based authentication
- Created login/logout endpoints
- Implemented auth middleware
- Added comprehensive tests
**Related tags**: #auth #security
```

### When NOT to log
- Simple file reads or searches
- Minor typo fixes (unless in critical code)
- Temporary debugging changes
- Exploratory analysis without changes

## Project Memory and Progress Tracking

### Memory System Structure
When working on template improvements or framework enhancements, use the following structure:

```
.kiro/
├── memory/
│   ├── global/           # Cross-project persistent knowledge
│   ├── project/          # Current project memory
│   │   ├── enhancement-progress.md  # Main progress tracking document
│   │   └── decisions.md             # Important decisions record
│   └── session/          # Current session temporary memory
├── research/
│   └── [YYYY-MM-DD]/    # Daily research documents
│       ├── *.md          # Research reports and analysis
│       └── decisions/    # Daily decision records
└── logs/
    ├── tasks.log         # Task execution log
    └── archive/          # Archived weekly logs
```

### Progress Tracking Rules

#### Must Update Progress When:
1. **Completing sub-agent transformations**: Update `.kiro/memory/project/enhancement-progress.md`
2. **Making important decisions**: Record in `.kiro/memory/project/decisions.md`
3. **Completing research analysis**: Save to `.kiro/research/[current date]/`
4. **Architecture or process changes**: Update relevant memory documents

#### Update Methods:
- **Progress documents**: Use Edit/MultiEdit tools to update markdown files
- **Todo items**: Use TodoWrite tool to manage current tasks
- **Research documents**: Use Write tool to create new research reports

### Todo Management with TodoWrite

```python
# Task states: pending, in_progress, completed
# Only one task can be in_progress at a time
# Mark tasks as completed immediately after finishing
```

### Knowledge Update Workflow

1. **Research Phase**: Save all research outputs to `.kiro/research/[date]/`
2. **Decision Phase**: Update important decisions to `.kiro/memory/project/decisions.md`
3. **Implementation Phase**: Update progress to `.kiro/memory/project/enhancement-progress.md`
4. **Summary Phase**: Create summary documents in research directory

### Query Order Suggestion
When needing to understand project status:
1. Check `.kiro/memory/project/enhancement-progress.md` for overall progress
2. Check `.kiro/research/[recent date]/` for latest research
3. Use TodoWrite tool to view current tasks
4. Check `.kiro/memory/project/decisions.md` for key decisions