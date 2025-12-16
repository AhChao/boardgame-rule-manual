# Two Rooms and a Boom Rulebook - Chinese Translation & Mobile Site

## Goal Description
Create a mobile-friendly, Traditional Chinese version of the "Two Rooms and a Boom" rulebook based on the extracted PDF content. The output will be a single HTML file with embedded CSS for easy sharing and viewing on mobile devices.

## User Review Required
- **Translation Quality**: The translation will be done by the AI. Review for specific gaming terminology preference may be needed (e.g., "Bomber" -> "炸彈客", "President" -> "總統").
- **Layout**: The design will focus on readability on small screens (mobile-first).

## Proposed Changes
### Project Structure
- `artifacts/two-rooms-rules/index.html`: The main HTML file containing the translated rules and styles.

### Content Mapping
The HTML will be structured into sections corresponding to the rulebook pages:
1.  **Title & Intro** (Page 1-3)
2.  **Components** (Page 2)
3.  **Setup** (Page 4)
4.  **The 4 Basic Rules** (Page 5)
5.  **Leaders & Hostages** (Page 6-7) - *Will likely use a responsive table or list for the hostage chart.*
6.  **Changing Leaders** (Page 8)
7.  **End of a Round** (Page 9)
8.  **Game Over** (Page 10)
9.  **Advanced & Additional Rules** (Page 11-13)
10. **Glossary** (Page 14-15)

### Design & Tech Stack
-   **HTML5** for semantic structure.
-   **CSS3** for styling.
    -   Mobile-first approach.
    -   Clear typography (larger fonts for mobile).
    -   Distinct sections/cards for each rule category.
    -   Navigation menu (sticky or hamburger) to jump between sections.
    -   Color scheme: Red vs Blue theme (fitting the game).

## Verification Plan
### Automated Tests
-   None (Visual project).

### Manual Verification
-   **Browser Preview**: Use the browser tool to open the generated `index.html` and verify:
    -   Text readability on "mobile" viewport size.
    -   Navigation links work.
    -   Translation makes sense (self-check).
    -   Layout responsiveness (resize window).
