# Features Guide

This guide explains all the features of the Todo List Manager application with detailed usage instructions.

## 🏠 Main Interface

The application has a clean, minimalist interface with the following components:

```
+-------------------------------------------------+
|  Todo List Manager                             |
|                                                 |
|  [Task input field]                 [Add]      |
|                                                 |
|  Year: [2025]  Month: [12]  Day: [5]           |
|  Hour: [00]    Minute: [00]                    |
|                                                 |
|  • Task 1                                      |
|  • Task 2 with reminder                        |
|  • Task 3                                      |
|                                                 |
|  [Delete]               [Clear All]            |
+-------------------------------------------------+
```

### Interface Elements:
1. **Title Bar**: "Todo List Manager"
2. **Task Input Field**: Text field for entering new tasks
3. **Add Button**: Adds the task from the input field
4. **Date/Time Selectors**: Five dropdowns for setting reminders
5. **Task List**: Scrollable list of all tasks
6. **Delete Button**: Deletes selected task
7. **Clear All Button**: Removes all tasks (with confirmation)

## 📝 Task Management

### Adding Tasks

**Method 1: Using Add Button**
1. Type your task in the input field
2. Click the "Add" button (or press Enter)
3. The task appears in the list below

**Method 2: Keyboard Shortcut**
1. Type your task in the input field
2. Press `Enter` key
3. The task is added automatically

**Example:**
```
Input: "Buy groceries"
Action: Press Enter or click Add
Result: "Buy groceries" appears in task list
```

### Task Display Format

Tasks are displayed with the following information:
- **Task text**: The description you entered
- **Reminder indicator**: ⏰ icon if a reminder is set
- **Reminder time**: Displayed in parentheses if set

**Examples:**
```
• Buy groceries
• Call dentist ⏰ (2025-12-10 14:30)
• Finish report
```

### Deleting Tasks

**Delete Single Task:**
1. Select a task from the list by clicking on it
2. Click the "Delete" button
3. The task is removed immediately

**Keyboard Alternative:**
1. Select a task
2. Press `Delete` key on your keyboard

### Clearing All Tasks

**Bulk Deletion:**
1. Click the "Clear All" button
2. A confirmation dialog appears:
   ```
   Are you sure you want to delete all tasks?
   [Cancel] [Confirm]
   ```
3. Click "Confirm" to delete all tasks
4. Click "Cancel" to abort the operation

**⚠️ Warning**: This action cannot be undone. All tasks will be permanently deleted.

## ⏰ Scheduled Notifications

### Setting Reminders

The application provides five independent dropdown selectors for precise date/time selection:

1. **Year**: Current year and next year options
2. **Month**: 1-12 (January-December)
3. **Day**: 1-31 (automatically adjusts based on month/year)
4. **Hour**: 00-23 (24-hour format)
5. **Minute**: 00-59

**To set a reminder:**
1. Select Year from the first dropdown
2. Select Month from the second dropdown
3. Select Day from the third dropdown (options update based on month/year)
4. Select Hour from the fourth dropdown
5. Select Minute from the fifth dropdown
6. Add your task as usual

**Example:**
```
Task: "Team meeting"
Date/Time: 2025-12-15 14:30
Steps: Year=2025, Month=12, Day=15, Hour=14, Minute=30
Result: Task added with reminder set for December 15, 2025 at 2:30 PM
```

### Notification Behavior

**When a reminder triggers:**
1. A native system notification appears
2. Notification includes task text and scheduled time
3. Notification persists according to system settings
4. The task remains in your list

**Platform-specific notifications:**
- **macOS**: AppleScript notification with sound
- **Windows**: Toast notification with action buttons
- **Linux**: Fallback notification using `notify-send`

**Example Notification:**
```
Todo List Reminder
Team meeting
Scheduled: 2025-12-15 14:30
```

### Reminder Management

**Viewing Set Reminders:**
- Tasks with reminders show ⏰ icon
- Hover over task to see reminder time tooltip
- Reminder time displayed in parentheses

