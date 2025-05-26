import os
import platform
import sys
import threading
import time
import tkinter as tk
from tkinter import ttk

import sv_ttk
from plyer import notification

sit_mode = "sit down"
stand_mode = "stand up"

system_name = platform.system()
icon = None
icon_path = None
if system_name == "Windows":
    icon = "stand_up_lazy.ico"
if system_name == "Linux":
    icon = "stand_up_lazy.png"
if system_name == "Darwin":
    icon = "stand_up_lazy.icns"
if icon:
    if hasattr(sys, "_MEIPASS"):
        # _MEIPASS is the temporary folder where PyInstaller extracts the bundle
        icon_path = os.path.join(sys._MEIPASS, icon)
    else:
        icon_path = os.path.join("./icons", icon)  # Use this during development

class StandUpApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Stand Up, Lazy!")
        if icon_path:  # set icon
            self.root.iconbitmap(icon_path)

        sv_ttk.set_theme("dark")  # set theme

        self.sitting_time_default = 45  # Default sitting time in minutes
        self.standing_time_default = 15  # Default standing time in minutes
        self.sitting_time = tk.IntVar(value=self.sitting_time_default)
        self.standing_time = tk.IntVar(value=self.standing_time_default)  #
        self.timer_running = False
        self.current_mode = sit_mode

        self.create_widgets()

        # Bind the close event to a custom handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # Frame to hold labels
        time_input_frame = ttk.Frame(self.root)
        time_input_frame.pack(pady=(1, 0))

        # Labels and Entries for standing and sitting
        ttk.Label(time_input_frame, text="Sitting:", font=("Helvetica", 10), anchor="e").pack(side=tk.LEFT, padx=(1, 0), pady=(5, 0))
        self.sitting_time_entry = ttk.Entry(time_input_frame, textvariable=self.sitting_time, width=4, font=("Helvetica", 10))
        self.sitting_time_entry.pack(side=tk.LEFT, padx=(0, 1), pady=(5, 0))
        ttk.Label(time_input_frame, text="Standing:", font=("Helvetica", 10), anchor="e").pack(side=tk.LEFT, padx=(1, 0), pady=(5, 0))
        self.standing_time_entry = ttk.Entry(time_input_frame, textvariable=self.standing_time, width=4, font=("Helvetica", 10))
        self.standing_time_entry.pack(side=tk.LEFT, padx=(0, 1), pady=(5, 0))

        # Timer label with larger font size
        self.time_left_label = ttk.Label(self.root, text="00:00", font=("Helvetica", 36))
        self.time_left_label.pack(pady=0)

        # Frame to hold the buttons side by side
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=0)

        # Button to toggle timer
        self.toggle_button = ttk.Button(button_frame, text="I sat down", command=self.toggle_timer)
        self.toggle_button.pack(side=tk.LEFT, padx=0, pady=(0, 5))

        # Reset button
        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=0, pady=(0, 5))

    def toggle_timer(self):
        if not self.timer_running:
            self.toggle_button.config(state=tk.DISABLED)
            self.start_timer()

    def start_timer(self):
        self.timer_running = True

        def timer_thread():
            time_to_wait = self.sitting_time.get() * 60 if self.current_mode == sit_mode else self.standing_time.get() * 60
            while self.timer_running and time_to_wait >= 0:
                mins, secs = divmod(time_to_wait, 60)
                self.time_left_label.config(text=f"{mins:02}:{secs:02}")
                time.sleep(1)
                time_to_wait -= 1

            if self.timer_running and time_to_wait <= 0:
                self.timer_running = False
                self.switch_mode()
                self.send_notification()
                self.toggle_button.config(state=tk.NORMAL)

        threading.Thread(target=timer_thread).start()

    def switch_mode(self):
        self.current_mode = stand_mode if self.current_mode == sit_mode else sit_mode
        self.toggle_button.config(text="I sat down" if self.current_mode == sit_mode else "I stood up")

    def send_notification(self):
        try:
            notification.notify(
                title=f"Time to {self.current_mode.capitalize()}!",
                message=f"Please {self.current_mode} now.",
                app_name="Stand Up, Lazy!",
                app_icon=icon_path if icon_path else "",
                timeout=30
            )
        except:
            pass

    def reset(self):
        # Reset the application state
        self.timer_running = False
        self.current_mode = sit_mode
        self.sitting_time_entry.delete(0, tk.END)
        self.sitting_time_entry.insert(0, str(self.sitting_time_default))
        self.standing_time_entry.delete(0, tk.END)
        self.standing_time_entry.insert(0, str(self.standing_time_default))
        self.toggle_button.config(text="I sat down", state=tk.NORMAL)
        self.time_left_label.config(text="00:00")

    def on_close(self):
        # Stop the timer and close the application
        self.timer_running = False
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = StandUpApp(root)
    root.mainloop()


def main():
    root = tk.Tk()
    app = StandUpApp(root)
    root.mainloop()
