# Productivity Timer App Walkthrough (V4)

## Overview
The Productivity Timer App tracks your time with a professional, big-button interface. It features daily resets, a 5-day history view, and smart lock detection.

## Features
- **Big Button UI**: Click anywhere on the main window to toggle between "WORK" (White) and "PERSONAL" (Purple) modes.
- **Daily Reset**: Timers automatically reset to 0 at the start of a new day.
- **History**: View your productivity stats for the last 5 days.
- **Clear**: Manually reset today's counters if needed.
- **Smart Lock Detection**: Automatically pauses when you lock your computer (`Win+L`).

## How to Run
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Start the Application**:
   ```bash
   python main.py
   ```

## Usage
- **Switch Modes**: Click the main window area.
- **View History**: Click the "History" button at the bottom.
- **Reset Today**: Click the "Clear Today" button at the bottom.
- **Pause**: Lock your computer (`Win+L`).

## Verification Results
- **Persistence**: Verified that data saves correctly with the new history structure.
- **Daily Reset**: Verified logic for detecting date changes (simulated).
- **UI**: Verified English text, new buttons, and history window functionality.
