# Troubleshooting Guide

This guide helps you diagnose and fix common issues with the Todo List Manager application.

## 🚨 Quick Troubleshooting Flow

```
Application Won't Start
├── Check Python version (≥ 3.13)
├── Check UV installation
├── Check dependencies (uv sync)
└── Check console for error messages

GUI Issues
├── Window not appearing
├── Text rendering problems
├── Button clicks not working
└── Layout problems

Database Issues
├── Tasks not saving
├── Tasks not loading
├── Database corruption
└── Permission errors

Notification Issues
├── Notifications not showing
├── Wrong notification time
├── Notification duplicates
└── Platform-specific problems
```

## 🔧 Installation Problems

### Python Version Error

**Symptoms:**
```
Error: Python 3.13 or higher is required
Current version: 3.11.0
```

**Solution:**
1. **Check current version:**
   ```bash
   python --version
   # or
   python3 --version
   ```

2. **Install Python 3.13+:**
   - **Windows**: Download from [python.org](https://python.org)
   - **macOS**: `brew install python@3.13`
   - **Linux**: Use distribution package manager

3. **Verify installation:**
   ```bash
   python3.13 --version
   ```

### UV Not Found

**Symptoms:**
```
command not found: uv
uv: command not found
```

**Solution:**

**Windows:**
```powershell
# Reinstall UV
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Add to PATH (if needed)
$env:Path += ";$env:USERPROFILE\.cargo\bin"
```

**macOS/Linux:**
```bash
# Reinstall UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Reload shell
source ~/.bashrc  # or ~/.zshrc
```

### Module Import Errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'tkinter'
ImportError: cannot import name 'sqlite3'
```

**Solution:**

**Tkinter missing (Windows):**
1. Reinstall Python with "tcl/tk and IDLE" option checked
2. Or install manually: `pip install tk`

**Tkinter missing (macOS):**
```bash
# Install Python with Tkinter
brew install python-tk
```

**Tkinter missing (Linux):**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora/RHEL
sudo dnf install python3-tkinter
```

## 🖥️ GUI Issues

### Window Not Appearing

**Symptoms:**
- Application starts but no window appears
- Process runs but nothing visible
- Console shows no errors

**Solution:**
1. **Check Tkinter installation:**
   ```bash
   python -c "import tkinter; print('Tkinter available')"
   ```

2. **Run with debug output:**
   ```bash
   uv run main.py 2>&1 | grep -i error
   ```

3. **Check display server (Linux):**
   ```bash
   echo $DISPLAY
   # Should show :0 or similar
   ```

4. **Try software rendering:**
   ```bash
   export TK_SILENCE_DEPRECATION=1
   uv run main.py
   ```

### Text Rendering Issues

**Symptoms:**
- Chinese text shows as boxes or gibberish
- Font appears incorrectly
- Text overlapping or cut off

**Solution:**

**Chinese font issues:**
1. **Windows**: Install "Microsoft JhengHei" font
2. **macOS**: Ensure "PingFang TC" is available
3. **Linux**: Install Chinese font package:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install fonts-noto-cjk

   # Fedora/RHEL
   sudo dnf install google-noto-sans-cjk-fonts
   ```

**Font configuration override:**
Modify font settings in `main.py`:
```python
# Find font configuration and change to:
font = ("Helvetica", 12)  # Fallback font
```

### Button Clicks Not Working

**Symptoms:**
- Buttons don't respond to clicks
- No visual feedback when clicked
- Console shows no errors

**Solution:**
1. **Check event bindings:**
   - Verify button commands are connected
   - Check for typos in function names

2. **Test with simple example:**
   ```python
   # Add debug print to button command
   def test_button():
       print("Button clicked!")
   ```

3. **Check focus:**
   - Ensure window has focus
   - Try clicking title bar first

### Layout Problems

**Symptoms:**
- Widgets overlapping
- Window size incorrect
- Scrollbars not appearing

**Solution:**
1. **Reset window geometry:**
   ```python
   # In main.py, try changing:
   self.master.geometry("500x400")
   ```

2. **Check weight configuration:**
   - Ensure `grid_rowconfigure` and `grid_columnconfigure` are set
   - Verify weight values (usually 1)

3. **Platform-specific adjustments:**
   - Different platforms may need different padding
   - Test on target platform

## 💾 Database Issues

### Tasks Not Saving

**Symptoms:**
- Tasks disappear after restart
- No database file created
- Console shows database errors

**Solution:**

**Check database location:**
```python
# Add debug print in TaskRepository.__init__
print(f"Database path: {db_path}")
```

**Common locations:**
- **Windows**: `C:\Users\YourName\AppData\Roaming\todo_app.db`
- **macOS**: `~/Library/Application Support/todo_app.db`
- **Linux**: `~/.local/share/todo_app.db`

**Permission issues:**
```bash
# Check write permissions
ls -la ~/.local/share/  # Linux/macOS
dir %APPDATA%           # Windows
```

### Database Corruption

**Symptoms:**
```
sqlite3.DatabaseError: database disk image is malformed
sqlite3.OperationalError: unable to open database file
```

**Solution:**
1. **Backup corrupted database:**
   ```bash
   cp ~/.local/share/todo_app.db ~/.local/share/todo_app.db.backup
   ```

2. **Delete corrupted database:**
   ```bash
   rm ~/.local/share/todo_app.db
   ```

3. **Application will create new database** on next start

**Note**: Data loss may occur. The application doesn't have backup/restore features.

### Database Locking Issues

**Symptoms:**
```
sqlite3.OperationalError: database is locked
```

**Solution:**
1. **Close other instances**: Ensure only one app instance is running
2. **Check for zombie processes**: Kill any hanging Python processes
3. **Wait and retry**: Lock may clear automatically

## 🔔 Notification Issues

### Notifications Not Showing

**Symptoms:**
- Reminder time passes but no notification
- No error messages
- Task has reminder icon

**Solution:**

**Platform-specific checks:**

**macOS:**
```bash
# Check notification permissions
defaults read com.apple.notificationcenterui

# Test AppleScript notification
osascript -e 'display notification "Test" with title "Todo List"'
```

**Windows:**
- Check Action Center settings
- Ensure "Get notifications from apps and other senders" is ON
- Test with other apps that use notifications

**Linux:**
```bash
# Check notify-send installation
which notify-send

# Test notification
notify-send "Test" "Todo List notification"
```

**Application-level debugging:**
1. **Check scheduler thread:**
   - Verify `NotificationScheduler` is running
   - Check console for scheduler errors

2. **Verify reminder times:**
   - Check database for correct reminder values
   - Ensure timezone is handled correctly

### Wrong Notification Time

**Symptoms:**
- Notifications at wrong time
- Timezone issues
- Off by one hour

**Solution:**
1. **Check system time:**
   ```bash
   date  # Linux/macOS
   # Should show correct local time
   ```

2. **Timezone handling:**
   - Application uses local system time
   - No timezone conversion performed
   - Ensure system timezone is correct

3. **Database time values:**
   - Verify year/month/day/hour/minute values in database
   - Check for off-by-one errors (e.g., month 0-11 vs 1-12)

### Notification Duplicates

**Symptoms:**
- Multiple notifications for same task
- Notifications repeating

**Solution:**
1. **Check scheduler logic:**
   - `NotificationScheduler` should mark notifications as sent
   - Verify duplicate detection logic

2. **Database state:**
   - Check for duplicate task entries
   - Verify task IDs are unique

## 🔄 Application Behavior Issues

### Slow Performance

**Symptoms:**
- UI lag when adding/deleting tasks
- High CPU usage
- Slow startup

**Solution:**

**With many tasks (>100):**
1. **Task loading optimization:**
   - Application loads all tasks at startup
   - Consider pagination for very large lists

2. **Notification scheduler:**
   - Checks every second (configurable)
   - With many reminders, may cause CPU usage

**Diagnostic steps:**
```bash
# Check memory usage
top | grep python  # Linux/macOS
tasklist | findstr python  # Windows

# Profile with cProfile
python -m cProfile -o profile.stats main.py
```

### High Memory Usage

**Symptoms:**
- Memory grows over time
- Application becomes slow
- Possible memory leak

**Solution:**
1. **Check for circular references**
2. **Verify proper cleanup in `__del__` methods**
3. **Monitor with memory profiler**

### Application Crashes

**Symptoms:**
- Unexpected exit
- Segmentation fault
- GUI disappears suddenly

**Solution:**
1. **Run with debug output:**
   ```bash
   uv run main.py 2>&1 | tee debug.log
   ```

2. **Check system logs:**
   ```bash
   # macOS/Linux
   dmesg | tail -20

   # Windows Event Viewer
   eventvwr.msc
   ```

3. **Common crash causes:**
   - Tkinter compatibility issues
   - Database corruption
   - Memory exhaustion
   - Platform-specific bugs

## 🌐 Cross-Platform Issues

### Platform Detection Failures

**Symptoms:**
- Wrong fonts or notifications for platform
- Path separator errors
- Platform-specific features not working

**Solution:**
1. **Check `get_current_platform()` function**
2. **Verify platform string detection logic**
3. **Test on actual target platform**

### Path Separator Issues

**Symptoms:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'C:\Users\...\todo_app.db'
```

**Solution:**
- Application uses `os.path.join()` for cross-platform paths
- Verify path construction logic
- Check for hardcoded path separators (`/` or `\`)

### Line Ending Issues (Git)

**Symptoms:**
- Script errors on Windows/Linux
- `^M` characters in output
- Shebang line problems

**Solution:**
```bash
# Configure Git for cross-platform
git config --global core.autocrlf input

# Fix existing files
dos2unix main.py  # Linux/macOS
# or
unix2dos main.py  # Windows
```

## 📊 Diagnostic Tools

### Debug Mode

Add debug prints to `main.py`:
```python
# Enable debug mode
DEBUG = True

def debug_print(message):
    if DEBUG:
        print(f"[DEBUG] {message}")

# Use in code
debug_print(f"Adding task: {task_text}")
```

### Logging Configuration

For better diagnostics, add logging:
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='todo_app.log'
)

logger = logging.getLogger(__name__)
logger.debug("Application started")
```

### Database Inspection

**Examine database contents:**
```bash
# Using sqlite3 command line
sqlite3 ~/.local/share/todo_app.db

# Inside sqlite3:
.tables
SELECT * FROM tasks;
.schema
```

## 🔍 Advanced Troubleshooting

### Threading Issues

**Symptoms:**
- GUI freezing
- Notifications stopping
- Race conditions

**Solution:**
1. **Check `NotificationScheduler` thread:**
   - Verify it's running as daemon
   - Check for unhandled exceptions in thread

2. **GUI thread safety:**
   - All GUI updates must be in main thread
   - Use `after()` for thread-to-GUI communication

### Memory Leak Detection

**Tools:**
- **Python**: `tracemalloc`, `objgraph`
- **System**: `top`, `htop`, Task Manager
- **Manual**: Monitor memory growth over time

**Common leak sources:**
- Unclosed database connections
- Circular references in GUI objects
- Event handler accumulations

### Performance Profiling

**CPU Profiling:**
```bash
python -m cProfile -o profile.stats main.py
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('time').print_stats(20)"
```

**Memory Profiling:**
```bash
# Install memory_profiler first
uv pip install memory_profiler

# Profile specific function
python -m memory_profiler main.py
```

## 📞 Getting Help

### Information to Provide

When asking for help, include:

1. **Platform**: Windows/macOS/Linux + version
2. **Python Version**: `python --version`
3. **Error Messages**: Full traceback
4. **Steps to Reproduce**: Exact steps
5. **What You've Tried**: Troubleshooting steps attempted

### Support Channels

1. **GitHub Issues**: Primary support channel
2. **Documentation**: Check this guide first
3. **Code Inspection**: Review `main.py` for known issues

### Known Limitations

- **No backup/restore**: Database corruption causes data loss
- **Single instance**: Multiple instances may cause database locks
- **No cloud sync**: Local storage only
- **Basic error recovery**: Some errors may crash application

---

**Still stuck?** Create a detailed issue on GitHub with all the information above.