# Getting Started

This guide will help you install and run the Todo List Manager application on your system.

## 📋 Prerequisites

### Python Requirements
- **Python 3.13 or higher** is required
- Check your Python version:
  ```bash
  python --version
  # or
  python3 --version
  ```

### Package Manager (Recommended)
- **UV** - Modern Python package manager (recommended)
- **pip** - Traditional Python package manager (alternative)

## 🛠️ Installation

### Step 1: Install UV (Recommended)

**Windows:**
```powershell
# Run in PowerShell as Administrator
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
# Run in terminal
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Verify UV installation:**
```bash
uv --version
```

### Step 2: Get the Source Code

**Option A: Clone from GitHub (Recommended)**
```bash
git clone https://github.com/Yamiyorunoshura/project-part-B.git
cd project-part-B
```

**Option B: Download ZIP**
1. Visit the [GitHub repository](https://github.com/Yamiyorunoshura/project-part-B)
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file to your preferred location

### Step 3: Install Dependencies

```bash
# Navigate to project directory
cd project-part-B

# Sync dependencies with UV
uv sync
```

This command will:
- Create a virtual environment
- Install required packages
- Generate lock file

### Step 4: Run the Application

```bash
# Run with UV
uv run main.py
```

Or activate the virtual environment first:
```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Run the application
python main.py
```

## 🚀 First Run

When you first run the application:

1. **Main Window**: The application window will open with a clean, Apple-style interface
2. **Database Setup**: A SQLite database will be created automatically in your user data directory
3. **Empty Task List**: The task list will be empty initially
4. **UI Language**: Interface is in Traditional Chinese

### Expected First Screen:
```
+----------------------------------------+
|  Todo List Manager                    |
|                                        |
|  [Input field]              [Add]     |
|                                        |
|  Year: [2025]  Month: [12]  Day: [5]  |
|  Hour: [00]    Minute: [00]           |
|                                        |
|  [Empty task list]                    |
|                                        |
|  [Delete]        [Clear All]          |
+----------------------------------------+
```

## 📁 Project Structure

After installation, your project directory should look like:
```
project-part-B/
├── main.py              # Main application (1515 lines)
├── README.md           # Project overview
├── pyproject.toml      # Project configuration
├── uv.lock            # Dependency lock file
├── .venv/             # Virtual environment (created by uv sync)
├── docs/              # Documentation directory
└── openspec/          # OpenSpec specification files
```

## 🔧 Alternative Installation Methods

### Using pip (Without UV)

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Install dependencies
pip install -e .
```

### Running Without Virtual Environment (Not Recommended)

```bash
# Install dependencies globally
pip install .

# Run application
python main.py
```

**⚠️ Warning**: Installing globally may cause dependency conflicts with other Python projects.

## 🌐 Platform-Specific Notes

### Windows
- **Notification System**: Uses Windows Toast notifications
- **Font Rendering**: Automatically selects appropriate Chinese font
- **Path Separators**: Uses backslashes in file paths

### macOS
- **Notification System**: Uses AppleScript for native notifications
- **Font Rendering**: Uses "PingFang TC" for Chinese text
- **Window Management**: Follows macOS window conventions

### Linux
- **Notification System**: Uses fallback notification method
- **Font Rendering**: Uses system default Chinese font
- **XDG Compliance**: Stores data in XDG directories

## ✅ Verification

To verify your installation is working correctly:

1. **Run the application**: `uv run main.py`
2. **Add a test task**: Type "Test task" and press Enter
3. **Check database**: Look for `.todo_app.db` in your user data directory
4. **Test notification**: Set a reminder for 1 minute in the future

## 🐛 Troubleshooting Installation

### Common Issues:

**1. Python version error:**
```
Error: Python 3.13 or higher is required
```
**Solution**: Install Python 3.13+ from [python.org](https://python.org)

**2. UV not found:**
```
command not found: uv
```
**Solution**: Reinstall UV or add to PATH

**3. Module import errors:**
```
ModuleNotFoundError: No module named 'tkinter'
```
**Solution**: Install Tkinter for your Python distribution

**4. Database creation errors:**
```
sqlite3.OperationalError: unable to open database file
```
**Solution**: Check write permissions in user data directory

For more troubleshooting help, see the [Troubleshooting Guide](../operations/troubleshooting.md).

## 🎉 Next Steps

Now that you have the application installed:
1. Learn how to use features in the [Features Guide](../features/README.md)
2. Explore the system design in [Architecture](../architecture/README.md)
3. Contribute to development with the [Development Guide](../development/README.md)