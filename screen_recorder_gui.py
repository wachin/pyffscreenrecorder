import tkinter as tk
import subprocess
import threading
import signal
import os
import psutil

# Obtener la ruta del directorio del script actual
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construir la ruta completa al script ffscreenrecord.sh
ffscreenrecord_path = os.path.join(script_dir, 'src', 'ffscreenrecord.sh')

class ScreenRecorderGUI:
    def __init__(self, master):
        self.master = master
        master.title("Grabador de Pantalla")

        self.start_button = tk.Button(master, text="Iniciar Grabación", command=self.start_recording)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Detener Grabación", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack()

        self.output_text = tk.Text(master, height=10, width=50)
        self.output_text.pack()

        self.process = None

    def start_recording(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)

        def run_ffmpeg():
            self.process = subprocess.Popen(['bash', ffscreenrecord_path],
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.STDOUT,
                                            universal_newlines=True,
                                            preexec_fn=os.setsid)

            for line in self.process.stdout:
                self.output_text.insert(tk.END, line)
                self.output_text.see(tk.END)

            self.process.wait()
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

        threading.Thread(target=run_ffmpeg, daemon=True).start()

    def stop_recording(self):
        if self.process:
            try:
                parent = psutil.Process(self.process.pid)
                for child in parent.children(recursive=True):
                    child.terminate()
                parent.terminate()
            except psutil.NoSuchProcess:
                pass

        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

root = tk.Tk()
app = ScreenRecorderGUI(root)
root.mainloop()
