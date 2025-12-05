# Development Guide

This guide is for developers who want to contribute to the Todo List Manager project. It covers setup, coding standards, testing, and contribution workflow.

## 🛠️ Development Setup

### Prerequisites
- **Python 3.13+** (strict requirement)
- **UV** (recommended) or **pip** for package management
- **Git** for version control
- **Code Editor** (VS Code, PyCharm, etc.) with Python support

### Clone and Setup
```bash
# Clone repository
git clone https://github.com/Yamiyorunoshura/project-part-B.git
cd project-part-B

# Install development dependencies
uv sync --dev

# Create development branch
git checkout -b feature/your-feature-name
```

### Development Dependencies
The project uses these development tools:
- **Black** (>= 25.11.0): Code formatting
- **Ruff** (>= 0.14.6): Linting and code quality
- **UV**: Package and virtual environment management

### Virtual Environment
```bash
# UV creates virtual environment automatically
uv sync

# Activate manually if needed
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Verify installation
python main.py
```

## 📁 Project Structure

```
project-part-B/
├── main.py              # Main application (1515 lines)
├── README.md           # Project documentation
├── pyproject.toml      # Project configuration
├── uv.lock            # Dependency lock file
├── .gitignore         # Git ignore rules
├── docs/              # Documentation
│   ├── getting-started/   # Installation guides
│   ├── architecture/      # System design
│   ├── features/         # User documentation
│   ├── development/      # This guide
│   └── operations/       # Deployment and troubleshooting
└── openspec/           # OpenSpec specifications
    ├── project.md      # Project context
    ├── AGENTS.md       # OpenSpec workflow
    ├── specs/          # Feature specifications
    └── changes/        # Change proposals
```

## 📝 Code Standards

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `TodoListGUI`, `TaskRepository` |
| Methods/Functions | snake_case | `add_task`, `delete_selected_task` |
| Variables | snake_case | `task_entry`, `year_var` |
| Constants | UPPER_SNAKE_CASE | `DEFAULT_FONT_SIZE`, `COLORS` |
| Private Members | _leading_underscore | `_running`, `_check_notifications()` |

### Code Style

**Formatting (Black):**
```bash
# Format code
uv run black main.py

# Check formatting without applying
uv run black --check main.py
```

**Linting (Ruff):**
```bash
# Lint code
uv run ruff check main.py

# Auto-fix linting issues
uv run ruff check --fix main.py
```

### Style Guidelines

1. **Imports**: Group and sort imports:
   ```python
   # Standard library
   import sqlite3
   import threading
   import time

   # Third-party (none in this project)

   # Local application
   # (all code in main.py, no local imports)
   ```

2. **Documentation**: Use descriptive variable names instead of excessive comments
3. **Line Length**: 88 characters (Black default)
4. **Type Hints**: Not required but encouraged for complex functions
5. **Error Handling**: Use try-except blocks for recoverable errors

### UI Text Convention
- **Language**: Traditional Chinese (繁體中文)
- **Consistency**: Use same terminology throughout UI
- **Clarity**: Clear, concise button labels and messages

## 🔧 Development Workflow

### OpenSpec Development Process

This project uses **OpenSpec** for specification-driven development:

```
1. Create Proposal → 2. Write Spec → 3. Implement → 4. Archive
```

**Key Commands:**
```bash
# Create new change proposal
/.claude/commands/openspec/proposal.md

# Implement approved change
/.claude/commands/openspec/apply.md

# Archive deployed change
/.claude/commands/openspec/archive.md
```

### Branch Strategy
- `master`: Main branch with stable code
- `feature/*`: Feature development branches
- No long-lived branches except `master`

### Commit Guidelines
1. **Atomic Commits**: One logical change per commit
2. **Descriptive Messages**: Explain *why* not just *what*
3. **Reference Issues**: Include issue numbers when applicable

**Commit Message Format:**
```
feat: Add SQLite persistence for tasks

- Implement TaskRepository class for database operations
- Add error handling for database connection issues
- Update GUI to load/save tasks automatically

Resolves: #123
```

### Pull Request Process
1. **Fork** the repository
2. **Create Branch**: `feature/description`
3. **Make Changes**: Follow coding standards
4. **Run Checks**: Format, lint, test
5. **Submit PR**: With clear description
6. **Address Review**: Make requested changes
7. **Merge**: After approval

## 🧪 Testing

### Current Testing Status
- **No automated tests** implemented
- **Manual testing** required for GUI features
- **Console output** for debugging

### Recommended Testing Strategy

**Unit Tests (Recommended with pytest):**
```python
# Example test structure
def test_add_task():
    todo = todolist()
    todo.add_task("Test task")
    assert len(todo.get_all_tasks()) == 1

def test_delete_task():
    todo = todolist()
    todo.add_task("Test task")
    todo.delete_task(0)
    assert len(todo.get_all_tasks()) == 0
```

**GUI Testing (Manual):**
1. Launch application
2. Test each feature manually
3. Verify expected behavior
4. Check error conditions

**Integration Testing:**
1. Database operations
2. Notification scheduling
3. Cross-platform compatibility

### Debugging Tips

**Common Debugging Techniques:**
1. **Print Debugging**: Add `print()` statements for flow tracing
2. **Logging**: Use Python's `logging` module for structured logs
3. **Exception Inspection**: Catch and print exception details
4. **GUI Inspection**: Use Tkinter's `after()` for delayed debugging

**Debug Database:**
```python
# Add debug prints in TaskRepository methods
print(f"[DEBUG] Adding task: {task_text}")
print(f"[DEBUG] Database path: {self.db_path}")
```

