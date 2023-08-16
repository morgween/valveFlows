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
    def __init__(self, _pipes: list, menu_window):
        self.menu_window = menu_window
        self._root = tk.Tk()
        self._valve_num = 1
        self._pipes = _pipes
        self._opened_valve = None
        self._is_finished = True
        self._root.title("Calibration")
        self._root.geometry('800x480')
        self._create_widgets()

    def _create_widgets(self):
        helv50 = TkFont.Font(family='Helvetica', size=50, weight='bold')

        manual_button = tk.Button(self._root, bg='#8aecff', text='MANUAL',
                                  command=self._manual_calibr, font=helv50, width=30, height=20)
        manual_button.pack(side='left', padx=10, pady=10)
        pressure_button = tk.Button(self._root, bg='#8aecff', text='ONLY WITH THE PRESSURE OF MANOMETER',
                                    command=self._presure_calibr, font=helv50, width=30, height=20, wraplength=200)
        pressure_button.pack(side='right', padx=10, pady=10)

    def _destroy_widgts(self):
        for widget in self._root.winfo_children():
            widget.destroy()

    def _validate_float(self, P):
        if P == "" or P == ".":
            return True
        try:
            float(P)
            return True
        except ValueError:
            messagebox.showerror(
                "Invalid Input", "Please enter a valid float number.")
            return False

    def _manual_calibr(self):
        self._root.geometry('550x450')
        validate_num = self._root.register(self._validate_float)
        self._destroy_widgts()
        text_label = tk.Label(
            self._root, text="OPEN THE VALVES AND MANUALLY RECORD THE FLOW\n FROM EACH VALVE, USING A MEASURING CONTAINER")
        text_label.pack(side='top', padx=10, pady=10)
        # Create four frames for columns

        valves_top = tk.Frame(self._root, width=200)
        valves_bottom = tk.Frame(self._root, width=200)
        valve_frame1 = tk.Frame(valves_top, width=200)
        valve1_open_button = tk.Button(
            valve_frame1, bg='#8aecff', text='OPEN', command=lambda: self.open_valve(1, valve1_open_button))
        valve1_label = tk.Label(valve_frame1, text="Valve №1 mass flow")
        self.valve1_text = tk.Entry(
            valve_frame1, validate="key", validatecommand=(validate_num, "%P"))
        valve1_open_button.pack(side='top', padx=10, pady=10)
        valve1_label.pack(side='top', padx=10, pady=10)
        self.valve1_text.pack(side='top', padx=10, pady=10)

        valve_frame2 = tk.Frame(valves_top, width=200)
        valve2_open_button = tk.Button(
            valve_frame2, bg='#8aecff', text='OPEN', command=lambda: self.open_valve(2, valve2_open_button))
        valve2_label = tk.Label(valve_frame2, text="Valve №2 mass flow")
        self.valve2_text = tk.Entry(
            valve_frame2, validate="key", validatecommand=(validate_num, "%P"))
        valve2_open_button.pack(side='top', padx=10, pady=10)
        valve2_label.pack(side='top', padx=10, pady=10)
        self.valve2_text.pack(side='top', padx=10, pady=10)

        valve_frame3 = tk.Frame(valves_bottom, width=200)
        valve3_open_button = tk.Button(
            valve_frame3, bg='#8aecff', text='OPEN', command=lambda: self.open_valve(3, valve3_open_button))
        valve3_label = tk.Label(valve_frame3, text="Valve №3 mass flow")
        self.valve3_text = tk.Entry(
            valve_frame3, validate="key", validatecommand=(validate_num, "%P"))
        valve3_open_button.pack(side='top', padx=10, pady=10)
        valve3_label.pack(side='top', padx=10, pady=10)
        self.valve3_text.pack(side='top', padx=10, pady=10)

        valve_frame4 = tk.Frame(valves_bottom, width=200)
        valve4_open_button = tk.Button(
            valve_frame4, bg='#8aecff', text='OPEN', command=lambda: self.open_valve(4, valve4_open_button))
        valve4_label = tk.Label(valve_frame4, text="Valve №4 mass flow")
        self.valve4_text = tk.Entry(
            valve_frame4, validate="key", validatecommand=(validate_num, "%P"))
        valve4_open_button.pack(side='top', padx=10, pady=10)
        valve4_label.pack(side='top', padx=10, pady=10)
        self.valve4_text.pack(side='top', padx=10, pady=10)
        self.valves_buttons = [valve1_open_button, valve2_open_button,
                               valve3_open_button, valve4_open_button]
        valve_frame1.pack(side='left', padx=0, pady=0)
        valve_frame2.pack(side='left', padx=0, pady=0)
        valve_frame3.pack(side='left', padx=0, pady=0)
        valve_frame4.pack(side='left', padx=0, pady=0)

        valves_top.pack(side='top', padx=10, pady=10)
        valves_bottom.pack(side='top', padx=10, pady=10)

        button_frame = tk.Frame(self._root, width=200)
        button_frame.pack(side='bottom', pady=5)

        apply_button = tk.Button(
            button_frame, bg='#8aecff', text='APPLY', command=self._apply_manual_calibration)
        apply_button.pack(side='top', padx=10, pady=10)
        self._root.update()

    def open_valve(self, _valve_num, valve_button):
        if self._opened_valve is not None:
            messagebox.showerror(
                "Failure", f"Please close the valve №{self._opened_valve}")
            return
        else:
            valve_button.config(
                text='CLOSE', command=lambda: self.close_valve(_valve_num, valve_button))
            self._opened_valve = _valve_num
            self._pipes[_valve_num-1].open_Pipe()

    def close_valve(self, _valve_num, valve_button):
        valve_button.config(
            text='OPEN', command=lambda: self.open_valve(_valve_num, valve_button))
        self._pipes[_valve_num-1].close_Pipe()
        self._opened_valve = None

    def _apply_manual_calibration(self):
        config = configparser.ConfigParser()
        config.read('configuration/config.ini')
        config['Calibration']['is_calibrated'] = 'True'
        if self.valve1_text.get() == '':
            messagebox.showerror(
                "Failure", "Please enter the mass flow of valve №1")
            return
        if self.valve2_text.get() == '':
            messagebox.showerror(
                "Failure", "Please enter the mass flow of valve №2")
            return
        if self.valve3_text.get() == '':
            messagebox.showerror(
                "Failure", "Please enter the mass flow of valve №3")
            return
        if self.valve4_text.get() == '':
            messagebox.showerror(
                "Failure", "Please enter the mass flow of valve №4")
            return
        self._pipes[0].set_mass_flow(float(self.valve1_text.get()))
        config['Calibration']['valve1'] = self.valve1_text.get()
        self._pipes[1].set_mass_flow(float(self.valve2_text.get()))
        config['Calibration']['valve2'] = self.valve2_text.get()
        self._pipes[2].set_mass_flow(float(self.valve3_text.get()))
        config['Calibration']['valve3'] = self.valve3_text.get()
        self._pipes[3].set_mass_flow(float(self.valve4_text.get()))
        config['Calibration']['valve4'] = self.valve4_text.get()

        with open('configuration/config.ini', 'w') as configfile:
            config.write(configfile)
        self.menu_window.update_header_frame()
        self._root.destroy()

    def _presure_calibr(self):
        def apply_pressure_calibr(pressure):
            config = configparser.ConfigParser()
            config.read('configuration/config.ini')
            for valve in range(4):
                self._pipes[valve].calculate_mass_flows_from_pressure(float(pressure))
                config['Calibration'][f'valve{valve+1}'] = str(
                    self._pipes[valve].get_mass_flow())
            config['Calibration']['is_calibrated'] = 'True'
            with open('configuration/config.ini', 'w') as configfile:
                config.write(configfile)
            self.menu_window.update_header_frame()
            self._destroy_widgts()
            self._root.destroy()
            return

        self._root.geometry('550x450')
        validate_num = self._root.register(self._validate_float)
        self._destroy_widgts()
        text_label = tk.Label(
            self._root, text=f"Open the valve № {self._valve_num} and enter the pressure displayed on manometer", font=(
                "Helvetica", 20), wraplength=450)
        text_label.pack(pady=40)
        input_frame = tk.Frame(self._root)
        input_frame.pack()
        valve_button = tk.Button(input_frame, text=f"Open Valve {self._valve_num}", width=20, height=3, command=lambda: self.open_valve(
            self._valve_num, valve_button), font=("Helvetica", 20))
        valve_button.grid(row=0, column=0, padx=10, pady=10, rowspan=2)
        pressure_label = tk.Label(
            input_frame, text="Pressure [Kg/cm^2]", font=("Helvetica", 20))
        pressure_label.grid(row=0, column=1, padx=0, pady=0)
        pressure_entry = tk.Entry(input_frame, validate="key", validatecommand=(
            validate_num, "%P"), font=("Helvetica", 20))
        pressure_entry.grid(row=1, column=1, padx=0, pady=0)
        apply_button = tk.Button(self._root, text="Apply",
                                 width=20, command=lambda: apply_pressure_calibr(pressure_entry.get()), font=("Helvetica", 20))
        apply_button.pack(pady=20)
        self._root.update()

    def is_working(self):
        return not self._is_finished

    def run(self):
        self._is_finished = False
        self._root.mainloop()
