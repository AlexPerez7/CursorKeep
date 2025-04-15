import tkinter as tk
from tkinter import ttk
import threading
import pyautogui
import time
import os
import sys


class MouseMoverApp:
    def __init__(self, root):
        # Configuración de ventana
        self.root = root
        self.root.title("CursorKeep")
        self.root.geometry("300x260")
        self.root.resizable(False, False)

        # Tipografías
        self.fuente = ("Segoe UI", 10)
        self.fuente_firma = ("Segoe UI", 9, "italic")

        # Ícono
        self.set_icon()

        # Estado e intervalo
        self.running = False
        self.intervalo_var = tk.IntVar(value=30)

        # Botón Iniciar/Detener
        self.btn_toggle = tk.Button(
            root, text="Iniciar", font=self.fuente, width=20, command=self.toggle
        )
        self.btn_toggle.pack(pady=(15, 10), padx=20)

        # Etiqueta de estado
        self.status_label = tk.Label(root, text="Estado: Inactivo", font=self.fuente)
        self.status_label.pack(pady=5, padx=20)

        # Menú de selección de intervalo
        intervalo_frame = tk.Frame(root)
        intervalo_frame.pack(pady=5, padx=20)

        intervalo_label = tk.Label(
            intervalo_frame, text="Intervalo (segundos):", font=self.fuente
        )
        intervalo_label.grid(row=0, column=0, sticky="w", padx=(0, 10))

        intervalo_menu = ttk.Combobox(
            intervalo_frame,
            textvariable=self.intervalo_var,
            values=[30, 60, 120, 300],
            font=self.fuente,
            state="readonly",
            width=10,
        )
        intervalo_menu.grid(row=0, column=1)

        # Barra de progreso
        self.progress_bar = ttk.Progressbar(
            root, orient="horizontal", length=250, mode="determinate"
        )
        self.progress_bar.pack(pady=15, padx=20)
        self.progress_bar["maximum"] = self.intervalo_var.get()

        # Firma
        self.signature_label = tk.Label(
            root, text="by AlexDev", font=self.fuente_firma, fg="gray"
        )
        self.signature_label.pack(side="bottom", pady=5)

    def set_icon(self):
        if getattr(sys, "frozen", False):
            icon_path = os.path.join(sys._MEIPASS, "cursorkeep.ico")
        else:
            icon_path = "cursorkeep.ico"
        self.root.iconbitmap(icon_path)

    def toggle(self):
        if not self.running:
            self.running = True
            self.btn_toggle.config(text="Detener")
            self.status_label.config(text="Estado: Activo")
            threading.Thread(target=self.mover_cursor, daemon=True).start()
        else:
            self.running = False
            self.btn_toggle.config(text="Iniciar")
            self.status_label.config(text="Estado: Inactivo")
            self.progress_bar["value"] = 0

    def mover_cursor(self):
        while self.running:
            intervalo_actual = self.intervalo_var.get()
            self.progress_bar["maximum"] = intervalo_actual

            for i in range(intervalo_actual):
                if not self.running:
                    break
                self.progress_bar["value"] = i + 1
                time.sleep(1)

            if self.running:
                pyautogui.moveRel(10, 0, duration=0.1)
                pyautogui.moveRel(-10, 0, duration=0.1)
                pyautogui.press("shift")
                print("Cursor movido y Shift presionado")
                self.progress_bar["value"] = 0


if __name__ == "__main__":
    root = tk.Tk()
    app = MouseMoverApp(root)
    root.mainloop()