## 🏗️ Architecture Patterns

### MVC-inspired Pattern
- **Model**: `todolist` + `TaskRepository` (data and business logic)
- **View**: `TodoListGUI` (user interface)
- **Controller**: Event handlers in GUI class

### Repository Pattern
- `TaskRepository` abstracts database operations
- Centralized data access logic
- Consistent error handling

### Observer Pattern (Notifications)
- `NotificationScheduler` observes time changes
- Notifies users when tasks are due
- Decoupled from main GUI thread

## 🔄 Adding New Features

### Feature Development Steps

1. **Proposal Phase** (OpenSpec):
   ```bash
   # Create proposal
   /.claude/commands/openspec/proposal.md
   ```
   - Describe feature purpose and scope
   - Define acceptance criteria
   - Get approval before implementation

2. **Specification Phase**:
   - Write detailed specification in `openspec/specs/`
   - Define UI changes, API changes, database schema
   - Create implementation tasks

3. **Implementation Phase**:
   - Create feature branch
   - Implement according to spec
   - Follow coding standards
   - Test thoroughly

4. **Review Phase**:
   - Submit pull request
   - Address review comments
   - Update documentation

5. **Deployment Phase**:
   - Merge to master
   - Archive specification
   - Update changelog

### Example: Adding a New Feature

**Feature**: "Task Categories"

**Steps:**
1. Create proposal: `openspec/changes/add-task-categories/proposal.md`
2. Write spec: `openspec/changes/add-task-categories/specs/task-categories/spec.md`
3. Implement:
   - Database schema update (add `category` column)
   - GUI category selector (dropdown or tags)
   - Business logic for category filtering
   - Update `TaskRepository` methods
4. Test: Manual testing of all category features
5. Document: Update user guide and architecture docs

## 🐛 Bug Fixing Process

### Bug Report Template
```
Title: [Brief description]
Platform: [Windows/macOS/Linux]
Python Version: [3.13.x]

Steps to Reproduce:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Expected Behavior:
[What should happen]

Actual Behavior:
[What actually happens]

Additional Context:
[Screenshots, logs, etc.]
```

### Bug Triage
1. **Reproduce**: Confirm bug exists
2. **Isolate**: Find minimal reproduction case
3. **Diagnose**: Identify root cause
4. **Fix**: Implement solution
5. **Test**: Verify fix works
6. **Document**: Update troubleshooting guide

### Common Bug Categories
1. **Database Issues**: Corruption, permission errors
2. **GUI Glitches**: Layout problems, event handling
3. **Notification Problems**: Platform-specific issues
4. **Cross-platform Differences**: Fonts, paths, behaviors

## 📚 Documentation Standards

### Code Documentation
- **Module Docstrings**: Not required for single-file project
- **Function Docstrings**: Use for complex functions
- **Inline Comments**: Explain *why*, not *what*

### User Documentation
- **Getting Started**: Step-by-step installation
- **Features Guide**: Complete user documentation
- **Troubleshooting**: Common issues and solutions

### Technical Documentation
- **Architecture**: System design and components
- **API Reference**: Code interfaces (if multi-file)
- **Development Guide**: This document

### Documentation Updates
- Update docs when adding new features
- Keep screenshots current
- Test documentation commands

## 🔍 Code Review Checklist

### General
- [ ] Follows coding standards
- [ ] No syntax errors
- [ ] Proper error handling
- [ ] No security vulnerabilities
- [ ] Documentation updated

### GUI Specific
- [ ] UI text in Traditional Chinese
- [ ] Apple-style design consistency
- [ ] Keyboard navigation works
- [ ] Window resizing handled
- [ ] Cross-platform compatibility

### Database Specific
- [ ] SQL queries parameterized (no injection risk)
- [ ] Error recovery implemented
- [ ] Data persistence verified
- [ ] Schema changes documented

### Performance
- [ ] No memory leaks
- [ ] Responsive UI
- [ ] Efficient database queries
- [ ] Notification scheduling efficient

## 🚀 Release Process

### Versioning
- **Educational Project**: No formal versioning
- **Changes**: Documented in OpenSpec archives
- **Breaking Changes**: Avoid if possible

### Release Checklist
1. [ ] All tests pass (manual)
2. [ ] Documentation updated
3. [ ] Code formatted and linted
4. [ ] Cross-platform testing completed
5. [ ] Release notes prepared
6. [ ] OpenSpec changes archived

### Distribution
- **Source Only**: Distribute as Python source
- **No Packaging**: No PyPI package or executable
- **GitHub Releases**: Source code releases on GitHub

## 🤝 Contributor Guidelines

### Getting Help
1. **Documentation**: Check docs/ first
2. **Issues**: Search existing issues
3. **Discussion**: Create new issue for questions

### Contribution Areas
1. **Bug Fixes**: Fix reported issues
2. **Features**: Implement approved proposals
3. **Documentation**: Improve guides and examples
4. **Testing**: Add test coverage
5. **Code Quality**: Refactoring and optimization

### Recognition
- Contributors listed in commit history
- Feature contributors acknowledged in docs
- Significant contributions noted in README

## 📞 Support

### Development Questions
- **Issue Tracker**: GitHub Issues
- **Response Time**: Within 1-2 days
- **Scope**: Project-specific questions only

### External Resources
- **Python Documentation**: docs.python.org
- **Tkinter Guide**: tkdocs.com
- **SQLite Documentation**: sqlite.org/docs.html
- **OpenSpec**: Project-specific specification system

---

**Ready to contribute?** Start by reviewing open issues or creating a feature proposal!