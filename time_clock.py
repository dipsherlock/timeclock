import tkinter as tk
from tkinter import messagebox, Menu, filedialog
import csv
import os
from datetime import datetime, timedelta

# --- App Metadata ---
APP_VERSION = "1.2.2"  # Change this line only to update version everywhere
APP_NAME = f"Time Clock v{APP_VERSION}"
AUTHOR = "zegron"
EMAIL = "matt@onetakemedia.net"
AUTHOR_DER = "dipsherlock"
EMAIL_DER = "skylertclark@gmail.com"
LICENSE_SNIPPET = "MIT License © 2025 zegron"

FILENAME = "time_log.csv"
CLOCK_FORMAT = "12h"


# --- Core Functions ---

def get_last_action():
    """Read the last logged action from the CSV file, if any."""
    if not os.path.exists(FILENAME):
        return None
    try:
        with open(FILENAME, "r") as f:
            lines = f.readlines()
            if not lines:
                return None
            last_line = lines[-1].strip().split(",")
            if len(last_line) >= 2:
                return last_line[1].strip()
    except Exception:
        return None
    return None


def log_action(action):
    """Log Punch In/Out actions to the CSV file, preventing invalid sequences."""
    last_action = get_last_action()

    # Detect invalid sequence
    if action == "Punch In" and last_action == "Punch In":
        messagebox.showwarning("Warning", "You must Clock Out before clocking in again.")
        return
    if action == "Punch Out" and last_action != "Punch In":
        messagebox.showwarning("Warning", "You must Clock In before clocking out.")
        return

    now = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    file_exists = os.path.exists(FILENAME)
    with open(FILENAME, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Action"])
        writer.writerow([now, action])
    messagebox.showinfo("Logged", f"{action} at {now}")


def view_log():
    """Display the entire log file contents."""
    if not os.path.exists(FILENAME):
        messagebox.showwarning("Error", "No log file found.")
        return
    with open(FILENAME, "r") as f:
        log = f.read()
    messagebox.showinfo("Time Log", log if log else "Log is empty.")


def export_report(period="all"):
    """Export the log file to a user-selected CSV location."""
    if not os.path.exists(FILENAME):
        messagebox.showwarning("Error", "No log file found.")
        return

    try:
        export_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            initialfile=f"time_report_{period}_{datetime.now().strftime('%m%d%Y')}.csv",
            title="Export Time Log"
        )

        if not export_path:
            return  # User cancelled

        entries = []

        with open(FILENAME, "r", newline="") as f:
            reader = csv.reader(f)

            next(reader, None)

            for row in reader:
                if len(row) < 2:
                    continue

                timestamp, action = row
                dt = datetime.strptime(timestamp, "%m-%d-%Y %H:%M:%S")

                entries.append((dt, action))

        # Export Filter
        today = datetime.now()
        if period == "week":
            # Sunday-start week
            days_since_sunday = (today.weekday() + 1) % 7
            start_date = (today - timedelta(days=days_since_sunday)).replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "month":
            start_date = today.replace(day=1)
        elif period == "year":
            start_date = today.replace(month=1, day=1)
        else:
            start_date = None

        # Build sessions
        sessions = []
        punch_in_time = None

        for dt, action in entries:
            if action == "Punch In":
                punch_in_time = dt

            elif action == "Punch Out" and punch_in_time:
                sessions.append((punch_in_time, dt))
                punch_in_time = None

        if not sessions:
            messagebox.showinfo("Export", "No completed sessions found.")
            return

        total_hours = 0

        # Filter sessions
        filtered_sessions = []
        for start, end in sessions:
            if start_date:
                if start < start_date:
                    continue
            filtered_sessions.append((start, end))
            

        # Write export
        with open(export_path, "w", newline="") as f:
            writer = csv.writer(f)

            # Header row
            writer.writerow(["Date", "Clock In", "Clock Out", "Hours"])

            for start, end in filtered_sessions:
                hours = round((end - start).total_seconds() / 3600, 2)
                total_hours += hours

                writer.writerow([
                    start.strftime("%m-%d-%Y"),
                    start.strftime("%H:%M:%S"),
                    end.strftime("%H:%M:%S"),
                    f"{hours:.2f}"
                ])

            # Blank line
            writer.writerow([])

            # Footer / summary row
            writer.writerow([
                "TOTAL",
                "",
                "",
                f"{total_hours:.2f}"
            ])

        messagebox.showinfo(
            "Export Successful",
            f"Report exported successfully:\n{export_path}"
        )

    except Exception as e:
        messagebox.showerror(
            "Export Failed",
            f"An error occurred:\n{e}"
        )

