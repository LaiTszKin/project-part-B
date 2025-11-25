# Change: Support Windows Compatibility

## Why
The current application is designed with macOS-specific features, including AppleScript-based notifications and "SF Pro" fonts. This limits usability on Windows systems, where notifications fail or degrade to simple message boxes, and fonts may default unpredictably. To reach a wider user base, the application needs to explicitly support Windows.

## What Changes
- **Notifications:** Implement native-like notifications for Windows (using PowerShell for toast notifications or improved fallback) to match the macOS experience.
- **Typography:** Update font selection logic to use "Segoe UI" on Windows while preserving "SF Pro" on macOS.
- **Platform Detection:** Add robust platform detection to switch between macOS and Windows behaviors at runtime.

## Impact
- **Affected specs:** `scheduled-notifications`, `ui-layout`
- **Affected code:** `main.py` (specifically `NotificationScheduler` and `TodoListGUI`)
