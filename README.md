# Enhanced Soundboard developed in Python

This is a completely free, simple, and flexible open-source soundboard application that lets you bind sound files to keyboard keys. It's perfect for streamers, presenters, or anyone needing quick access to sound effects. It has a CC0 license, so you can use it as you please.

![image](https://github.com/user-attachments/assets/09a770ab-7624-48a0-9a43-c94c04d2608a)

## Features

- **Key Binding**: Bind any sound file (MP3/WAV) to almost any keyboard key
- **Dynamic Stop Key**: Configurable "Stop All Sounds" key (default: Numpad 0)
- **Master Volume Control**: Adjust volume for all sounds through a single slider
- **Sound Testing**: Test sounds directly from the interface with a stop function
- **Persistent Configuration**: Your bindings are automatically saved and loaded between sessions
- **User-Friendly Interface**: Clean, intuitive design with human-readable key names

## Usage

### Getting Started
1. Download the latest release from the Releases section
2. Run the `.exe` file - no installation required
3. The application will start with a clean configuration

### Creating Sound Bindings
1. Click "+ Add New Binding"
2. Press any key you want to bind
3. Select a sound file (MP3 or WAV)
4. Your binding will be saved automatically

### Managing Bindings
- **Test Sounds**: Click "Test" to play a sound, "Stop" to stop it
- **Delete Bindings**: Remove any binding using the "Delete" button
- **Stop All Sounds**: Use the configurable stop key (default: Numpad 0)
- **Change Stop Key**: Click "Change Stop Key" and press your preferred key

### Volume Control
- Use the master volume slider to adjust the volume of all sounds
- Volume settings apply to both active soundboard and sound testing

## Notes
- When the soundboard is running, bound keys will be intercepted by the application
- The stop key binding is preserved between sessions
- Supported file formats: MP3 and WAV

## Technical Requirements
- Windows Operating System
- No additional software installation required
- Runs from a single executable file

## Building from Source
If you want to run from the Python source:
1. Ensure you have Python 3.x installed
2. Install required packages:
   ```
   pip install pygame pynput
   ```
3. Run `soundboard_gui.py`

## License
CC0
