import pygame
from pynput import keyboard
import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog
import json
from tkinter.messagebox import showinfo, showerror

class SoundBoardGUI:
    def __init__(self):
        self.soundboard = None
        self.root = tk.Tk()
        self.root.title("Enhanced Soundboard")
        self.root.geometry("600x700")
        
		# Add this line
        self.test_buttons = {}  # To track test button states
        
        # Configure grid weight for full width
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Apply styling
        self.style = ttk.Style()
        self.style.configure('Custom.TFrame', background='#f0f0f0')
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        self.style.configure('Custom.TButton', padding=5)
        
        # Comprehensive key name mapping
        self.key_names = {
            # Number pad
            96: 'Numpad 0', 97: 'Numpad 1', 98: 'Numpad 2', 99: 'Numpad 3',
            100: 'Numpad 4', 101: 'Numpad 5', 102: 'Numpad 6',
            103: 'Numpad 7', 104: 'Numpad 8', 105: 'Numpad 9',
            # Standard numbers
            48: '0', 49: '1', 50: '2', 51: '3', 52: '4',
            53: '5', 54: '6', 55: '7', 56: '8', 57: '9',
            # Function keys
            112: 'F1', 113: 'F2', 114: 'F3', 115: 'F4',
            116: 'F5', 117: 'F6', 118: 'F7', 119: 'F8',
            120: 'F9', 121: 'F10', 122: 'F11', 123: 'F12',
            # Letters
            65: 'A', 66: 'B', 67: 'C', 68: 'D', 69: 'E',
            70: 'F', 71: 'G', 72: 'H', 73: 'I', 74: 'J',
            75: 'K', 76: 'L', 77: 'M', 78: 'N', 79: 'O',
            80: 'P', 81: 'Q', 82: 'R', 83: 'S', 84: 'T',
            85: 'U', 86: 'V', 87: 'W', 88: 'X', 89: 'Y', 90: 'Z',
            # Special keys
            32: 'Space', 13: 'Enter', 27: 'Esc', 9: 'Tab',
            16: 'Shift', 17: 'Ctrl', 18: 'Alt',
            37: 'Left', 38: 'Up', 39: 'Right', 40: 'Down'
        }
        
        self.setup_gui()
        self.load_config()
        
    def setup_gui(self):
        # Main container with padding
        main_container = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_container.grid(row=0, column=0, sticky="nsew")
        main_container.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_container, text="Soundboard Configuration", style='Header.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 20), sticky="ew")
        
        # Master volume control
        volume_frame = ttk.LabelFrame(main_container, text="Master Volume", padding="10")
        volume_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        volume_frame.grid_columnconfigure(0, weight=1)
        
        self.volume_var = tk.DoubleVar(value=100)
        volume_scale = ttk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                               variable=self.volume_var, command=self.update_volume)
        volume_scale.grid(row=0, column=0, sticky="ew", padx=10)
        
        # Stop key binding section
        stop_frame = ttk.LabelFrame(main_container, text="Stop All Sounds Key", padding="10")
        stop_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        stop_frame.grid_columnconfigure(1, weight=1)
        
        self.stop_key_label = ttk.Label(stop_frame, text=self.key_names.get(96, "Numpad 0"))
        self.stop_key_label.grid(row=0, column=0, padx=5)
        
        ttk.Button(stop_frame, text="Change Stop Key",
                  command=self.change_stop_key).grid(row=0, column=1, padx=5)
        
        # Bindings section
        bindings_label = ttk.Label(main_container, text="Sound Bindings", style='Header.TLabel')
        bindings_label.grid(row=3, column=0, pady=(0, 10), sticky="ew")
        
        # Bindings list
        self.bindings_frame = ttk.Frame(main_container)
        self.bindings_frame.grid(row=4, column=0, sticky="nsew")
        self.bindings_frame.grid_columnconfigure(0, weight=1)
        
        # Controls frame
        controls_frame = ttk.Frame(main_container)
        controls_frame.grid(row=5, column=0, sticky="ew", pady=20)
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=1)
        
        # Add binding button
        ttk.Button(controls_frame, text="+ Add New Binding", 
                  command=self.add_binding, style='Custom.TButton').grid(row=0, column=0, padx=5, sticky="ew")
        
        # Start/Stop button
        self.start_button = ttk.Button(controls_frame, text="Start Soundboard",
                                     command=self.toggle_soundboard, style='Custom.TButton')
        self.start_button.grid(row=0, column=1, padx=5, sticky="ew")

    def update_volume(self, *args):
        volume = self.volume_var.get() / 100
        if self.soundboard:
            # Update volume for soundboard sounds
            for sound in self.soundboard.sounds.values():
                sound.set_volume(volume)
        # Always set the global mixer volume
        pygame.mixer.set_num_channels(32)  # Ensure we have enough channels
        for i in range(pygame.mixer.get_num_channels()):
            pygame.mixer.Channel(i).set_volume(volume)
            
    def change_stop_key(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Change Stop Key")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        
        ttk.Label(dialog, text="Press any key to set as new stop key...",
                 font=('Arial', 12)).pack(pady=20)
        
        key_label = ttk.Label(dialog, text="", font=('Arial', 11))
        key_label.pack(pady=10)
        
        def on_key(key):
            if hasattr(key, 'vk') and key.vk:
                # Update the stop key in mappings
                old_stop_key = next(k for k, v in self.key_mappings.items() if v is None)
                del self.key_mappings[old_stop_key]
                self.key_mappings[key.vk] = None
                
                # Update the display
                self.stop_key_label.config(text=self.key_names.get(key.vk, f"Key {key.vk}"))
                self.save_config()
                dialog.destroy()
                return False
        
        # Start key listener for the dialog
        listener = keyboard.Listener(on_press=on_key)
        listener.start()
        
        dialog.grab_set()
    
    def update_bindings_display(self):
        """Update the display of current bindings"""
        # Clear test buttons dictionary since we're rebuilding the display
        self.test_buttons.clear()
        
        for widget in self.bindings_frame.winfo_children():
            widget.destroy()
            
        # Create a scrollable frame for bindings
        canvas = tk.Canvas(self.bindings_frame, height=300, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.bindings_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_width())
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas.find_all()[0], width=e.width))
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Configure grid weights for full width
        scrollable_frame.grid_columnconfigure(1, weight=1)
        
        # Grid layout for headers
        ttk.Label(scrollable_frame, text="Key", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(scrollable_frame, text="Sound File", font=('Arial', 10, 'bold')).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        ttk.Label(scrollable_frame, text="Actions", font=('Arial', 10, 'bold')).grid(row=0, column=2, padx=10, pady=5, sticky="e")
        
        # Add each binding
        for row, (key_code, sound_file) in enumerate(self.key_mappings.items(), start=1):
            if sound_file is not None:  # Skip the stop key
                frame = ttk.Frame(scrollable_frame)
                frame.grid(row=row, column=0, columnspan=3, sticky="ew", pady=2)
                frame.grid_columnconfigure(1, weight=1)
                
                # Show key name instead of code
                key_name = self.key_names.get(key_code, f"Key {key_code}")
                ttk.Label(frame, text=key_name).grid(row=0, column=0, padx=10, sticky="w")
                
                # Show sound file
                sound_name = os.path.basename(str(sound_file))
                ttk.Label(frame, text=sound_name).grid(row=0, column=1, padx=10, sticky="w")
                
                # Buttons frame
                buttons_frame = ttk.Frame(frame)
                buttons_frame.grid(row=0, column=2, padx=10, sticky="e")
                
                # Test button
                test_btn = ttk.Button(buttons_frame, text="Test", 
                          command=lambda k=key_code: self.test_sound(k))
                test_btn.pack(side=tk.LEFT, padx=2)
                self.test_buttons[key_code] = test_btn  # Store reference to button
                
                # Delete button
                ttk.Button(buttons_frame, text="Delete",
                          command=lambda k=key_code: self.delete_binding(k)).pack(side=tk.LEFT, padx=2)
        
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure canvas weight
        self.bindings_frame.grid_columnconfigure(0, weight=1)
        self.bindings_frame.grid_rowconfigure(0, weight=1)
        
    def test_sound(self, key_code):
        """Test a sound binding"""
        button = self.test_buttons.get(key_code)
        
        # Ensure mixer is initialized if we're testing without soundboard
        if not self.soundboard and not pygame.mixer.get_init():
            pygame.mixer.init()
        
        # If this button is in Stop state, stop the sound
        if button and button.cget('text') == "Stop":
            if self.soundboard:
                self.soundboard.stop_all_sounds()
            else:
                pygame.mixer.stop()
            # Reset all buttons to Test state
            for btn in self.test_buttons.values():
                btn.config(text="Test")
            return

        # Reset any other buttons to Test state
        for btn in self.test_buttons.values():
            btn.config(text="Test")
            
        # Stop any currently playing sound
        if self.soundboard:
            self.soundboard.stop_all_sounds()
        else:
            pygame.mixer.stop()
        
        # Start test playback
        volume = self.volume_var.get() / 100
        if self.soundboard is None:
            temp_soundboard = SoundBoard(self.key_mappings)
            # Apply current volume to temp soundboard
            for sound in temp_soundboard.sounds.values():
                sound.set_volume(volume)
            temp_soundboard.play_sound(key_code)
        else:
            self.soundboard.play_sound(key_code)
        
        # Update button state
        if button:
            button.config(text="Stop")
                                    
    def add_binding(self):
        """Start the process of adding a new key binding"""
        dialog = tk.Toplevel(self.root)
        dialog.title("New Sound Binding")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        
        # Style the dialog
        ttk.Label(dialog, text="Press any key to bind...", 
                 font=('Arial', 12)).pack(pady=20)
        
        key_label = ttk.Label(dialog, text="", font=('Arial', 11))
        key_label.pack(pady=10)
        
        file_label = ttk.Label(dialog, text="No sound file selected", font=('Arial', 11))
        file_label.pack(pady=10)
        
        captured_key = None
        sound_file = None
        
        def on_key(key):
            nonlocal captured_key
            if hasattr(key, 'vk') and key.vk:
                if key.vk in self.key_mappings:
                    key_label.config(text="Key already in use! Press another key.")
                    return True
                key_name = self.key_names.get(key.vk, f"Key {key.vk}")
                key_label.config(text=f"Selected: {key_name}")
                captured_key = key.vk
                return False
            return True
        
        def select_sound():
            nonlocal sound_file
            file_path = filedialog.askopenfilename(
                filetypes=[("Sound files", "*.mp3 *.wav")]
            )
            if file_path:
                sound_file = file_path
                file_label.config(text=f"Selected: {os.path.basename(file_path)}")
        
        def save_binding():
            if captured_key is None:
                showerror("Error", "Please press a key first")
                return
            if sound_file is None:
                showerror("Error", "Please select a sound file")
                return
                
            self.key_mappings[captured_key] = sound_file
            self.save_config()
            self.update_bindings_display()
            dialog.destroy()
        
        ttk.Button(dialog, text="Select Sound File", 
                  command=select_sound).pack(pady=10)
        ttk.Button(dialog, text="Save Binding",
                  command=save_binding).pack(pady=10)
        
        # Start key listener for the dialog
        listener = keyboard.Listener(on_press=on_key)
        listener.start()
        
        dialog.grab_set()

    def load_config(self):
        """Load key mappings from config file"""
        self.key_mappings = {}
        try:
            if os.path.exists('soundboard_config.json'):
                with open('soundboard_config.json', 'r') as f:
                    self.key_mappings = json.load(f)
                # Convert string keys back to integers
                self.key_mappings = {int(k): v for k, v in self.key_mappings.items()}
            
# Ensure there's a stop key
            if not any(v is None for v in self.key_mappings.values()):
                self.key_mappings[96] = None  # Default to Numpad 0 if no stop key exists
        except Exception as e:
            showerror("Error", f"Failed to load configuration: {e}")
            # Initialize with just the stop key
            self.key_mappings = {96: None}  # Numpad 0 as default stop key
            
        self.update_bindings_display()
        # Update stop key label
        stop_key = next(k for k, v in self.key_mappings.items() if v is None)
        self.stop_key_label.config(text=self.key_names.get(stop_key, f"Key {stop_key}"))

    def save_config(self):
        """Save current key mappings to config file"""
        try:
            with open('soundboard_config.json', 'w') as f:
                json.dump(self.key_mappings, f)
        except Exception as e:
            showerror("Error", f"Failed to save configuration: {e}")
    
    def delete_binding(self, key_code):
        """Delete a key binding"""
        if key_code in self.key_mappings:
            # Ensure mixer is initialized if needed
            if not self.soundboard and not pygame.mixer.get_init():
                pygame.mixer.init()
                
            # Stop any playing sound for this binding
            if self.soundboard:
                self.soundboard.stop_all_sounds()
            else:
                pygame.mixer.stop()
            
            # Remove from mappings
            del self.key_mappings[key_code]
            
            # Remove from test buttons
            if key_code in self.test_buttons:
                del self.test_buttons[key_code]
                
            self.save_config()
            self.update_bindings_display()
                    
    def toggle_soundboard(self):
        """Start or stop the soundboard"""
        if self.soundboard is None:
            self.start_soundboard()
        else:
            self.stop_soundboard()
    
    def start_soundboard(self):
        """Start the soundboard with current configuration"""
        if self.soundboard is None:
            self.soundboard = SoundBoard(self.key_mappings)
            # Apply current volume
            self.update_volume()
            threading.Thread(target=self.soundboard.run, daemon=True).start()
            self.start_button.config(text="Stop Soundboard")
            showinfo("Soundboard", "Soundboard is now running!")
    
    def stop_soundboard(self):
        """Stop the soundboard"""
        if self.soundboard:
            self.soundboard.stop()
            self.soundboard = None
            self.start_button.config(text="Start Soundboard")
            showinfo("Soundboard", "Soundboard stopped!")
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

class SoundBoard:
    def __init__(self, key_mappings):
        # Initialize pygame mixer
        pygame.mixer.init()
        self.running = True
        
        # Dictionary to store our sound mappings
        self.sounds = {}
        
        # Track currently playing sound
        self.current_sound = None
        
        # Store key mappings
        self.key_map = key_mappings
        
        # Load sounds
        self.load_sounds()
        
    def load_sounds(self):
        """Load all sound files defined in key_map"""
        for vk_code, sound_file in self.key_map.items():
            if sound_file:  # Skip None values (like stop key)
                try:
                    if os.path.exists(sound_file):
                        self.sounds[vk_code] = pygame.mixer.Sound(sound_file)
                        print(f"Successfully loaded: {sound_file}")
                    else:
                        print(f"File not found: {sound_file}")
                except pygame.error as e:
                    print(f"Error loading {sound_file}: {e}")

    def win32_event_filter(self, msg, data):
        """Filter keyboard events before they're propagated"""
        # msg 256 is WM_KEYDOWN, msg 257 is WM_KEYUP
        if msg in [256, 257]:  # We only care about key down/up events
            if data.vkCode in self.key_map:  # Check if it's one of our mapped keys
                if msg == 256:  # Key down event
                    stop_key = next(k for k, v in self.key_map.items() if v is None)
                    if data.vkCode == stop_key:  # Stop key
                        self.stop_all_sounds()
                    elif data.vkCode in self.sounds:
                        self.play_sound(data.vkCode)
                # Suppress our mapped keys
                self.listener._suppress = True
                return True
        
        # Let all other keys pass through
        self.listener._suppress = False
        return True

    def play_sound(self, vk_code):
        """Play the sound associated with the key"""
        # Stop current sound if playing
        self.stop_all_sounds()
        
        # Play new sound
        if vk_code in self.sounds:
            self.current_sound = self.sounds[vk_code]
            self.current_sound.play()
            
    def stop_all_sounds(self):
        """Stop all currently playing sounds"""
        if self.current_sound:
            self.current_sound.stop()
            self.current_sound = None
            
    def stop(self):
        """Stop the soundboard"""
        self.running = False
        if hasattr(self, 'listener'):
            self.listener.stop()
        pygame.mixer.quit()

    def run(self):
        """Start the soundboard"""
        # Start keyboard listener
        self.listener = keyboard.Listener(
            win32_event_filter=self.win32_event_filter,
            suppress=False
        )
        
        with self.listener as listener:
            try:
                listener.join()
            except KeyboardInterrupt:
                self.stop()

if __name__ == "__main__":
    gui = SoundBoardGUI()
    gui.run()