# Architecture Overview

This document describes the system architecture of the Todo List Manager application, including design patterns, component interactions, and technical implementation details.

## 🏗️ System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│                    GUI Layer (Tkinter)              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │ TodoListGUI │  │  DateTime   │  │   Event     │ │
│  │   Class     │◄─┤  Selector   │  │  Handlers   │ │
│  └─────────────┘  └─────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────┐
│               Business Logic Layer                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │  todolist   │  │ Notification│  │ Platform    │ │
│  │   Class     │  │  Scheduler  │  │  Adapter    │ │
│  └─────────────┘  └─────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────┐
│               Data Access Layer                      │
│  ┌───────────────────────────────────────────────┐  │
│  │            TaskRepository Class               │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐       │  │
│  │  │  CRUD   │  │  Error  │  │  DB     │       │  │
│  │  │  Ops    │  │ Handling│  │  Schema │       │  │
│  │  └─────────┘  └─────────┘  └─────────┘       │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────┐
│               Persistence Layer                      │
│            ┌─────────────────────┐                  │
│            │   SQLite Database   │                  │
│            │    (todo_app.db)    │                  │
│            └─────────────────────┘                  │
└─────────────────────────────────────────────────────┘
```

### Architecture Style: MVC-inspired

The application follows an **MVC-inspired** (Model-View-Controller) pattern:

- **Model**: `todolist` class + `TaskRepository` for data management
- **View**: `TodoListGUI` class for user interface
- **Controller**: Event handlers within the GUI class

## 📦 Core Components

### 1. GUI Layer (`TodoListGUI` Class)

**Responsibilities:**
- Create and manage Tkinter window and widgets
- Handle user input and events
- Update UI based on application state
- Provide visual feedback to users

**Key Methods:**
- `__init__()`: Initialize GUI components
- `add_task()`: Handle task addition
- `delete_selected_task()`: Handle task deletion
- `clear_all_tasks()`: Handle bulk deletion
- `update_day_dropdown()`: Dynamic day selection

**UI Components:**
- `task_entry`: Text input field
- `task_listbox`: Scrollable task list
- `year_var`, `month_var`, etc.: Date/time selection variables
- `add_button`, `delete_button`, `clear_button`: Action buttons

### 2. Business Logic Layer

#### `todolist` Class
**Responsibilities:**
- Coordinate between GUI and data layer
- Manage task lifecycle
- Validate task data
- Handle business rules

**Key Methods:**
- `add_task()`: Validate and add new task
- `delete_task()`: Remove existing task
- `get_all_tasks()`: Retrieve all tasks
- `clear_all_tasks()`: Remove all tasks

#### `NotificationScheduler` Class
**Responsibilities:**
- Schedule and manage timed notifications
- Platform-specific notification delivery
- Thread management for background scheduling
- Notification persistence across restarts

**Key Methods:**
- `start()`: Start scheduler thread
- `stop()`: Stop scheduler thread
- `schedule_notification()`: Schedule new reminder
- `check_notifications()`: Check for due notifications

### 3. Data Access Layer (`TaskRepository` Class)

**Responsibilities:**
- SQLite database operations
- Data persistence and retrieval
- Error handling and recovery
- Database schema management

**Key Methods:**
- `__init__()`: Initialize database connection
- `add_task()`: Insert new task
- `delete_task()`: Remove task by ID
- `get_all_tasks()`: Retrieve all tasks
- `clear_all_tasks()`: Remove all tasks
- `close()`: Clean up database connection

**Database Schema:**
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_text TEXT NOT NULL,
    reminder_year INTEGER,
    reminder_month INTEGER,
    reminder_day INTEGER,
    reminder_hour INTEGER,
    reminder_minute INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Platform Adapter Layer

**Responsibilities:**
- Detect current operating system
- Provide platform-specific implementations
- Handle cross-platform compatibility issues

**Key Functions:**
- `get_current_platform()`: Detect macOS/Windows/Linux
- `send_notification()`: Platform-specific notification delivery
- Platform-specific font configuration

## 🔄 Data Flow

### Task Addition Flow
```
1. User types task in input field → GUI Layer
2. User sets date/time (optional) → GUI Layer
3. User clicks Add or presses Enter → Event Handler
4. Validate input → Business Logic
5. Save to database → Data Access Layer
6. Schedule notification (if set) → Notification Scheduler
7. Update UI list → GUI Layer
8. Clear input field → GUI Layer
```

### Task Deletion Flow
```
1. User selects task → GUI Layer
2. User clicks Delete → Event Handler
3. Remove from database → Data Access Layer
4. Cancel scheduled notification → Notification Scheduler
5. Update UI list → GUI Layer
```

### Notification Flow
```
1. Notification Scheduler thread runs every second
2. Check database for due notifications → Data Access Layer
3. Retrieve task details → Business Logic
4. Send platform-specific notification → Platform Adapter
5. Log notification delivery → Application Log
```

## 🧵 Concurrency Model

### Threading Strategy
- **Main Thread**: GUI event loop (Tkinter mainloop)
- **Worker Thread**: Notification scheduler (runs every second)
- **No Background Threads**: Database operations run on main thread

### Thread Safety
- **Database Access**: SQLite connections are thread-local
- **GUI Updates**: All GUI operations on main thread
- **Notification Scheduling**: Thread-safe scheduling queue

### Notification Scheduler Implementation
```python
class NotificationScheduler(threading.Thread):
    def __init__(self, task_repository):
        super().__init__(daemon=True)
        self.task_repository = task_repository
        self.running = True

    def run(self):
        while self.running:
            self.check_notifications()
            time.sleep(1)  # Check every second

    def check_notifications(self):
        # Get current time
        # Query database for due notifications
        # Send notifications for due tasks
