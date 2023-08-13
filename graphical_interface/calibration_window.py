import tkinter as tk
from tkinter import messagebox


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
    def __init__():
        pass
