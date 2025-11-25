# Change: Update Button Styling for Softer Interface

## Why
Current button styles have sharp edges that feel rigid. Rounded buttons create a softer, more inviting UI that aligns better with modern Apple design principles and improves the overall aesthetic cohesion of the application.

## What Changes
- Increase border radius on all button styles (Primary, Secondary, Success) for more rounded corners
- Apply consistent roundness across all interactive button elements
- Maintain color scheme and padding while softening visual appearance

## Impact
- Affected specs: `ui-layout`
- Affected code: `main.py` (ttk.Style button configurations)
