# TimeTracker

A productivity timer application that tracks your work and personal time with an intuitive, big-button interface. Automatically pauses when your workstation is locked and maintains a 5-day history of your productivity.

## Features

- **Big Button UI**: Click anywhere on the main window to toggle between "WORK" (White) and "PERSONAL" (Purple) modes
- **Daily Reset**: Timers automatically reset to 0 at the start of a new day
- **History View**: View your productivity stats for the last 5 days
- **Smart Lock Detection**: Automatically pauses when you lock your computer (`Win+L`)
- **Manual Reset**: Clear today's counters with a single click
- **Real-time Tracking**: Continuously tracks time in the background

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the Application**:
   ```bash
   python main.py
   ```

2. **Switch Modes**: Click anywhere on the main window area to toggle between WORK and PERSONAL modes

3. **View History**: Click the "History" button at the bottom to see your productivity stats for the last 5 days

4. **Reset Today**: Click the "Clear Today" button at the bottom to manually reset today's counters

5. **Pause**: Lock your computer (`Win+L`) to automatically pause tracking

## Project Structure

- `main.py` - Main application entry point with GUI using CustomTkinter
- `monitor.py` - Background monitoring thread that tracks time and detects workstation lock state
- `storage.py` - Data persistence layer that handles daily resets and history management
- `data.json` - JSON file storing current day's time and 5-day history

## Requirements

- Python 3.x
- customtkinter
- packaging

## Notes

- Data is automatically saved every 5 seconds
- History is limited to the last 5 days
- The application runs on Windows and uses Windows-specific APIs for lock detection