import os
import sys
import tkinter as tk
import threading
import time
from plyer import notification

sit_mode = "sit down"
stand_mode = "stand up"


if hasattr(sys, '_MEIPASS'):
    # _MEIPASS is the temporary folder where PyInstaller extracts the bundle
    icon_path = os.path.join(sys._MEIPASS, 'stand_up_lazy.icns')
else:
    icon_path = './icons/stand_up_lazy.icns'  # Use this during development
    print(os.getcwd())

class StandUpApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stand Up, Lazy!")

        self.standing_time = tk.IntVar(value=10)  # Default standing time in minutes
        self.sitting_time = tk.IntVar(value=50)  # Default sitting time in minutes

        self.timer_running = False
        self.current_mode = sit_mode

        self.create_widgets()

        # Bind the close event to a custom handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # Frame to hold labels
        time_input_frame = tk.Frame(self.root)
        time_input_frame.pack(pady=(1,0))

        # Labels and Entries for standing and sitting
        tk.Label(time_input_frame, text="Sitting:", width=7, font=("Helvetica", 10), anchor="e").pack(side=tk.LEFT, padx=(1,0), pady=(5, 0))
        tk.Entry(time_input_frame, textvariable=self.standing_time, width=4, font=("Helvetica", 10)).pack(side=tk.LEFT, padx=(0,1), pady=(5, 0))
        tk.Label(time_input_frame, text="Standing:", width=7, font=("Helvetica", 10), anchor="e").pack(side=tk.LEFT, padx=(1,0), pady=(5, 0))
        tk.Entry(time_input_frame, textvariable=self.sitting_time, width=4, font=("Helvetica", 10)).pack(side=tk.LEFT, padx=(0,1), pady=(5, 0))


        # Timer label with larger font size
        self.time_left_label = tk.Label(self.root, text="00:00", font=("Helvetica", 36))
        self.time_left_label.pack(pady=0)

        # Frame to hold the buttons side by side
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=0)

        # Button to toggle timer
        self.toggle_button = tk.Button(button_frame, text="I sat down", command=self.toggle_timer, width=5)
        self.toggle_button.pack(side=tk.LEFT, padx=0, pady=(0, 5))

        # Reset button
        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset, width=5)
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
                app_icon=icon_path,
                timeout=10
            )
        except:

            pass

    def reset(self):
        # Reset the application state
        self.timer_running = False
        self.current_mode = sit_mode
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