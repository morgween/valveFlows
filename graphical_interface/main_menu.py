import tkinter as tk
import time
import configparser
from tkinter import messagebox
from apscheduler.schedulers.background import BackgroundScheduler
from graphical_interface.calibration_window import Calibration_window
from graphical_interface.calibration_window import on_validate
from objects.pipe import Pipe


class ScrollersWidget(tk.Frame):
    def __init__(self, root) -> None:
        super().__init__(root)
        self.create_widget()
        self.pack(fill='y')

    def create_widget(self) -> None:
        self.hour_frame = tk.Frame(self, bg='white')
        self.min_frame = tk.Frame(self, bg='white')
        self.hour_scroller = tk.Scale(self.hour_frame, from_=00,
                                      to=23, length=250, orient='horizontal')
        self.min_scroller = tk.Scale(self.min_frame, from_=00,
                                     to=59, length=250, orient='horizontal')
        self.hour_label = tk.Label(self.hour_frame, text='Hour', bg='white')
        self.min_label = tk.Label(self.min_frame, text='Minute', bg='white')
        self.hour_scroller.pack(side='left')
        self.hour_label.pack(side='left')
        self.min_scroller.pack(side='left')
        self.min_label.pack(side='left')
        self.hour_frame.pack(side='top')
        self.min_frame.pack(side='top')

    def get_time_str(self) -> str:
        hour = self.hour_scroller.get()
        minute = self.min_scroller.get()
        if len(hour) == 1:
            hour = '0'+hour
        if len(minute) == 1:
            minute = '0'+minute
        return hour+':'+minute

    def get_time_int(self) -> int:
        hour = self.hour_scroller.get()
        minute = self.min_scroller.get()
        return int(hour), int(minute)


class MenuWindow:
    def __init__(self, pipes: list[Pipe]) -> None:
        self.root = tk.Tk()
        self.root.geometry('800x480')
        self.root.title('Menu')
        self.root.configure(bg='white')
        self.pipes = pipes
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.header_frame = self.create_header_frame()
        self.section_frames = [self.create_section_frame(
            column) for column in range(1, 5)]

    def destroy_widgets(self) -> None:
        for section in self.section_frames:
            section.destroy()
        self.header_frame.destroy()

    def on_calibration_clicked(self) -> None:
        calibration_window = Calibration_window(self.pipes, self)
        calibration_window.run()
        self.root.wait_window(calibration_window.window)
        self.update_header_frame()

    def on_reset_button_clicked(self) -> None:
        config = configparser.ConfigParser()
        config.read('configuration/config.ini')
        for pipe in range(1, 5):
            self.pipes[pipe - 1].mass_flow = 0
            self.pipes[pipe - 1].openning_time = 0
            self.pipes[pipe - 1].is_Active = False
            config['Callibration'][f'valve{pipe}'] = '0'
        config['Callibration']['is_calibrated'] = 'False'
        with open('configuration/config.ini', 'w') as configfile:
            config.write(configfile)
        self.update_header_frame()

    def add_button_clicked(self) -> None:
        pass

    def on_check_calibration_clicked(self) -> None:
        pass

    def on_off_clicked(self) -> None:
        pass

    def create_header_frame(self) -> tk.Frame:
        pass

    def update_header_frame(self) -> None:
        pass

    def create_section_frame(self) -> tk.Frame:
        validate_num = self.root.registrer(on_validate)
        pass

    def run(self):
        self.root.mainloop()
