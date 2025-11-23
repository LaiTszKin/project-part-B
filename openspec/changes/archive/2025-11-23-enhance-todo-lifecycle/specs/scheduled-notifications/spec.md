## MODIFIED Requirements
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
