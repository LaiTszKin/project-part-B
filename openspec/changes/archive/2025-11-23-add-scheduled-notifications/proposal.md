# Change: Add Scheduled Notifications Support

## Why
用戶希望能夠設定定時提醒，在指定的日期和時間收到通知來完成特定的備忘錄項目，提升應用程式的實用性和用戶體驗。

## What Changes
- 新增定時通知功能，允許用戶為備忘錄項目設定提醒時間
- 添加通知調度系統，使用Python內建庫實現定時功能
- 在用戶界面中集成通知顯示，採用Apple風格的彈出通知
- 擴展備忘錄數據結構以支持日期時間資訊
- 新增通知管理界面，允許用戶查看和管理預定的通知

## Impact
- Affected specs: 新增 `scheduled-notifications` 功能規範
- Affected code: 主要修改 `main.py`，新增通知調度類和GUI組件
- **BREAKING**: 需要擴展 `todolist` 類以支持帶時間的備忘錄項目