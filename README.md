# Todo List Manager - Cross-Platform Desktop Application

A modern, Apple-style memo/todo list application built with Python and Tkinter. This desktop GUI application helps you manage personal memos with a clean, minimalist interface, scheduled notifications, and data persistence.

![Application Screenshot](docs/images/screenshot.png)

## ✨ Features

- **📝 Memo Management**: Add, delete, and view memos with a simple interface
- **⏰ Scheduled Notifications**: Set reminders for specific date and time
- **💾 Data Persistence**: SQLite database automatically saves your tasks
- **🌍 Cross-Platform**: Works on Windows, macOS, and Linux
- **🍎 Apple-Style Design**: Clean, minimalist interface with specific color palette
- **🇹🇼 Traditional Chinese UI**: User interface in Traditional Chinese language
- **⌨️ Keyboard Support**: Use Enter key to add tasks quickly

## 📋 Requirements

- Python 3.13 or higher
- UV package manager (recommended) or pip

## 🚀 Quick Start

### 1. Install UV (Package Manager)

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/Yamiyorunoshura/project-part-B.git
cd project-part-B

# Sync dependencies
uv sync

# Run the application
uv run main.py
```

## 📖 Documentation

- [Getting Started](docs/getting-started/README.md) - Detailed installation and first run guide
- [User Guide](docs/features/README.md) - Complete feature documentation
- [Architecture](docs/architecture/README.md) - System design and technical details
- [Development Guide](docs/development/README.md) - For contributors and developers
- [Troubleshooting](docs/operations/troubleshooting.md) - Common issues and solutions

## 🏗️ Architecture

The application follows an MVC-inspired architecture:

- **Model**: `todolist` class for data management and SQLite persistence
- **View**: `TodoListGUI` class for user interface with Tkinter
- **Controller**: Event handlers within GUI class

### Key Components:
1. **Task Repository**: SQLite database operations with error handling
2. **Notification Scheduler**: Thread-based scheduled reminders with platform-specific notifications
3. **DateTime Selector**: Independent year/month/day/hour/minute picker interface
4. **Cross-Platform Adapter**: OS-specific UI adaptations and notification systems

## 🎯 Usage

### Adding a Task
1. Type your task in the input field
2. (Optional) Set a reminder date and time using the dropdown selectors
3. Press Enter or click the "Add" button

### Setting Reminders
1. Use the dropdown selectors (Year, Month, Day, Hour, Minute) to set a specific date and time
2. The application will show a native system notification at the scheduled time
3. Notifications persist across application restarts

### Managing Tasks
- **Delete Single Task**: Select a task from the list and click "Delete"
- **Clear All Tasks**: Click "Clear All" to remove all tasks (requires confirmation)
- **Automatic Save**: All tasks are automatically saved to SQLite database

## 🔧 Development

### Project Structure
```
project-part-B/
├── main.py              # Main application (1515 lines)
├── README.md           # This file
├── pyproject.toml      # Project configuration
├── uv.lock            # Dependency lock file
├── docs/              # Documentation directory
└── openspec/          # OpenSpec specification files
```

### Code Quality
- **Formatter**: Black >= 25.11.0
- **Linter**: Ruff >= 0.14.6
- **Package Manager**: UV

### Running Tests
```bash
# No test framework implemented yet
# Manual testing recommended for GUI components
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Classes: PascalCase (e.g., `TodoListGUI`, `todolist`)
- Methods/Functions: snake_case (e.g., `add_task`, `delete_selected_task`)
- Variables: snake_case (e.g., `task_entry`, `colors`)
- UI Language: Traditional Chinese
- Formatting: Black with default settings

## 📄 License

This project is for educational purposes as part of the AMS1640 course.

## 🐛 Troubleshooting

### Common Issues:
1. **Python version too old**: Ensure Python 3.13+ is installed
2. **UV not found**: Install UV using the commands above
3. **Notification not working**: Check system notification settings
4. **Database errors**: The application will create a new database if corrupted

For more details, see the [Troubleshooting Guide](docs/operations/troubleshooting.md).

## 📞 Support

For issues and questions:
1. Check the [documentation](docs/)
2. Review existing GitHub issues
3. Create a new issue with detailed information

---

**Built with ❤️ for the AMS1640 course project**

