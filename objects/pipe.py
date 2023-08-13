import math
import configparser
# import RPi.GPIO as GPIO


class Pipe:
    def __init__(self, valve_number: int):
        """
        Initializes a Pipe instance with the given valve number.
        """
        self.valve_number = valve_number
        self.mass_flow = 0
        self.is_Active = False
        self.is_open = False
        # save the corresponding pins for each valve
        self.valve_pin = [17, 27, 23, 24][self.valve_number-1]
        # GPIO.setup(self.valve_pin, GPIO.OUT)
        print("setup")

    def get_valve_num(self) -> int:
        return self.valve_number

    def open_pipe(self) -> None:
        """
        Opens the pipe valve by sending a HIGH signal to the valve pin.
        """
        if (self.is_Active != False):
            self.is_open = True
            # GPIO.output(self.valve_pin, GPIO.HIGH)
            print("open")

    def close_pipe(self) -> None:
        """
        Closes the pipe valve by sending a LOW signal to the valve pin.
        """
        # GPIO.output(self.valve_pin, GPIO.LOW)
        self.is_open = False
        print("close")

    def is_open(self) -> bool:
        """
        Returns True if the pipe valve is open, False otherwise.
        """
        return self.is_open

    def deactivate(self) -> None:
        """
        Deactivates the pipe.
        """
        self.is_Active = False

    def activate(self) -> None:
        """
        Activates the pipe.
        """
        self.is_Active = True

    def is_active(self) -> bool:
        """
        Returns True if the pipe is active, False otherwise.
        """
        return self.is_Active

    def set_mass_flow(self, mass_flow: float) -> None:
        """
        Sets the mass flow rate and activates the pipe.
        """
        self.mass_flow = mass_flow
        self.activate()

    def get_mass_flow(self) -> int:
        """
        Returns the current mass flow rate.
        """
        return self.mass_flow

    def calculate_mass_flows_from_pressure(self, pressure: float) -> None:
        """
        Calculates mass flows based on pressure and updates configuration.
        """
        dict_valves = {
            1: [0.45442, 5],
            2: [0.65442, 7],
            3: [0.85442, 9],
            4: [1.05442, 9.75],
        }

        x = ((pressure * math.pow(10, 4))/1000 + 0.25442)*19.62
        y = (0.02476 * dict_valves[self.pipe_num][0] /
             0.013868) + dict_valves[self.pipe_num][1]
        v = math.pow(x/y, 0.5)
        q = math.pow(0.013868/2, 2) * math.pi * v
        self.mass_flow = q*1000
        config = configparser.ConfigParser()
        config.read('configuration/config.ini')
        config['Callibration'][f'valve{self.pipe_num}'] = str(self.mass_flow)
        with open('configuration/config.ini', 'w') as configfile:
            config.write(configfile)

    # calculate the time needed to fill the given amount of water
    def calculate_time(self, water_amount: float) -> float:
        time = ((float(water_amount)*math.pow(10, -3)) /
                float(self.mass_flow)) + 0.15 + 0.3
        return time