```

## 💾 Persistence Design

### Database Strategy
- **SQLite**: Lightweight, serverless, cross-platform
- **Single File**: `todo_app.db` in user data directory
- **Automatic Setup**: Schema created on first run
- **Error Recovery**: New database created if corrupted

### Data Location by Platform
```
Windows:    %APPDATA%\todo_app.db
macOS:      ~/Library/Application Support/todo_app.db
Linux:      ~/.local/share/todo_app.db
```

### Schema Evolution
- **Current**: v1.0 (tasks table with reminder fields)
- **Migration**: Not implemented (recreate if schema changes)
- **Backward Compatibility**: Not maintained (educational project)

## 🔌 Platform Integration

### Notification Systems

**macOS:**
```python
def send_notification_macos(title, message):
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(['osascript', '-e', script])
```

**Windows:**
```python
def send_notification_windows(title, message):
    # Uses win10toast or similar Windows notification API
    toast = ToastNotifier()
    toast.show_toast(title, message, duration=5)
```

**Linux:**
```python
def send_notification_linux(title, message):
    subprocess.run(['notify-send', title, message])
```

### Font Configuration

**Platform-specific Font Selection:**
```python
def get_platform_font():
    platform = get_current_platform()
    if platform == 'macos':
        return 'PingFang TC'  # Apple's Chinese font
    elif platform == 'windows':
        return 'Microsoft JhengHei'  # Windows Chinese font
    else:  # linux
        return None  # Use system default
```

## 🛡️ Error Handling Strategy

### Error Categories

1. **Database Errors** (SQLite operational errors)
   - Action: Create new database, log error
   - User Impact: Potential data loss, silent recovery

2. **Notification Errors** (Platform notification failures)
   - Action: Log error, continue execution
   - User Impact: Missed notifications

3. **GUI Errors** (Tkinter exceptions)
   - Action: Show error in console, attempt recovery
   - User Impact: Possible UI glitches

4. **File System Errors** (Permission/access issues)
   - Action: Use fallback location, log error
   - User Impact: Different storage location

### Recovery Mechanisms
- **Database Corruption**: Auto-recreate with clean state
- **Notification Failure**: Skip failed notification, continue
- **GUI Crash**: Application exits with error code
- **File Permission Issues**: Use temporary directory fallback

## 📈 Scalability Considerations

### Current Limitations
- **Single User**: Designed for individual use
- **Local Storage**: No cloud sync or backup
- **No Concurrency**: Single instance at a time
- **Memory Usage**: All tasks loaded into memory

### Potential Extensions
1. **Multi-user Support**: User accounts and authentication
2. **Cloud Sync**: Remote backup and multi-device sync
3. **Advanced Notifications**: Recurring reminders, priority levels
4. **Data Export**: CSV, JSON, or iCal export
5. **Plugin System**: Extensible feature architecture

## 🔍 Code Organization

### Single-File Architecture
```
main.py (1515 lines)
├── Imports and Constants
├── Platform Detection Functions
├── TaskRepository Class (Data Layer)
├── NotificationScheduler Class (Business Logic)
├── todolist Class (Business Logic)
├── TodoListGUI Class (GUI Layer)
└── Main Execution Block
```

### Advantages:
- **Simplicity**: Easy to understand and maintain
- **Portability**: Single file distribution
- **No Dependencies**: Only Python standard library

### Disadvantages:
- **Size**: Large file (1500+ lines)
- **Coupling**: Tight coupling between components
- **Testability**: Harder to unit test individual components

## 🎯 Design Decisions

### Why Tkinter?
- **Standard Library**: No external dependencies
- **Cross-platform**: Works on Windows, macOS, Linux
- **Simple**: Easy to learn and use
- **Lightweight**: Low resource consumption

### Why SQLite?
- **Zero Configuration**: No server setup required
- **Single File**: Easy backup and distribution
- **ACID Compliant**: Reliable data storage
- **Python Integration**: Built-in `sqlite3` module

### Why Thread-based Notifications?
- **Responsive GUI**: Main thread not blocked
- **Simple Implementation**: Easy to understand
- **Reliable**: Regular checks ensure no missed notifications

## 📚 Related Documentation

- [Main README](../README.md) - Quick start and overview
- [Features Guide](../features/README.md) - User-facing features
- [Development Guide](../development/README.md) - Contributor guidelines
- [OpenSpec Specifications](../../openspec/) - Specification documents

---

**Next**: Learn how to contribute to development in the [Development Guide](../development/README.md)