## MODIFIED Requirements
### Requirement: Scheduled Memo Notifications
系統 SHALL 提供跨平台定時通知功能，允許用戶為備忘錄項目設定特定日期時間的提醒，且通知生命週期與任務綁定。

#### Scenario: Create scheduled memo
- **WHEN** 用戶添加新備忘錄並設定日期時間
- **THEN** 系統應在指定時間觸發通知提醒用戶

#### Scenario: Display notification
- **WHEN** 預定的通知觸發時間到達
- **THEN** 系統應顯示該平台的原生風格通知（macOS使用AppleScript，Windows使用Toast，Linux使用Fallback）
- **AND** 通知應包含備忘錄內容

#### Scenario: Auto-cancel notification on delete
- **WHEN** 用戶移除一個帶有預定通知的備忘錄
- **THEN** 系統應自動移除該備忘錄關聯的待觸發通知

## ADDED Requirements
### Requirement: Windows Notification Support
The system SHALL support native-like notifications on Windows using PowerShell or appropriate system calls.

#### Scenario: Windows Toast Notification
- **WHEN** a notification is triggered on a Windows system
- **THEN** the system should attempt to show a Toast notification
- **AND** if Toast fails, it should fall back to a reliable method (e.g., Tray balloon or Message Box)
