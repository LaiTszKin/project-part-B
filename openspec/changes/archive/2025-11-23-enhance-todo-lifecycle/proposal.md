# Change: Enhance Todo Lifecycle (Completion & Overdue)

## Why
Users need a more intuitive way to mark tasks as done directly from the list, and they need immediate visual feedback when time-sensitive tasks are overdue. The current Listbox-based interface limits interaction and visual formatting.

## What Changes
- **UI Architecture Change**: Replace the standard `tk.Listbox` with a custom scrollable frame implementation to support rich row widgets.
- **Task Completion**: Add a checkbox/button to the right of each task item.
- **Completion Behavior**: Clicking the completion control immediately marks the task as complete and removes it from the list (and cancels any pending notifications).
- **Overdue Warning**: Tasks with a set deadline that has passed will be displayed with a distinct red warning style.

## Impact
- Affected specs: `ui-layout`, `scheduled-notifications`
- Affected code: `main.py` (significant refactor of `TodoListGUI` list rendering logic)
