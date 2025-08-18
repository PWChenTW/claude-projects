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

## ⚠️ Template Synchronization Requirements

**IMPORTANT**: When making improvements to the AI collaboration framework, ensure that **BOTH** templates receive the same updates:

### Templates that Must Stay Synchronized:
1. **General_Project_Template/** - General-purpose AI collaboration
2. **Quant_Project_Template/** - Quantitative trading specialized

### Key Areas Requiring Synchronization:
- **Sub-agent definitions** (`.claude/agents/`)
- **Commands** (`.claude/commands/`)  
- **INITIAL.md** template
- **CLAUDE.md** configuration
- **Memory management scripts**
- **SDD workflow integration**

### Why Synchronization Matters:
- Prevents feature divergence between templates
- Ensures consistent user experience
- Maintains framework improvements across all project types
- Reduces maintenance burden

### How to Synchronize:
```bash
# Example: After updating General Template
cp General_Project_Template/.claude/commands/*.md Quant_Project_Template/.claude/commands/
cp General_Project_Template/INITIAL.md Quant_Project_Template/INITIAL.md

# Verify both templates have same features
diff -q General_Project_Template/.claude/commands/ Quant_Project_Template/.claude/commands/
```

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

**General Template Sub Agents (Researcher Mode):**
- `business-analyst-researcher`: Requirements research, BDD scenarios planning, UX analysis
- `architect-researcher`: System architecture research, DDD modeling, tech evaluation
- `data-specialist-researcher`: Data structure analysis, algorithm research, performance planning
- `integration-specialist-researcher`: API design research, service integration analysis
- `quality-researcher`: Quality assurance research, test strategy, best practices (merged test-engineer + tech-lead)
- `context-manager-researcher`: Knowledge management research, documentation planning

**Quant Template Sub Agents (Researcher Mode):**
- `quant-analyst-researcher`: Quantitative analysis, financial modeling, portfolio theory research
- `hft-researcher`: Market microstructure research, latency optimization analysis, order execution strategies
- `data-engineer-researcher`: Data pipeline research, technical indicators analysis, feature engineering planning
- `data-scientist-researcher`: ML model research, statistical analysis, prediction methodology
- `api-specialist-researcher`: API integration research, performance analysis, error handling strategies
- `system-architect-researcher`: Trading system architecture, technical design research (merged architect-analyst + developer-specialist)
- `quality-researcher`: Quality assurance research, test strategy, best practices (merged quality-engineer + test-engineer + tech-lead)
- `context-manager-researcher`: Strategy knowledge research, market intelligence analysis

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
├── context/
│   └── current.md        # Active working context (MUST update frequently)
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

### 🔴 Context vs Memory 重要區別

**Context (`.kiro/context/current.md`)** - 活躍工作記憶：
- **必須更新時機**：
  - ✅ 每次新會話開始時先讀取
  - ✅ 完成重大功能或改變後更新
  - ✅ 切換工作焦點時更新
  - ✅ 發現重要限制或問題時記錄
- **內容特點**：簡潔（2-3頁）、即時、高度相關
- **包含**：當前狀態、最近改變、活躍項目、快速參考

**Memory (`.kiro/memory/`)** - 持久化知識庫：
- **更新時機**：完成任務、做出決策、階段總結
- **內容特點**：詳細、完整、可追溯
- **包含**：完整進度、決策理由、歷史記錄

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