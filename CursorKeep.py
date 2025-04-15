import tkinter as tk
from tkinter import ttk
import threading
import pyautogui
import time
import os
import sys


class MouseMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CursorKeep")
        self.root.geometry("300x180")
        self.root.resizable(False, False)

        self.set_icon()

        self.running = False
        self.intervalo = 30  # segundos
        self.progress = 0

        self.btn_toggle = tk.Button(root, text="Iniciar", width=20, command=self.toggle)
        self.btn_toggle.pack(pady=10)

        self.status_label = tk.Label(root, text="Estado: Inactivo")
        self.status_label.pack()

        self.progress_bar = ttk.Progressbar(
            root, orient="horizontal", length=250, mode="determinate"
        )
        self.progress_bar.pack(pady=15)
        self.progress_bar["maximum"] = self.intervalo

        self.signature_label = tk.Label(
            root, text="by AlexDev", font=("Segoe UI", 9, "italic"), fg="gray"
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
            for i in range(self.intervalo):
                if not self.running:
                    break
                self.progress_bar["value"] = i + 1
                time.sleep(1)
            if self.running:
                pyautogui.moveRel(10, 0, duration=0.1)
                pyautogui.moveRel(-10, 0, duration=0.1)
                pyautogui.press("shift")  # Simula una tecla para evitar suspensión
                print("Cursor movido y Shift presionado")
                self.progress_bar["value"] = 0


if __name__ == "__main__":
    root = tk.Tk()
    app = MouseMoverApp(root)
    root.mainloop()
