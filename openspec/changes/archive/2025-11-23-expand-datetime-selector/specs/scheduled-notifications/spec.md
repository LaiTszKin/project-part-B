## MODIFIED Requirements
### Requirement: Date Selection Interface
The system SHALL provide a multi-selector interface for selecting notification dates, allowing users to independently choose year, month, day, hour, and minute.

#### Scenario: Select custom date and time
- **WHEN** user opens the schedule notification interface
- **THEN** five separate dropdowns should be available (Year, Month, Day, Hour, Minute)
- **AND** default values should be set to current or logical next time
- **AND** changing the month or year should automatically update the available days (e.g., leap years)

#### Scenario: Validate selection
- **WHEN** user selects a date components
- **THEN** the system should construct a valid datetime object
- **AND** invalid combinations (like Feb 30) should be prevented by the UI logic
