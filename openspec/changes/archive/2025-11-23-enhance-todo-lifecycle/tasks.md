## 1. Implementation
- [x] 1.1 Create `ScrollableFrame` utility class in `main.py` to replace `Listbox`.
- [x] 1.2 Refactor `TodoListGUI` to use `ScrollableFrame` for the task list container.
- [x] 1.3 Implement `create_task_row` method to generate a Frame with Label (task text) and Button (complete).
- [x] 1.4 Implement `complete_task` logic: remove task from model, cancel notification, refresh view.
- [x] 1.5 Add overdue logic: check `datetime.now() > task.notification_time` and apply red color style to the task label.
- [x] 1.6 Remove legacy `Listbox` specific code (selection handling, `delete_selected_task` adaptation if needed).
- [x] 1.7 Verify layout matches Apple-style design (padding, alignment).
- [x] 1.8 Test adding, completing (removing), and overdue display scenarios.
