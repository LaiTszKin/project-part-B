# scheduled-notifications Specification

## Purpose
TBD - created by archiving change add-scheduled-notifications. Update Purpose after archive.
## Requirements
### Requirement: Scheduled Memo Notifications
系統 SHALL 提供定時通知功能，允許用戶為備忘錄項目設定特定日期時間的提醒，且通知生命週期與任務綁定。

#### Scenario: Create scheduled memo
- **WHEN** 用戶添加新備忘錄並設定日期時間
- **THEN** 系統應在指定時間觸發通知提醒用戶

#### Scenario: Display notification
- **WHEN** 預定的通知觸發時間到達
- **THEN** 系統應在用戶界面顯示Apple風格的彈出通知，包含備忘錄內容

#### Scenario: Auto-cancel notification on delete
- **WHEN** 用戶移除一個帶有預定通知的備忘錄
- **THEN** 系統應自動移除該備忘錄關聯的待觸發通知

### Requirement: DateTime Integration
備忘錄數據結構 SHALL 支持可選的日期時間資訊，並在界面上適當呈現。

#### Scenario: Add datetime to memo
- **WHEN** 用戶為備忘錄設定提醒時間
- **THEN** 系統應儲存日期時間資訊與備忘錄關聯

#### Scenario: Display memos with scheduling
- **WHEN** 主界面顯示備忘錄列表
- **THEN** 帶有預定通知的項目應顯示時間資訊

#### Scenario: Overdue warning
- **WHEN** a task has a scheduled time that is in the past
- **THEN** the task text should be displayed in red to warn the user
- **AND** the time display should also be highlighted

### Requirement: Notification Scheduling System
系統 SHALL 包含基於Python內建庫的通知調度機制。

#### Scenario: Background notification checking
- **WHEN** 應用程式執行期間
- **THEN** 系統應在背景定期檢查並觸發到期通知

#### Scenario: Application lifecycle management
- **WHEN** 應用程式關閉或重新開啟
- **THEN** 系統應適當處理預定通知的狀態

### Requirement: Date Selection Interface
The system SHALL provide a multi-selector interface for selecting notification dates, allowing users to independently choose year, month, day, hour, and minute.

#### Scenario: Select custom date and time
- **WHEN** user opens the schedule notification interface
- **THEN** five separate dropdowns should be available (Year, Month, Day, Hour, Minute)
- **AND** default values should be set to current or logical next time
- **AND** changing the month or year should automatically update the available days (e.g., leap years)

#### Scenario: Validate selection
- **WHEN** user selects a date components
- **THEN** the system should construct a valid datetime object
- **AND** invalid combinations (like Feb 30) should be prevented by the UI logic

