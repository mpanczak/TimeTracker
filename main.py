import customtkinter as ctk
from monitor import Monitor
from storage import load_data, save_full_data
import tkinter.messagebox as messagebox

# Colors
COLOR_WORK_BG = "#FFFFFF"      # White
COLOR_WORK_TEXT = "#2D3436"    # Dark Gray
COLOR_PERSONAL_BG = "#6C5CE7"  # Vibrant Purple
COLOR_PERSONAL_TEXT = "#FFFFFF" # White
COLOR_BTN_HOVER = "#dfe6e9"

class HistoryWindow(ctk.CTkToplevel):
    def __init__(self, history_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.title("History (Last 5 Days)")
        
        self.label_title = ctk.CTkLabel(self, text="Productivity History", font=("Roboto", 18, "bold"))
        self.label_title.pack(pady=10)
        
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        if not history_data:
            ctk.CTkLabel(self.scrollable_frame, text="No history available.").pack(pady=20)
        else:
            for date, times in sorted(history_data.items(), reverse=True):
                work_str = self.format_time(times.get("work", 0))
                pers_str = self.format_time(times.get("personal", 0))
                
                row_frame = ctk.CTkFrame(self.scrollable_frame)
                row_frame.pack(fill="x", pady=5)
                
                ctk.CTkLabel(row_frame, text=date, font=("Roboto", 14, "bold")).pack(side="left", padx=10)
                ctk.CTkLabel(row_frame, text=f"Work: {work_str} | Personal: {pers_str}", font=("Roboto", 12)).pack(side="right", padx=10)

    def format_time(self, seconds):
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}"

class ProductivityApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Productivity Timer")
        self.geometry("500x450")
        
        # Load data
        self.data = load_data()
        self.monitor = Monitor(self.data)
        # self.monitor.set_initial_times(self.data["work"], self.data["personal"]) # Removed as we pass data dict
        self.monitor.start()

        # Configure Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Main button area
        self.grid_rowconfigure(1, weight=0) # Control bar

        # Main Container (The "Big Button")
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Bind click to toggle
        self.main_frame.bind("<Button-1>", self.toggle_mode)
        
        # Labels
        self.label_mode = ctk.CTkLabel(self.main_frame, text="WORK", font=("Roboto", 48, "bold"))
        self.label_mode.grid(row=0, column=0, pady=(40, 10))
        self.label_mode.bind("<Button-1>", self.toggle_mode)

        self.label_timer = ctk.CTkLabel(self.main_frame, text="00:00:00", font=("Roboto", 72, "bold"))
        self.label_timer.grid(row=1, column=0, pady=10)
        self.label_timer.bind("<Button-1>", self.toggle_mode)

        self.label_stats = ctk.CTkLabel(self.main_frame, text="Today's Total:\nWork: 00:00\nPersonal: 00:00", 
                                        font=("Roboto", 18))
        self.label_stats.grid(row=2, column=0, pady=20)
        self.label_stats.bind("<Button-1>", self.toggle_mode)

        self.label_status = ctk.CTkLabel(self.main_frame, text="Tracking...", font=("Roboto", 14))
        self.label_status.grid(row=3, column=0, pady=(0, 20))
        self.label_status.bind("<Button-1>", self.toggle_mode)

        # Control Bar
        self.control_frame = ctk.CTkFrame(self, height=50, corner_radius=0, fg_color="#dfe6e9")
        self.control_frame.grid(row=1, column=0, sticky="ew")
        self.control_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.btn_history = ctk.CTkButton(self.control_frame, text="History", command=self.show_history,
                                         fg_color="#b2bec3", hover_color="#636e72", text_color="black")
        self.btn_history.grid(row=0, column=0, padx=20, pady=10)

        self.btn_clear = ctk.CTkButton(self.control_frame, text="Clear Today", command=self.clear_data,
                                       fg_color="#fab1a0", hover_color="#e17055", text_color="black")
        self.btn_clear.grid(row=0, column=2, padx=20, pady=10)

        # Initial State
        self.update_ui_mode()
        
        # Start update loop
        self.update_gui()

        # Handle close
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def toggle_mode(self, event=None):
        new_mode = not self.monitor.is_work_mode
        self.monitor.set_mode(new_mode)
        self.update_ui_mode()

    def update_ui_mode(self):
        if self.monitor.is_work_mode:
            bg_color = COLOR_WORK_BG
            text_color = COLOR_WORK_TEXT
            mode_text = "WORK"
        else:
            bg_color = COLOR_PERSONAL_BG
            text_color = COLOR_PERSONAL_TEXT
            mode_text = "PERSONAL"

        self.main_frame.configure(fg_color=bg_color)
        self.label_mode.configure(text=mode_text, text_color=text_color)
        self.label_timer.configure(text_color=text_color)
        self.label_stats.configure(text_color=text_color)
        self.label_status.configure(text_color=text_color)

    def format_time(self, seconds):
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    def update_gui(self):
        work, personal = self.monitor.get_times()
        
        if self.monitor.is_work_mode:
            self.label_timer.configure(text=self.format_time(work))
        else:
            self.label_timer.configure(text=self.format_time(personal))
            
        self.label_stats.configure(text=f"Today's Total:\nWork: {self.format_time(work)}\nPersonal: {self.format_time(personal)}")

        if self.monitor.is_workstation_locked():
             self.label_status.configure(text="LOCKED (PAUSED)")
        else:
             self.label_status.configure(text="CLICK TO SWITCH")

        self.after(1000, self.update_gui)

    def show_history(self):
        history = self.data.get("history", {})
        HistoryWindow(history, self)

    def clear_data(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear today's data?"):
            self.monitor.reset_today()
            self.update_gui()

    def on_close(self):
        self.monitor.stop()
        save_full_data(self.data)
        self.destroy()

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    app = ProductivityApp()
    app.mainloop()
