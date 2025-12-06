import time
import ctypes
import threading
from storage import save_full_data

class Monitor:
    def __init__(self, data_dict):
        self.data = data_dict
        self.is_work_mode = True # Default to work mode
        self.running = False
        self.lock = threading.Lock()
        self._thread = None

    def set_mode(self, is_work):
        with self.lock:
            self.is_work_mode = is_work

    def is_workstation_locked(self):
        """Checks if the workstation is locked."""
        user32 = ctypes.windll.user32
        h_desktop = user32.OpenInputDesktop(0, False, 0x0100)
        if h_desktop == 0:
            return True
        user32.CloseDesktop(h_desktop)
        
        hwnd = user32.GetForegroundWindow()
        if hwnd == 0:
            return True
        return False

    def start(self):
        if self.running:
            return
        self.running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join()

    def _loop(self):
        last_time = time.time()
        while self.running:
            current_time = time.time()
            elapsed = current_time - last_time
            last_time = current_time

            if not self.is_workstation_locked():
                with self.lock:
                    if self.is_work_mode:
                        self.data["work"] += elapsed
                    else:
                        self.data["personal"] += elapsed
                
                # Save periodically
                if int(current_time) % 5 == 0:
                     save_full_data(self.data)
            
            time.sleep(1)

    def get_times(self):
        with self.lock:
            return self.data["work"], self.data["personal"]
            
    def reset_today(self):
        with self.lock:
            self.data["work"] = 0.0
            self.data["personal"] = 0.0
            save_full_data(self.data)
