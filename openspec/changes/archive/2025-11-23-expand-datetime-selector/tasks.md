## 1. Implementation
- [x] 1.1 Remove the existing single `datetime_entry` Combobox and its associated frame content.
- [x] 1.2 Create a new frame structure to hold 5 Comboboxes (Year, Month, Day, Hour, Minute).
- [x] 1.3 Implement helper methods to populate Years (current+10), Months (1-12), Hours (0-23), Minutes (0-59).
- [x] 1.4 Implement `update_days` method to dynamically update the Day Combobox based on Year/Month selection.
- [x] 1.5 Implement `get_selected_datetime` method to construct a `datetime` object from the 5 Combobox values.
- [x] 1.6 Update `add_task_input` to use the new `get_selected_datetime` method.
- [x] 1.7 Update validation logic to give visual feedback (e.g., highlight invalid dates if manual entry is allowed, though selection prevents most errors).
- [x] 1.8 Verify the layout looks correct and aligned with Apple design principles (spacing, fonts).

## 2. Verification
- [x] 2.1 Verify that selecting a date (e.g., Feb 29 in a leap year) works correctly.
- [x] 2.2 Verify that changing the month updates the available days (e.g., switching from Jan to Feb reduces days).
- [x] 2.3 Verify that adding a task with the new selector correctly schedules a notification.
