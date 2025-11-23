## MODIFIED Requirements
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
