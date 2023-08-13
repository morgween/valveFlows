from tkinter import Frame, Scale, Label


class Scroller(Frame):
    def __init__(self, root) -> None:
        super().__init__(root)
        self.create_widget()
        self.pack(fill='y')

    def create_widget(self) -> None:
        self.hour_frame = Frame(self, bg='white')
        self.min_frame = Frame(self, bg='white')
        self.hour_scroller = Scale(self.hour_frame, from_=00,
                                   to=23, length=250, orient='horizontal')
        self.min_scroller = Scale(self.min_frame, from_=00,
                                  to=59, length=250, orient='horizontal')
        self.hour_label = Label(self.hour_frame, text='Hour', bg='white')
        self.min_label = Label(self.min_frame, text='Minute', bg='white')
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
