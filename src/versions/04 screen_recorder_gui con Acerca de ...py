import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import threading
import signal
import os
import psutil

# Obtener la ruta del directorio del script actual
script_dir = os.path.dirname(os.path.abspath(__file__))
ffscreenrecord_path = os.path.join(script_dir, 'src', 'ffscreenrecord.sh')

class AboutWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Acerca de pyscreenrecorder")
        self.geometry("420x350")
        self.resizable(False, False)

        text = tk.Text(self, wrap=tk.WORD, padx=10, pady=10, relief=tk.FLAT)
        text.pack(expand=True, fill=tk.BOTH)

        # Configurar los estilos para negrita y cursiva
        text.tag_configure("bold", font=("TkDefaultFont", 10, "bold"))
        text.tag_configure("italic", font=("TkDefaultFont", 10, "italic"))

        # Insertar texto con formato
        text.insert(tk.END, "pyscreenrecorder\n\n", "bold")
        text.insert(tk.END, "Graba la pantalla en un rectángulo de 854x480 con el seguimiento del mouse. "
                            "Este rectángulo se moverá alrededor de la pantalla para capturar lo que más le importa "
                            "según donde se mueva.\n\n")
        text.insert(tk.END, "Copyright 2024 © Washington Indacochea Delgado.\n")
        text.insert(tk.END, "wachin.id@gmail.com\n")
        text.insert(tk.END, "Licencia: GNU GPL3.\n\n")
        text.insert(tk.END, "Esta aplicación es una manera sencilla de grabar tu pantalla en Linux sin tener que lidiar "
                            "con complicadas opciones de línea de comandos.\n\n")
        text.insert(tk.END, "Para más información, visite: ", "italic")
        text.insert(tk.END, "https://github.com/wachin/pyffscreenrecorder\n")

        # Deshabilitar el campo de texto para que sea de solo lectura
        text.config(state=tk.DISABLED)

        # Botón para cerrar la ventana
        close_button = ttk.Button(self, text="Cerrar", command=self.destroy)
        close_button.pack(pady=10)

class ScreenRecorderGUI:
    def __init__(self, master):
        self.master = master
        master.title("Grabador de Pantalla")

        # Crear la barra de menú
        menu_bar = tk.Menu(master)
        master.config(menu=menu_bar)

        # Añadir la sección "Ayuda" con "Acerca de..."
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de...", command=self.show_about)

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

    def show_about(self):
        # Mostrar la ventana "Acerca de..." con el formato
        AboutWindow(self.master)

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
