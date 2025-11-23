# ui-layout Specification

## Purpose
TBD - created by archiving change optimize-frontend-layout. Update Purpose after archive.
## Requirements
### Requirement: Minimalist Window Layout
The application window SHALL present a clean, minimalist interface with generous whitespace and balanced padding, following Apple design principles.

#### Scenario: Application startup
- **WHEN** the application is launched
- **THEN** the window should have a minimum size of 320x480
- **AND** the main content area should have consistent padding (e.g., 24px) from the window edges
- **AND** the background color should match the system background color (e.g., #F2F2F7)

### Requirement: Typography Hierarchy
The application SHALL use a clear typography hierarchy to distinguish between headings, body text, and secondary information.

#### Scenario: Viewing the main interface
- **WHEN** the user views the application
- **THEN** the title "我的備忘錄" should be prominent (Large Title style)
- **AND** the input fields and list items should use a readable body font size (e.g., 15pt)
- **AND** secondary text (like dates or status counts) should be smaller and lighter in color

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

### Requirement: Interactive Elements Styling
Buttons and inputs SHALL have consistent styling that indicates their state and function.

#### Scenario: Interacting with inputs
- **WHEN** the user focuses on an input field
- **THEN** it should have a subtle indication of focus
- **AND** buttons should have clear primary (colored) and secondary (outline/text) styles

