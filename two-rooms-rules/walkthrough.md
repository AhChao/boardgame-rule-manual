# Two Rooms and a Boom - Chinese Mobile Rulebook Walkthrough

## Summary
Successfully extracted the text from the original English PDF, translated it into Traditional Chinese (繁體中文), and created a responsive, mobile-friendly HTML rulebook.

## Changes
-   **Parsed PDF**: Used `pypdf` to extract text from `files/TwoRooms_Rulebook_v3.pdf`.
-   **Translation**: Manually translated the content to Traditional Chinese, focusing on clarity and game terminology associated with "Two Rooms and a Boom".
-   **Web Rules**: Created `artifacts/two-rooms-rules/index.html`.
    -   **Mobile-First Design**: Larger text, clear headers, card-based layout.
    -   **Navigation**: Quick jump buttons for sections like "Startup", "Leaders", "Winning".
    -   **Floating Sidebar**: Added a collapsible floating navigation bar on the right side for easier access while scrolling.
    -   **Active Highlight**: The current section in the navigation bar highlights automatically as you scroll.
    -   **Character Search**: Added a dedicated sub-page (`characters.html`) to search for character abilities by English or Chinese name.
    -   **Setup Guide**: Added a sub-page (`setup.html`) with recommended teaching setups, filterable by player count. Descriptions are neatly formatted as bullet points.
    -   **Cheat Sheet**: Added a quick reference table at the bottom of the main page showing the number of hostages exchanged per round based on player count.
    -   **Visuals**: Used Red/Blue color coding to match the game's theme.

## Verification Actions
-   **Content Check**: Verified that all key rules (Setup, 4 Basic Rules, Hostage Exchange Chart, Win Conditions) are present.
-   **Layout Check**: Validated the responsive design for mobile viewing.

## File Location
You can open the rulebook directly in your browser:
[Two Rooms Rules (Traditional Chinese)](index.html)
