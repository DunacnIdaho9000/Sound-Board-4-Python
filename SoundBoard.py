import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pygame
import os
import sounddevice as sd

SOUND_FOLDER = "sounds"
os.makedirs(SOUND_FOLDER, exist_ok=True)

sounds = {}
channels = []

# ---------------------------
# AUDIO DEVICE HANDLING
# ---------------------------
def get_output_devices():
    devices = sd.query_devices()
    output_devices = []
    for i, dev in enumerate(devices):
        if dev['max_output_channels'] > 0:
            output_devices.append((i, dev['name']))
    return output_devices

def init_audio(device_index=None):
    pygame.mixer.quit()

    if device_index is not None:
        os.environ["SDL_AUDIODRIVER"] = "directsound"
        os.environ["SDL_AUDIO_DEVICE_NAME"] = str(device_index)

    pygame.mixer.init()

# ---------------------------
# SOUND FUNCTIONS
# ---------------------------
def load_sounds():
    sounds.clear()
    for file in os.listdir(SOUND_FOLDER):
        if file.endswith(".wav") or file.endswith(".mp3"):
            sounds[file] = pygame.mixer.Sound(os.path.join(SOUND_FOLDER, file))

def play_sound(name):
    sound = sounds.get(name)
    if sound:
        channel = sound.play()
        if channel:
            channel.set_volume(volume_slider.get())
            channels.append(channel)

def stop_all_sounds():
    pygame.mixer.stop()
    channels.clear()

# ---------------------------
# UI FUNCTIONS
# ---------------------------
def refresh_buttons():
    for widget in button_frame.winfo_children():
        widget.destroy()

    for i, name in enumerate(sounds):
        btn = tk.Button(
            button_frame,
            text=name,
            width=20,
            height=2,
            bg="#2c2f33",
            fg="white",
            activebackground="#7289da",
            relief="flat",
            command=lambda n=name: play_sound(n)
        )
        btn.grid(row=i//3, column=i%3, padx=10, pady=10)

def add_sound():
    file_path = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.wav *.mp3")]
    )
    if file_path:
        filename = os.path.basename(file_path)
        dest = os.path.join(SOUND_FOLDER, filename)

        with open(file_path, "rb") as src, open(dest, "wb") as dst:
            dst.write(src.read())

        load_sounds()
        refresh_buttons()

def change_device(event):
    selected_index = device_dropdown.current()
    device_id = device_list[selected_index][0]

    try:
        init_audio(device_id)
        load_sounds()
        refresh_buttons()
    except Exception as e:
        messagebox.showerror("Device Error", str(e))

def show_tutorial():
    messagebox.showinfo("Tutorial", """
HOW TO USE:

1. Select your OUTPUT DEVICE at the top
   (Speakers, Headphones, VB Cable, etc.)

2. Add sounds using 'Add Sound'

3. Click buttons to PLAY sounds

4. Click 'STOP ALL' to instantly stop everything

5. Adjust volume with slider

TIPS:
- Use VB-Audio Virtual Cable to play sounds into Discord/mic
- WAV files = faster playback
""")

# ---------------------------
# UI SETUP
# ---------------------------
root = tk.Tk()
root.title("🔥 Pro Soundboard")
root.geometry("650x550")
root.configure(bg="#23272a")

# Title
tk.Label(root, text="Pro Soundboard", font=("Arial", 20, "bold"),
         bg="#23272a", fg="white").pack(pady=10)

# Device selection
device_list = get_output_devices()
device_names = [d[1] for d in device_list]

device_dropdown = ttk.Combobox(root, values=device_names, state="readonly")
device_dropdown.set("Select Output Device")
device_dropdown.pack(pady=5)
device_dropdown.bind("<<ComboboxSelected>>", change_device)

# Controls
control_frame = tk.Frame(root, bg="#23272a")
control_frame.pack(pady=10)

tk.Button(control_frame, text="➕ Add Sound", command=add_sound,
          bg="#7289da", fg="white", width=15).grid(row=0, column=0, padx=5)

tk.Button(control_frame, text="⏹ Stop All", command=stop_all_sounds,
          bg="#f04747", fg="white", width=15).grid(row=0, column=1, padx=5)

tk.Button(control_frame, text="📖 Tutorial", command=show_tutorial,
          bg="#99aab5", fg="black", width=15).grid(row=0, column=2, padx=5)

# Volume
volume_slider = tk.Scale(root, from_=0, to=1, resolution=0.1,
                         orient="horizontal", label="Volume",
                         bg="#23272a", fg="white")
volume_slider.set(0.5)
volume_slider.pack()

# Buttons
button_frame = tk.Frame(root, bg="#23272a")
button_frame.pack(pady=10)

# Init
init_audio()
load_sounds()
refresh_buttons()

root.mainloop()