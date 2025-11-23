## Context
The current application uses `tk.Listbox` to display tasks. `tk.Listbox` is a simple widget that only supports text items and has limited styling capabilities (e.g., cannot place interactive widgets like checkboxes inside rows). The requirement to add a "completion button on the right" and "red warning text for overdue items" necessitates a more flexible UI component.

## Goals / Non-Goals
- **Goals**:
  - Implement a scrollable list where each item is a custom container (Frame).
  - Each row contains the task text (Label) and a completion control (Button/Checkbutton).
  - Support dynamic styling (red text) for overdue items.
  - Maintain the existing Apple-style aesthetic.
- **Non-Goals**:
  - implementing a full complex task management system (subtasks, tags, etc.).
  - Persistent storage (out of scope for this change, though desirable later).

## Decisions
- **Decision**: Replace `tk.Listbox` with a `Canvas` + `Frame` (Scrollable Frame) pattern.
  - **Rationale**: This is the standard Tkinter pattern for creating scrollable lists of complex widgets. It allows full control over the layout of each "row".
- **Decision**: Use a "Checkmark" button on the right side.
  - **Rationale**: The requirements specify "right side". A button with a checkmark icon or text "✓" is clear and touch-friendly.
- **Decision**: Overdue check happens at render time.
  - **Rationale**: Since there is no background refresh loop for the UI (only for notifications), checking overdue status when the list is refreshed/rendered is sufficient for the MVP.

## Risks / Trade-offs
- **Risk**: Performance with many tasks.
  - **Mitigation**: Tkinter Frames are heavier than Listbox items. For a simple todo list (usually <100 items), this is negligible. If it grows, we might need virtual scrolling, but that's premature optimization.
- **Risk**: Scrollbar behavior.
  - **Mitigation**: Implementing a robust ScrollableFrame class that handles binding mousewheel and scrollbar events correctly is required.

## Migration Plan
1.  Create a `ScrollableFrame` helper class.
2.  Replace `self.task_listbox` initialization with `ScrollableFrame`.
3.  Update `display_task_in_list` (or equivalent) to create `TaskRow` widgets instead of inserting text.
4.  Update `delete_selected_task` logic (might be removed or adapted since we now have per-item delete). *Note: The "Delete Selected" button might become redundant or change to "Delete All Completed" if we kept them, but the req says "remove from todo list", so per-item delete is the primary interaction.*
