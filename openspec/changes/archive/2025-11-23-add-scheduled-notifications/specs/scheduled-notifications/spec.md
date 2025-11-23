## ADDED Requirements

### Requirement: Scheduled Memo Notifications
系統 SHALL 提供定時通知功能，允許用戶為備忘錄項目設定特定日期時間的提醒。

#### Scenario: Create scheduled memo
- **WHEN** 用戶添加新備忘錄並設定日期時間
- **THEN** 系統應在指定時間觸發通知提醒用戶

#### Scenario: Display notification
- **WHEN** 預定的通知觸發時間到達
- **THEN** 系統應在用戶界面顯示Apple風格的彈出通知，包含備忘錄內容

#### Scenario: Manage scheduled notifications
- **WHEN** 用戶查看通知管理界面
- **THEN** 系統應顯示所有預定的通知列表，包括時間和備忘錄內容

#### Scenario: Cancel scheduled notification
- **WHEN** 用戶選擇取消特定的預定通知
- **THEN** 系統應移除該通知且不再觸發

### Requirement: DateTime Integration
備忘錄數據結構 SHALL 支持可選的日期時間資訊。

#### Scenario: Add datetime to memo
- **WHEN** 用戶為備忘錄設定提醒時間
- **THEN** 系統應儲存日期時間資訊與備忘錄關聯

#### Scenario: Display memos with scheduling
- **WHEN** 主界面顯示備忘錄列表
- **THEN** 帶有預定通知的項目應顯示時間資訊

### Requirement: Notification Scheduling System
系統 SHALL 包含基於Python內建庫的通知調度機制。

#### Scenario: Background notification checking
- **WHEN** 應用程式執行期間
- **THEN** 系統應在背景定期檢查並觸發到期通知

#### Scenario: Application lifecycle management
- **WHEN** 應用程式關閉或重新開啟
- **THEN** 系統應適當處理預定通知的狀態