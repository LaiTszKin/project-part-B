# Change: Expand Datetime Selector

## Why
The current date selection interface relies on a single dropdown with limited presets and manual text entry, which can be error-prone and less intuitive for users who want to set precise custom times. Users need a more flexible way to combine year, month, day, hour, and minute freely.

## What Changes
- Replace the single `Combobox` for date entry with a set of 5 linked `Combobox` widgets (Year, Month, Day, Hour, Minute).
- Implement logic to dynamically update "Day" options based on the selected Year and Month (handling leap years and month lengths).
- Set default values to the current time or the next logical time slot.
- Update the UI layout to accommodate the new selector row.

## Impact
- **Affected specs**: `scheduled-notifications`
- **Affected code**: `main.py` (specifically `TodoListGUI` class widgets and validation logic)
