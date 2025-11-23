## MODIFIED Requirements
### Requirement: Task List Presentation
The task list SHALL be presented as a scrollable list of interactive rows, allowing users to view and manage tasks directly.

#### Scenario: Viewing tasks
- **WHEN** tasks are added to the list
- **THEN** each task should be displayed in its own row container
- **AND** the list background should contrast slightly with the main window background

#### Scenario: Task completion interaction
- **WHEN** a user views a task row
- **THEN** a completion control (checkbox or button) should be visible on the right side
- **AND** clicking the control should mark the task as complete and remove it
