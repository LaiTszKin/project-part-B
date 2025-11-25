## MODIFIED Requirements
### Requirement: Minimalist Window Layout
The application window SHALL present a clean, minimalist interface with generous whitespace and balanced padding, following Apple design principles while maintaining native look and feel on other platforms.

#### Scenario: Application startup
- **WHEN** the application is launched
- **THEN** the window should have a minimum size of 320x480
- **AND** the main content area should have consistent padding (e.g., 24px) from the window edges
- **AND** the background color should match the system background color (e.g., #F2F2F7 on Mac, SystemButtonFace/White on Windows)

### Requirement: Typography Hierarchy
The application SHALL use a clear typography hierarchy that respects the host platform's design language.

#### Scenario: Viewing the main interface
- **WHEN** the user views the application
- **THEN** the title "我的備忘錄" should be prominent (Large Title style)
- **AND** the font should be "SF Pro" on macOS and "Segoe UI" on Windows
- **AND** the input fields and list items should use a readable body font size (e.g., 15pt or 11pt depending on platform conventions)
- **AND** secondary text should be smaller and lighter in color
