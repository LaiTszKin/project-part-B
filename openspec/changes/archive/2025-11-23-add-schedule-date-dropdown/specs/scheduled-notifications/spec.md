## ADDED Requirements
### Requirement: Date Selection Interface
The system SHALL provide a dropdown interface for selecting notification dates to simplify user input.

#### Scenario: Select preset date
- **WHEN** user opens the schedule notification interface
- **THEN** a dropdown menu should be available
- **AND** it should include options for "Today", "Tomorrow", and "Next Week" (or specific dates)
- **AND** selecting an option should populate the date field with the correct formatted date

#### Scenario: Manual date entry
- **WHEN** user wants to set a specific date not in presets
- **THEN** the dropdown should allow manual text entry
- **AND** standard date format validation should apply
