import tkinter as tk
import time
import configparser
from tkinter import messagebox
from graphical_interface.calibration_window import Calibration_window
from graphical_interface.calibration_window import on_validate
from graphical_interface.scroller import Scroller
from objects.pipe import Pipe
from apscheduler.schedulers.background import BackgroundScheduler

class MenuWindow:
    def __init__(self, pipes: list[Pipe]) -> None:
        self._root = tk.Tk()
        self._root.geometry('800x480')
        self._root.title('Menu')
        self._root.configure(bg='white')
        self.pipes = pipes
        self._scheduler = BackgroundScheduler()
        self._scheduler.start()
        self.header_frame = self.create_header_frame()
        self.section_frames = [self.create_section_frame(
            column) for column in range(1, 5)]
        self.time_frames_list = []

    def _on_calibration_clicked(self) -> None:
        calibration_window = Calibration_window(self.pipes, self)
        calibration_window.run()
        self._root.wait_window(calibration_window.menu_window)
        self.update_header_frame()

    def _on_reset_button_clicked(self) -> None:
        config = configparser.ConfigParser()
        config.read('configuration/config.ini')
        for pipe in range(1, 5):
            self.pipes[pipe - 1].mass_flow = 0
            self.pipes[pipe - 1].openning_time = 0
            self.pipes[pipe - 1].is_Active = False
            config['Calibration'][f'valve{pipe}'] = '0'
        config['Calibration']['is_calibrated'] = 'False'
        with open('configuration/config.ini', 'w') as configfile:
            config.write(configfile)
        self.update_header_frame()

    def _on_check_calibration_clicked(self) -> None:
        config = configparser.ConfigParser()
        config.read('configuration/config.ini')
        if config['Calibration'].getboolean('is_calibrated'):
            calibration_check_window = tk.Toplevel(self._root)
            calibration_check_window.geometry('500x230')
            calibration_check_window.title('Calibration check')
            calibration_check_window.resizable(False, False)
            calibration_check_window.configure(background='white')
            calibration_check_window.grab_set()
            calibration_check_window.focus_set()
            calibration_check_window.transient(self._root)
            calibration_check_window.attributes("-topmost", True)
            calibration_check_window.protocol(
                "WM_DELETE_WINDOW", lambda: calibration_check_window.destroy())
            text_label = tk.Label(
                calibration_check_window, text="The device is calibrated, mass flows are:", bg='white', font=("Helvetica", 24))
            pipe1_label = tk.Label(
                calibration_check_window, text=f"Pipe 1 : {config['Calibration']['valve1']}", bg='white', font=("Helvetica", 32))
            pipe2_label = tk.Label(
                calibration_check_window, text=f"Pipe 2 : {config['Calibration']['valve2']}", bg='white', font=("Helvetica", 32))
            pipe3_label = tk.Label(
                calibration_check_window, text=f"Pipe 3 : {config['Calibration']['valve3']}", bg='white', font=("Helvetica", 32))
            pipe4_label = tk.Label(
                calibration_check_window, text=f"Pipe 4 : {config['Calibration']['valve4']}", bg='white', font=("Helvetica", 32))
            text_label.pack()
            pipe1_label.pack()
            pipe2_label.pack()
            pipe3_label.pack()
            pipe4_label.pack()
        else:
            messagebox.showinfo(
                "Calibration", "The device is not calibrated.")

    def create_header_frame(self):
        self.header_frame = tk.Frame(self._root, height=120, bg='white')
        self.header_frame.pack(fill='x')

        self.left_frame = tk.Frame(self.header_frame, bg='white')
        self.left_frame.pack(side='left')
        config = configparser.ConfigParser()
        config.read('configuration/config.ini')
        if (config['Calibration']['is_calibrated'] == 'False'):
            calibrate_button_state = tk.NORMAL
        else:
            calibrate_button_state = tk.DISABLED
        self.calibrate_button = tk.Button(self.header_frame, text='Calibrate', command=self._on_calibration_clicked,
                                          background='#8aecff', width=12, height=3, state=calibrate_button_state)

        self.calibrate_button.pack(side='right', padx=10)

        check_calibration_button = tk.Button(self.header_frame, text='Check calibration', command=self._on_check_calibration_clicked,
                                             background='#8aecff', width=12, height=3)
        check_calibration_button.pack(side='right', padx=10)

        self.reset_all_button = tk.Button(self.header_frame, text='Reset all', command=self._on_reset_button_clicked,
                                          background='#8aecff', width=12, height=3)
        self.reset_all_button.pack(side='right', padx=10)
        self.update_header_frame()
        return self.header_frame

    def update_header_frame(self) -> None:
        config = configparser.ConfigParser()
        config.read('configuration/config.ini')
        is_calibrated = config['Calibration']['is_calibrated']
        label_text1, label_text2 = 'Calibrated', 'Not calibrated'
        if is_calibrated == 'False':
            self.calibrate_button.config(state=tk.NORMAL)
            self.reset_all_button.config(state=tk.DISABLED)
            color1, color2 = 'white', 'blue'
        else:
            self.calibrate_button.config(state=tk.DISABLED)
            self.reset_all_button.config(state=tk.NORMAL)
            color1, color2 = 'blue', 'white'
        if hasattr(self, 'circle1'):
            self.circle1.itemconfig(1, fill=color1)
        else:
            self.circle1 = tk.Canvas(
                self.left_frame, width=40, height=40, bg='white', highlightthickness=0)
            self.circle1.create_oval(
                5, 5, 35, 35, outline='black', fill=color1)
            self.circle1.grid(row=0, column=0, padx=5, pady=5)
        if hasattr(self, 'circle2'):
            self.circle2.itemconfig(1, fill=color2)
        else:
            self.circle2 = tk.Canvas(
                self.left_frame, width=40, height=40, bg='white', highlightthickness=0)
            self.circle2.create_oval(
                5, 5, 35, 35, outline='black', fill=color2)
            self.circle2.grid(row=1, column=0, padx=5, pady=5)
        if hasattr(self, 'label1'):
            self.label1.config(text=label_text1)
        else:
            self.label1 = tk.Label(
                self.left_frame, text=label_text1, bg='white', fg='black')
            self.label1.grid(row=0, column=1, padx=5, pady=5)

        if hasattr(self, 'label2'):
            self.label2.config(text=label_text2)
        else:
            self.label2 = tk.Label(
                self.left_frame, text=label_text2, bg='white', fg='black')
            self.label2.grid(row=1, column=1, padx=5, pady=5)

    def task(self, pipe: int, water_amount: float):
        if not self.pipes[pipe-1].is_Active:
            return
        self.pipes[pipe-1].open_pipe()
        time.sleep(self.pipes[pipe-1].calculate_time(water_amount))
        self.pipes[pipe-1].close_pipe()

    def add_button_clicked(self, pipe_number: int, time_frames_fr: tk.Frame) -> None:
        def on_apply_clicked():
            def remove_label(label, button, frame):
                label.destroy()
                button.destroy()
                frame.destroy()
                self._root.update()
            amount_of_water = float(self.entry_field.get())
            time_sc = time_widget.get_time_str()
            hour, min = time_widget.get_time_int()
            time_frame = tk.Frame(time_frames_fr, bg='white')
            time_label = tk.Label(
                time_frame, text=f'{time_sc}, {self.entry_field.get()}', bg='white')
            time_label.pack(side='left', pady=5)
            remove_button = tk.Button(time_frame, text="X", command=lambda: remove_label(
                time_label, remove_button, time_frame))
            remove_button.pack(side='left', pady=5)
            time_frame.pack(side='top')
            self._scheduler.add_job(self.task, 'cron', args=[
                                   pipe_number, amount_of_water], hour=hour, minute=min)
            time_window.destroy()
            self._root.update()

        validate_num = self._root.register(on_validate)
        config = configparser.ConfigParser()
        config.read('configuration/config.ini')
        if not config['Calibration'].getboolean('is_calibrated'):
            messagebox.showinfo(
                "Calibration", "The device is not calibrated.")
            return
        time_window = tk.Tk()
        time_window.geometry('400x300')
        label = tk.Label(time_window, text='Choose the time (HH:MM): ')
        label.pack(side='top')
        time_widget = Scroller(time_window)
        time_widget.pack(side='top')
        water_amount_label = tk.Label(
            time_window, text="Amount of Water [ml]", bg='white')
        water_amount_label.pack()
        self.entry_field = tk.Entry(
            time_window, validate="key", validatecommand=(validate_num, "%P"))
        self.entry_field.pack(side='top', pady=5)
        apply_button = tk.Button(
            time_window, text="Apply", command=on_apply_clicked)
        apply_button.pack(side='bottom')
        time_window.mainloop()

    def create_section_frame(self, column):
        def on_off_button_clicked(pipe):
            self.pipes[pipe-1].is_Active = not self.pipes[pipe-1].is_Active
            if not self.pipes[pipe-1].is_Active:
                section_frame.config(bg='#adb5bd')
                on_off_button.config(bg='#adb5bd')
                on_off_button.config(fg='#343a40')
                add_button.config(state='disabled')
                add_button.config(bg='#adb5bd')
                add_button.config(fg='#343a40')
            else:
                section_frame.config(bg='white')
                on_off_button.config(state='normal')
                on_off_button.config(bg='white')
                on_off_button.config(fg='black')
                add_button.config(state='normal')
                add_button.config(bg='white')
                add_button.config(fg='black')

        section_frame = tk.Frame(
            self._root, borderwidth=1, relief='solid', bg='white')
        section_frame.pack(fill='both', expand=True, side='left')
        self._root.grid_columnconfigure(column, weight=1)
        time_frames_frame = tk.Frame(section_frame, bg='white')
        valve_label = tk.Label(
            section_frame, text=f"VALVE №{column}", bg='white')
        valve_label.pack(side='top', pady=5)

        add_button = tk.Button(section_frame, bg='white', text='+', font=("Helvetica", 20),
                               borderwidth=0, highlightthickness=0, command=lambda: self.add_button_clicked(column, time_frames_frame))
        add_button.pack(side='top', pady=5)
        on_off_button = tk.Button(
            section_frame, text="OFF/ON", bg='white', command=lambda: on_off_button_clicked(column))
        on_off_button.pack(side='bottom')
        status_frame = tk.Frame(section_frame, bg='white')
        circle = tk.Canvas(status_frame, width=40,
                           height=40, highlightthickness=0, bg='white')
        if (self.pipes[column-1].is_open):
            circle.create_oval(5, 5, 35, 35, outline='black', fill='green')
            status_label = tk.Label(status_frame, text="Opened", bg='white')
        else:
            circle.create_oval(5, 5, 35, 35, outline='black', fill='red')
            status_label = tk.Label(status_frame, text="Closed", bg='white')
        circle.pack(side='left')
        status_label.pack(side='left')
        status_frame.pack(side='bottom')
        if not self.pipes[column-1].is_Active:
            section_frame.config(bg='#adb5bd')
            on_off_button.config(bg='#adb5bd')
            on_off_button.config(fg='#343a40')
            add_button.config(state='disabled')
            add_button.config(bg='#adb5bd')
            add_button.config(fg='#343a40')

        time_frames_frame.pack(side='top')

    def run(self):
        self._root.mainloop()
