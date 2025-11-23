## 1. Implementation
- [x] 1.1 Update `TodoListGUI.create_widgets` to replace `ttk.Entry` with `ttk.Combobox` for date input.
- [x] 1.2 Configure `Combobox` values with dynamic options: "Today", "Tomorrow", "Next Week" (calculated based on current date).
- [x] 1.3 Implement event handler for Combobox selection to automatically fill/format the date string (keeping time as default or prompting).
- [x] 1.4 Ensure manual typing still works and validates correctly (existing validation logic might need adaptation to Combobox events).
- [x] 1.5 Verify styling matches Apple design system (consistent with other inputs).
