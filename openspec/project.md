# Project Context

## Purpose
A modern, Apple-style memo application built with Python and Tkinter. This is a desktop GUI application for managing personal memos with a clean, minimalist interface inspired by Apple's design system. The app supports adding, viewing, and removing memos with a focus on simplicity and user experience.

## Tech Stack
- **Language:** Python 3.13
- **GUI Framework:** Tkinter with ttk (standard Python GUI library)
- **Package Manager:** UV (modern Python package manager)
- **Code Formatting:** Black >= 25.11.0
- **Linting:** Ruff >= 0.14.6
- **Build System:** None (direct Python execution)

## Project Conventions

### Code Style
- **Formatting:** Black with default settings
- **Linting:** Ruff for code quality
- **Naming Conventions:**
  - Classes: PascalCase (e.g., `TodoListGUI`, `todolist`)
  - Methods/Functions: snake_case (e.g., `add_task`, `delete_selected_task`)
  - Variables: snake_case (e.g., `task_entry`, `colors`)
- **Language:** Chinese (Traditional) for UI text
- **Design System:** Apple-inspired design with specific color palette and typography

### Architecture Patterns
- **Single-file Application:** Main logic and GUI in `main.py`
- **MVC-inspired Structure:**
  - Model: `todolist` class for data management
  - View: `TodoListGUI` class for user interface
  - Controller: Event handlers within GUI class
- **Separation of Concerns:** Backend logic completely separated from GUI
- **Responsive Design:** Window resizing support with proper weight configuration

### Testing Strategy
- **Current Status:** No testing framework implemented
- **Recommended:** pytest for unit testing GUI components and backend logic
- **Manual Testing:** Required for GUI interactions and visual verification

### Git Workflow
- **Branch:** `master` (main branch)
- **Commits:** Standard commit messages
- **Files to Ignore:**
  - Virtual environment (`.venv/`)
  - Linting cache (`.ruff_cache/`)
  - Python bytecode (`__pycache__/`, `*.pyc`)

## Domain Context
- **Application Type:** Desktop memo/todo list manager
- **Target Platform:** Cross-platform desktop (Windows, macOS, Linux)
- **User Interface:** Chinese (Traditional) language with Apple-style design
- **User Interactions:**
  - Add memos via text input
  - Delete individual memos with confirmation
  - Clear all memos with bulk confirmation
  - Keyboard support (Enter key to add tasks)
- **Data Management:** In-memory storage (non-persistent)

## Important Constraints
- **Python Version:** Requires Python >= 3.13
- **GUI Framework:** Limited to Tkinter (standard library only, no external GUI frameworks)
- **No Persistent Storage:** Data is lost when application closes
- **Single User:** Designed for individual use, no multi-user support
- **No External Dependencies:** Runtime dependencies limited to Python standard library

## External Dependencies
- **Runtime:** None (uses only Python standard library)
- **Development Tools:**
  - Black (code formatting)
  - Ruff (linting)
  - UV (package management)
