import tkinter as tk
from tkinter import messagebox
from tkinter import font as TkFont
import configparser

def on_validate(P) -> bool:
    if P == "" or P == ".":
        return True
    try:
        float(P)
        return True
    except ValueError:
        messagebox.showerror(
            "Invalid Input", "Please enter a valid float number.")
        return False


class Calibration_window:
    def __init__(self, pipes, menu_window):
        self._menu_window = menu_window
        self._root = tk.Tk()
        self._valve_num = 1
        self._create_widgets()
        self._pipes = pipes
        self._opened_valve = None
        self._is_done = True
        self._root.title("Calibration")
        self._root.geometry('800x480')

    def _create_widgets(self):
        helv50 = TkFont.Font(family='Helvetica', size=50, weight='bold')

        manual_button = tk.Button(self.root, bg='#8aecff', text='MANUAL',
                                  command=self.on_manual_click, font=helv50, width=30, height=20)
        manual_button.pack(side='left', padx=10, pady=10)
        pressure_button = tk.Button(self.root, bg='#8aecff', text='ONLY WITH THE PRESSURE OF MANOMETER',
                                    command=self.on_pressure_click, font=helv50, width=30, height=20, wraplength=200)
        pressure_button.pack(side='right', padx=10, pady=10)

