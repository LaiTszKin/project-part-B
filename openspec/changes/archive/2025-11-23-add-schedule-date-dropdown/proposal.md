# Change: Add Schedule Date Dropdown

## Why
Current text-based date input requires users to manually type dates in specific formats, which is error-prone and inconvenient. A dropdown menu with common date options will improve usability.

## What Changes
- Replace/Enhance the date input field with a `ttk.Combobox`.
- Provide preset options like "Today", "Tomorrow", "Next Week".
- Support custom date entry via the same combobox (allowing manual typing).
- Auto-populate the date portion based on selection.

## Impact
- Affected specs: `scheduled-notifications`
- Affected code: `TodoListGUI` class in `main.py` (specifically `create_widgets` and event handlers for date input).