def clear_log():
    """Delete the current log file after confirmation."""

    if not os.path.exists(FILENAME):
        messagebox.showinfo("Clear Log", "No log file exists.")
        return

    confirm = messagebox.askyesno(
        "Clear Log",
        "This will permanently delete all logged time entries.\n\nContinue?"
    )

    if not confirm:
        return

    try:
        os.remove(FILENAME)
        with open(FILENAME, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Action"])

        messagebox.showinfo(
            "Clear Log",
            "Log file deleted successfully."
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Could not delete log file:\n{e}"
        )

def calculate_hours():
    """Read the CSV file and calculate total hours."""
    if not os.path.exists(FILENAME):
        messagebox.showwarning("Error", "No log file found.")
        return

    entries = []
    with open(FILENAME, "r") as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip header
        for row in reader:
            timestamp, action = row
            dt = datetime.strptime(timestamp, "%m-%d-%Y %H:%M:%S")
            entries.append((dt, action))

    sessions = []
    punch_in_time = None
    for dt, action in entries:
        if action == "Punch In":
            punch_in_time = dt
        elif action == "Punch Out" and punch_in_time:
            sessions.append((punch_in_time, dt))
            punch_in_time = None

    if not sessions:
        messagebox.showinfo("Hours Summary", "No completed sessions found.")
        return

    daily_totals = {}
    weekly_totals = {}
    all_time_total = 0.0

    for start, end in sessions:
        hours = (end - start).total_seconds() / 3600
        day = start.date()
        daily_totals[day] = daily_totals.get(day, 0) + hours
        # Week starts Sunday
        week_start = day - timedelta(days=day.weekday() + 1 if day.weekday() != 6 else 0)
        weekly_totals[week_start] = weekly_totals.get(week_start, 0) + hours
        all_time_total += hours

    summary = "Hours Summary\n" + "-" * 30 + "\n\n"
    summary += "Daily Totals:\n"
    for day in sorted(daily_totals):
        summary += f"{day}: {daily_totals[day]:.2f} hours\n"

    summary += "\nWeekly Totals:\n"
    for week in sorted(weekly_totals):
        summary += f"Week of {week}: {weekly_totals[week]:.2f} hours\n"

    summary += f"\nAll-Time Total: {all_time_total:.2f} hours"
    messagebox.showinfo("Hours Summary", summary)


def show_about():
    """Display app info in a popup window."""
    about_text = (
        f"{APP_NAME}\n"
        f"Author: {AUTHOR}\n"
        f"Contact: {EMAIL}\n\n"
        f"Derivative Author: {AUTHOR_DER}\n"
        f"Contact: {EMAIL_DER}\n\n"
        f"{LICENSE_SNIPPET}\n\n"
        "A simple Windows desktop time tracker built with Python and Tkinter."
    )
    messagebox.showinfo("About", about_text)


def apply_theme(bg_color, fg_color, button_bg, button_fg):
    """Apply colors to the whole app."""

    # Main window
    root.config(bg=bg_color)

    # Labels
    clock_label.config(bg=bg_color, fg=fg_color)
    version_label.config(bg=bg_color, fg=fg_color)

    # Buttons
    clock_in_button.config(
        bg=button_bg,
        fg=button_fg,
        activebackground=bg_color,
        activeforeground=fg_color
    )

    clock_out_button.config(
        bg=button_bg,
        fg=button_fg,
        activebackground=bg_color,
        activeforeground=fg_color
    )

    exit_button.config(
        bg=button_bg,
        fg=button_fg,
        activebackground=bg_color,
        activeforeground=fg_color
    )

    # Menu bar
    menu_bar.config(
        bg=button_bg,
        fg=button_fg,
        activebackground=bg_color,
        activeforeground=fg_color
    )

    # Dropdown menus
    for menu in [file_menu, export_menu, style_menu, about_menu, dev_menu]:
        menu.config(
            bg=button_bg,
            fg=button_fg,
            activebackground=bg_color,
            activeforeground=fg_color
        )

def dark_mode():
    """Change app style to dark colors"""
    apply_theme(
        bg_color="#1e1e1e",
        fg_color="#ffffff",
        button_bg="#333333",
        button_fg="white"
    )

def light_mode():
    """Change app style to light colors"""
    apply_theme(
        bg_color="white",
        fg_color="black",
        button_bg="#f0f0f0",
        button_fg="black"
    )


def on_exit():
    """Warn user if they are still punched in before exiting."""
    last_action = get_last_action()
    if last_action == "Punch In":
        confirm = messagebox.askyesno(
            "Still Clocked In",
            "You are still clocked in.\nAre you sure you want to exit?"
        )
        if not confirm:
            return  # Cancel exit
    root.destroy()  # Proceed with exit


# --- GUI Setup ---

root = tk.Tk()
root.title(APP_NAME)
root.geometry("340x200")  # slightly taller for footer label


# --- Digital Clock Display ---
clock_label = tk.Label(root, text="", font=("Helvetica", 16, "bold"))
clock_label.pack(pady=5)


def set_12_hour():
    """Switch clock to 12-hour format."""
    global CLOCK_FORMAT
    CLOCK_FORMAT = "12h"


def set_24_hour():
    """Switch clock to 24-hour format."""
    global CLOCK_FORMAT
    CLOCK_FORMAT = "24h"


def update_clock():
    """Update the on-screen digital clock every second."""
    if CLOCK_FORMAT == "12h":
        current_time = datetime.now().strftime("%I:%M:%S %p")
    else:
        current_time = datetime.now().strftime("%H:%M:%S")

    clock_label.config(text=current_time)

    root.after(1000, update_clock)


update_clock()


# --- Menu Bar ---
menu_bar = Menu(root)
root.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="View Hours", command=calculate_hours)
file_menu.add_command(label="View Log", command=view_log)
export_menu = Menu(file_menu, tearoff=0)
export_menu.add_command(label="This Week", command=lambda: export_report("week"))
export_menu.add_command(label="This Month", command=lambda: export_report("month"))
export_menu.add_command(label="This Year", command=lambda: export_report("year"))
export_menu.add_command(label="All Time", command=lambda: export_report("all"))
file_menu.add_separator()
file_menu.add_cascade(label="Export Report", menu=export_menu)
menu_bar.add_cascade(label="File", menu=file_menu)

