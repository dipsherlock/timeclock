# Changelog
<!-- Test commit after switching to Community Edition -->

<!-- Sync commit for GitHub display: v1.1.5 -->
All notable changes to this project will be documented in this file.

---

## [v1.2.2] – 2026-05-19
### Added
- **Dark and Light mode support:** Created a **Style** menu with sub-menu options **Dark Mode** and **Light Mode**
- **Alternate clock formats:** Added a **Clock Format** sub-menu to the Style menu, with options **12 Hour** and **24 Hour**.

### Changed
- Switched date format from "Year/Month/Day" to "Month/Day/Year" app-wide.

### Author
dipsherlock (<skylertclark@gmail.com>)

---

## [v1.2.1] – 2026-05-17
### Added
- **'Export Log' implementation:**
  - Finished implementing **Export Log** in the File menu, including sub-menu options **This Week, This Month, This Year,** and **All Time**.
  - User selects an option to save a time-filtered copy of the CSV file, with the default name "time_report_week/month/year/all_MMDDYYYY.csv".
  
  > **Example:** time_report_week_05172026.csv

- **Debugging tool:** Added Developer menu, including option **Clear Log** for debugging purposes.

### Changed
- Simplified main page by migrating buttons **View Hours** and **View Log** to the File menu.
- Updated About page to include myself as a derivative author.
- Switched wording from "**punch** in/out" to "**clock** in/out".

### Author
dipsherlock (<skylertclark@gmail.com>)

---

## [v1.1.5] – 2025-10-06
### Added
- **Unified version control system:**
  - Introduced a single `APP_VERSION` variable that automatically updates the version everywhere in the app.
  - Window title, About dialog, and footer version label now all sync automatically.

### Changed
- Simplified app metadata section for easier future updates.
- Minor layout adjustments for footer alignment and visual balance.

### Author
zegron (<matt@onetakemedia.net>)

---

## [v1.1.4] – 2025-10-06
### Added
- **Exit Warning System:**  
  - The app now checks if the user is still punched in when attempting to exit.  
  - Displays a confirmation dialog: “You are still punched in. Are you sure you want to exit?”  
  - User may choose to stay or exit — no forced actions.

### Changed
- Integrated window close (❌) and Exit button under unified `on_exit()` logic.
- Minor cleanup and improved code readability in main structure.

### Author
zegron (<matt@onetakemedia.net>)

---

## [v1.1.3] – 2025-10-06
### Added
- **Incomplete Session Detection:**  
  - App now checks the last logged action before accepting a new punch.  
  - Prevents users from punching in twice in a row or punching out without a prior punch in.  
  - Displays friendly warning popups to maintain consistent log data.

### Changed
- Improved internal logic for log handling and validation.
- Minor structural cleanup in `log_action()` and `get_last_action()` functions.

### Author
zegron (<matt@onetakemedia.net>)

---

## [v1.1.2] – 2025-10-06
### Added
- **Digital Clock:** Live clock field updates every second, showing the actual system time when punching in/out.  
- **Menu Bar:** Added File → Export (placeholder) and About menus.  
- **About Dialog:** Displays author, contact email, current version, and MIT license snippet.

### Changed
- Simplified menu layout — removed extra Help menu, replaced with About for clarity.

### Author
zegron (<matt@onetakemedia.net>)

---

## [v1.1.1] – 2025-10-01
### Added
- Introduced **View Hours** window with daily, weekly (Sunday–Saturday), and all-time totals.

### Removed
- Removed Undo Last / Undo Two buttons and logic.

---

## [v1.0.0] – 2025-09-24
### Initial Release
- Basic Punch In / Punch Out functionality.  
- CSV-based time logging.  
- Simple Tkinter GUI.