**Editing Reminders:**
Currently, reminders cannot be edited directly. To change a reminder:
1. Delete the existing task
2. Create a new task with the corrected reminder time

**Reminder Persistence:**
- Reminders are saved to the database
- Survive application restart
- Automatically rescheduled when application starts

## 💾 Data Persistence

### Automatic Saving

The application automatically saves:
- **All tasks** (with text and reminder times)
- **Database schema** (created on first run)
- **Application state**

**Save Locations:**
- **Windows**: `%APPDATA%\todo_app.db`
- **macOS**: `~/Library/Application Support/todo_app.db`
- **Linux**: `~/.local/share/todo_app.db`

### Database Features

**SQLite Database Structure:**
```sql
-- Tasks table
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

**Automatic Recovery:**
- If database is corrupted, a new one is created
- No data loss notification (for simplicity)
- Previous data may be lost if corrupted

## ⌨️ Keyboard Support

### Global Shortcuts

| Key | Action | Description |
|-----|--------|-------------|
| `Enter` | Add Task | Adds task from input field |
| `Delete` | Delete Task | Deletes selected task |
| `Ctrl+C` | Copy | Standard copy (text selection) |
| `Ctrl+V` | Paste | Standard paste |

### Field Navigation

1. **Task Input Field**: Automatically focused on startup
2. **Task List**: Use mouse click or arrow keys to select
3. **Dropdowns**: Use mouse or Tab key to navigate

### Accessibility Features
- **Tab navigation** between controls
- **Keyboard shortcuts** for common actions
- **Clear visual feedback** for selections
- **High contrast** color scheme (Apple-style)

## 🌍 Cross-Platform Features

### Platform Adaptations

**User Interface:**
- **Fonts**: Platform-appropriate Chinese fonts
- **Window Controls**: Native look and feel
- **Color Scheme**: Consistent across platforms

**File System:**
- **Paths**: Platform-specific path separators
- **Data Storage**: Follows platform conventions
- **Configuration**: No configuration files needed

**Notifications:**
- Uses native notification systems
- Platform-appropriate styling
- Consistent user experience

### Platform-Specific Details

**Windows:**
- Toast notifications with action center integration
- Segoe UI font for Chinese text
- Windows-style window controls

**macOS:**
- AppleScript notifications with sound
- PingFang TC font for Chinese text
- macOS-style window controls

**Linux:**
- `notify-send` command for notifications
- System default Chinese font
- XDG-compliant data storage

## 🔄 Application Lifecycle

### Startup Sequence
1. Check Python version (must be 3.13+)
2. Initialize database connection
3. Load saved tasks from database
4. Reschedule saved reminders
5. Create and display GUI window
6. Focus on task input field

### Shutdown Sequence
1. User closes window
2. Database connection closed
3. Notification scheduler stopped
4. Application exits cleanly

### Error Handling
- **Database errors**: Create new database
- **Notification errors**: Log error, continue running
- **GUI errors**: Show error message in console
- **File permission errors**: Use fallback location

## 🎨 Design Philosophy

### Apple-Style Design Principles
- **Minimalism**: Clean, uncluttered interface
- **Consistency**: Predictable behavior across features
- **Accessibility**: Keyboard support and clear visuals
- **Performance**: Responsive even with many tasks

### Color Scheme
- **Background**: Light gray (#f5f5f7)
- **Text**: Dark gray (#1d1d1f)
- **Accent**: Blue (#007AFF)
- **Buttons**: Subtle gradients and shadows

### Typography
- **Chinese Text**: Platform-appropriate Chinese font
- **Readability**: Clear contrast and spacing
- **Hierarchy**: Visual distinction between elements

## 📱 Mobile Considerations

While this is a desktop application, the design considers:
- **Touch-friendly** button sizes (where applicable)
- **Clear visual feedback** for interactions
- **Responsive layout** for different window sizes

---

**Next**: Learn about the system architecture in the [Architecture Guide](../architecture/README.md)