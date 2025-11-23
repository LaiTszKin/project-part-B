# Change: Merge Task and Notification Management

## Why
Simplify the user workflow by coupling notification lifecycle directly to tasks. Users currently have a separate "Notification Management" interface which is redundant if notifications are automatically managed with their parent tasks.

## What Changes
- Remove the standalone "Notification Management" interface and button.
- Enforce that deleting a task automatically cancels its associated notification.
- Update specifications to remove the requirement for a notification management view.

## Impact
- **Specs**: `scheduled-notifications`
- **Code**: `main.py` (Remove `show_notification_manager` and related UI elements)
