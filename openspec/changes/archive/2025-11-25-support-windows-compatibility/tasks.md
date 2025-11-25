## 1. Platform Detection & Foundation
- [x] 1.1 Update `main.py` to include reliable platform detection (macOS vs Windows vs Linux).
- [x] 1.2 Create `NotificationStrategy` abstract base class or interface for handling platform differences.

## 2. Notifications
- [x] 2.1 Implement `WindowsNotificationStrategy` using PowerShell for toast notifications (native feel).
- [x] 2.2 Enhance `FallbackNotificationStrategy` to be the default for unsupported platforms.
- [x] 2.3 Update `NotificationScheduler` to use the correct strategy based on detected platform.
- [x] 2.4 Verify `MacOSNotificationStrategy` (existing logic) is preserved and works.

## 3. UI & Typography
- [x] 3.1 Create a font configuration dictionary that maps UI elements to platform-specific fonts.
- [x] 3.2 Update `TodoListGUI.__init__` to use the font configuration (SF Pro for Mac, Segoe UI for Windows).
- [x] 3.3 Verify window sizing and padding look correct on Windows (adjust if necessary based on manual testing).

## 4. Verification
- [x] 4.1 Test notifications on Windows (if environment available) or simulate Windows path.
- [x] 4.2 Test font loading fallback logic.
