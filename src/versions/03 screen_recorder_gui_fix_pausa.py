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

        # Botón para iniciar grabación
        self.start_button = tk.Button(master, text="Iniciar Grabación", command=self.start_recording)
        self.start_button.pack()

        # Botón para pausar grabación
        self.pause_button = tk.Button(master, text="Pausar Grabación", command=self.pause_recording, state=tk.DISABLED)
        self.pause_button.pack()

        # Botón para reanudar grabación
        self.resume_button = tk.Button(master, text="Reanudar Grabación", command=self.resume_recording, state=tk.DISABLED)
        self.resume_button.pack()

        # Botón para detener grabación
        self.stop_button = tk.Button(master, text="Detener Grabación", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack()

        # Área de texto para mostrar la salida de ffmpeg
        self.output_text = tk.Text(master, height=10, width=50)
        self.output_text.pack()

        # Variable para manejar el proceso de grabación
        self.process = None

    def start_recording(self):
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
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
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)

        threading.Thread(target=run_ffmpeg, daemon=True).start()

    def pause_recording(self):
        if self.process:
            # Enviar la señal SIGSTOP para pausar la grabación
            os.killpg(os.getpgid(self.process.pid), signal.SIGSTOP)
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.NORMAL)

    def resume_recording(self):
        if self.process:
            # Enviar la señal SIGCONT para reanudar la grabación
            os.killpg(os.getpgid(self.process.pid), signal.SIGCONT)
            self.resume_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)

    def stop_recording(self):
        if self.process:
            try:
                # Reanudar el proceso si está pausado, para poder detenerlo correctamente
                os.killpg(os.getpgid(self.process.pid), signal.SIGCONT)

                # Terminar el proceso de grabación
                parent = psutil.Process(self.process.pid)
                for child in parent.children(recursive=True):
                    child.terminate()
                parent.terminate()

            except psutil.NoSuchProcess:
                pass

        # Restablecer el estado de los botones
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.resume_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)

# Iniciar la aplicación
root = tk.Tk()
app = ScreenRecorderGUI(root)
root.mainloop()
