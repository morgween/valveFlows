# valveFlows
valveFlows is a Raspberry Pi–oriented Python application that opens and closes up to four water valves through a touchscreen-friendly Tkinter interface. The app lets you calibrate each valve (manually or from pressure readings), schedule daily opening times with the APScheduler background scheduler, and track the current calibration state through a lightweight configuration file.

## Features
- **Four-valve control** with configurable GPIO pins (commented for offline development).
- **Calibration workflows**: enter measured flow rates manually or derive them from pressure readings to automatically update stored mass flows.
- **Daily scheduling UI** to pick times and water amounts for each valve using a touch-friendly scroller widget.
- **Status indicators** that reflect calibration readiness, activation state, and valve open/closed status.
- **Persistent settings** saved in `configuration/config.ini` so calibration survives restarts.

## Project structure
- `main.py` – application entry point that initializes valve objects and launches the Tkinter menu window.
- `graphical_interface/` – Tkinter windows and widgets for calibration, scheduling, and navigation.
  - `main_menu.py` – main dashboard, scheduling logic, and calibration/reset controls.
  - `calibration_window.py` – manual and pressure-based calibration flows plus input validation helpers.
  - `scroller.py` – reusable hour/minute selector used when scheduling valve activations.
- `objects/pipe.py` – `Pipe` class for valve metadata, GPIO pin mapping, flow calculations, and timing helpers.
- `configuration/config.ini` – persistent calibration values and a flag indicating whether calibration is complete.

## Requirements
- Python 3.10+ on Raspberry Pi OS or another Linux distribution.
- Tkinter (often packaged as `python3-tk`).
- [`APScheduler`](https://apscheduler.readthedocs.io/en/stable/) for background scheduling.
- `RPi.GPIO` when running on Raspberry Pi hardware (the import is commented out in `objects/pipe.py` to ease development on other platforms).

Install dependencies with:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install apscheduler RPi.GPIO  # RPi.GPIO only on Raspberry Pi
```

## Running the app
1. Ensure the configuration directory is writable (the app updates `configuration/config.ini`).
2. Activate your virtual environment if you created one.
3. Start the GUI:

   ```bash
   python main.py
   ```

The main window will open at `800x480`, suitable for common Raspberry Pi touchscreens. The background scheduler starts automatically and will dispatch valve open/close jobs at the selected times.

## Using the interface
### Calibration
- **Manual calibration**: open each valve, measure flow with a container, and enter the mass flow for all four valves. Press **APPLY** to write the values and mark the system as calibrated.
- **Pressure-based calibration**: enter the pressure from your manometer. The app computes the mass flows for all valves, saves them, and marks calibration complete.
- Use **Check calibration** in the header to review stored values. **Reset all** clears calibration data and disables scheduling until you calibrate again.

### Scheduling valve operations
1. Toggle a valve’s **OFF/ON** switch to activate it (inactive valves cannot be scheduled).
2. Press **+** under a valve to pick a daily time and the amount of water (ml). The job will appear in the list and be registered with the scheduler.
3. Remove a scheduled time by pressing the **X** beside it.
4. The colored circles and status labels indicate whether each valve is currently open or closed.

### GPIO notes
- Valve pins are mapped in `objects/pipe.py` to BCM pins `[17, 27, 23, 24]` for valves 1–4.
- GPIO calls are currently commented to allow development on non-Pi systems. Uncomment them on Raspberry Pi hardware and ensure proper wiring and safety precautions.

## Configuration
Calibration values and the `is_calibrated` flag live in `configuration/config.ini`. Manual and pressure-based calibration flows update this file automatically. You can reset it with the **Reset all** button or by editing the file directly when the app is closed.

## Troubleshooting
- If the GUI fails to start, verify that `python3-tk` is installed and that your display is available (e.g., `export DISPLAY=:0` when using X forwarding).
- APScheduler jobs rely on system time. Ensure the Raspberry Pi clock is correct to avoid unexpected scheduling.
- When running without GPIO hardware, keep the GPIO import commented to prevent import errors.

## Contributing
Issues and pull requests are welcome. Please follow PEP 8 style conventions and include a brief description of any UI changes or new scheduling behaviors.