style_menu = Menu(menu_bar, tearoff=0)
style_menu.add_command(label="Dark Mode", command=dark_mode)
style_menu.add_command(label="Light Mode", command=light_mode)
style_menu.add_separator()
clock_menu = Menu(style_menu, tearoff=0)
clock_menu.add_command(label="12 Hour", command=set_12_hour)
clock_menu.add_command(label="24 Hour", command=set_24_hour)
style_menu.add_cascade(label="Clock Format", menu=clock_menu)
menu_bar.add_cascade(label="Style", menu=style_menu)

about_menu = Menu(menu_bar, tearoff=0)
about_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="About", menu=about_menu)

dev_menu = Menu(menu_bar, tearoff=0)
dev_menu.add_command(label="Clear Log", command=clear_log)
menu_bar.add_cascade(label="Developer", menu=dev_menu)


# --- Buttons ---
clock_in_button = tk.Button(
    root,
    text="Clock In",
    width=15,
    command=lambda: log_action("Punch In")
)
clock_in_button.pack(pady=5)

clock_out_button = tk.Button(
    root,
    text="Clock Out",
    width=15,
    command=lambda: log_action("Punch Out")
)
clock_out_button.pack(pady=5)

exit_button = tk.Button(
    root,
    text="Exit",
    width=15,
    command=on_exit
)
exit_button.pack(pady=5)


# --- Version Label (footer) ---
version_label = tk.Label(root, text=f"Version {APP_VERSION}", font=("Arial", 9), fg="gray")
version_label.pack(side="bottom", pady=3)


# --- Default Style ---
dark_mode()


# --- Handle window close (X button) ---
root.protocol("WM_DELETE_WINDOW", on_exit)


# --- Run App ---
root.mainloop()
