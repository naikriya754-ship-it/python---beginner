# ============================================================
# 🎉 CLAP TO OPEN - Python Project
# ============================================================
# This program listens to your microphone and detects claps.
# When it hears a certain number of claps, it opens a website
# or application of your choice!
# ============================================================

# --- STEP 1: IMPORT LIBRARIES ---
# Libraries are pre-built toolboxes that give us extra powers.
# We don't write these from scratch — Python lets us reuse them.

import pyaudio        # pyaudio  → lets Python talk to your microphone
import numpy as np    # numpy   → helps us do math on audio data (arrays of numbers)
import time           # time    → lets us track time (e.g., pause between claps)
import webbrowser     # webbrowser → lets Python open websites in your browser
import os             # os      → lets Python interact with your operating system (open apps)


# --- STEP 2: CONFIGURATION SETTINGS ---
# Think of these as the "settings panel" of our program.
# You can tweak these values to make detection more accurate.

CHUNK = 1024
# CHUNK = how many audio "samples" we read at one time from the mic.
# 1024 samples at a time is a good balance — not too fast, not too slow.
# Think of it like reading a book 1024 letters at a time.

FORMAT = pyaudio.paInt16
# FORMAT = the format (data type) of each audio sample.
# paInt16 means each sample is a 16-bit integer (a number from -32768 to 32767).
# Higher number = louder sound. This is the standard format for audio.

CHANNELS = 1
# CHANNELS = mono (1) or stereo (2).
# Mono = one microphone input. We only need 1 channel to detect claps.

RATE = 44100
# RATE = how many samples are recorded per second (sample rate).
# 44100 Hz is CD quality — captures sounds humans can hear (up to ~20,000 Hz).

CLAP_THRESHOLD = 3000
# CLAP_THRESHOLD = the minimum "loudness" value to be considered a clap.
# Audio values range from 0 (silent) to 32767 (very loud).
# 3000 means we only react to sounds louder than 3000 — ignores background noise.
# ⚙️ Increase this (e.g. 5000) in a noisy room.
# ⚙️ Decrease this (e.g. 1500) in a quiet room.

CLAP_COOLDOWN = 0.3
# CLAP_COOLDOWN = minimum time (in seconds) between two claps.
# This prevents one clap from being detected as multiple claps.
# 0.3 seconds = 300 milliseconds gap required between claps.

DOUBLE_CLAP_WINDOW = 1.5
# DOUBLE_CLAP_WINDOW = max time allowed between first and second clap.
# If clap 2 doesn't come within 1.5 seconds, we reset and wait again.

TARGET_CLAP_COUNT = 2
# TARGET_CLAP_COUNT = how many claps trigger the action.
# Currently set to 2 (double clap). Change to 3 for triple clap!

ACTION_URL = "https://www.google.com"
# ACTION_URL = the website that opens when the claps are detected.
# You can change this to any URL like "https://youtube.com"


# --- STEP 3: THE CLAP DETECTOR CLASS ---
# A "class" is like a blueprint for an object.
# Here, ClapDetector is our "clap-listening machine" blueprint.
# It has: settings (attributes) + abilities (methods/functions).

class ClapDetector:

    def __init__(self):
        # __init__ = the "constructor" — runs automatically when we create the object.
        # It sets up everything the object needs to work.

        self.audio = pyaudio.PyAudio()
        # pyaudio.PyAudio() → starts the PyAudio engine.
        # self.audio is our connection to the computer's audio system.
        # "self" means this variable belongs to THIS object (not a global variable).

        self.stream = None
        # self.stream = the actual microphone input stream (like a live pipe of audio data).
        # We set it to None for now — we'll open it in the start() method.

        self.clap_times = []
        # self.clap_times = a list that stores the TIME of each detected clap.
        # Example: [1.23, 1.87] means clap 1 at 1.23 seconds, clap 2 at 1.87 seconds.

        self.running = False
        # self.running = a True/False flag.
        # True = the detector is actively listening.
        # False = the detector has stopped.

        print("🎤 Clap Detector initialized!")
        print(f"   Threshold: {CLAP_THRESHOLD} | Claps needed: {TARGET_CLAP_COUNT}")
        # f"..." is an f-string — it lets us insert variable values directly into text.
        # {CLAP_THRESHOLD} gets replaced with the actual value (e.g., 3000).


    def start_stream(self):
        # This method opens the microphone stream so we can start reading audio.
        # A "stream" is like turning on the tap — audio flows continuously.

        self.stream = self.audio.open(
            format=FORMAT,       # audio format (16-bit integers)
            channels=CHANNELS,   # mono audio (1 channel)
            rate=RATE,           # 44100 samples per second
            input=True,          # input=True means we're RECORDING (not playing)
            frames_per_buffer=CHUNK  # read 1024 samples at a time
        )
        # self.audio.open(...) opens a connection to your microphone with these settings.
        # The result is stored in self.stream — our live audio pipe.

        print("🎙️  Microphone stream opened. Listening...")


    def get_audio_volume(self):
        # This method reads a chunk of audio from the mic and calculates its volume.
        # Volume here = how loud the sound is, expressed as a single number.

        data = self.stream.read(CHUNK, exception_on_overflow=False)
        # self.stream.read(CHUNK) → reads CHUNK (1024) samples from the microphone.
        # exception_on_overflow=False → don't crash if the buffer overflows (data comes too fast).
        # "data" is raw bytes — like a chunk of binary code we need to decode.

        audio_data = np.frombuffer(data, dtype=np.int16)
        # np.frombuffer(...) → converts raw bytes into a numpy array of integers.
        # dtype=np.int16 → each number is a 16-bit integer (matches our FORMAT setting).
        # Now audio_data looks like: [-120, 340, -890, 3200, ...] — 1024 numbers.

        volume = np.max(np.abs(audio_data))
        # np.abs(audio_data) → converts all negative numbers to positive.
        #   Why? Sound waves go + and -, but loudness is always positive.
        #   Example: [-3200, 3200] → [3200, 3200]
        # np.max(...) → finds the maximum (peak) value in the array.
        #   This is the LOUDEST moment in this 1024-sample chunk.
        # So "volume" = the peak loudness of this moment. One number!

        return volume
        # Send this volume number back to whoever called this method.


    def is_clap(self, volume):
        # This method decides: is this loud sound a clap or just noise?
        # It returns True (yes, it's a clap) or False (no, ignore it).

        return volume > CLAP_THRESHOLD
        # Simple check: if volume is greater than our threshold, it's a clap.
        # Example: volume=5000, CLAP_THRESHOLD=3000 → 5000 > 3000 → True (clap!)
        # Example: volume=800,  CLAP_THRESHOLD=3000 → 800  > 3000 → False (not a clap)


    def process_clap(self):
        # This method is called every time a clap is detected.
        # It tracks clap timing and decides if the pattern (e.g., double clap) is complete.

        current_time = time.time()
        # time.time() → returns the current time as a decimal number (Unix timestamp).
        # Example: 1713800000.45 (seconds since Jan 1, 1970)
        # We use this to measure how much time has passed between claps.

        # --- Check cooldown to avoid duplicate detection ---
        if self.clap_times and (current_time - self.clap_times[-1]) < CLAP_COOLDOWN:
            return
        # self.clap_times[-1] → the time of the LAST recorded clap (-1 = last item in list).
        # current_time - self.clap_times[-1] = how many seconds since the last clap.
        # If it's less than CLAP_COOLDOWN (0.3s), we ignore this — it's the same clap echoing.
        # "return" exits the method early without doing anything.

        # --- Check if too much time has passed (reset window) ---
        if self.clap_times and (current_time - self.clap_times[0]) > DOUBLE_CLAP_WINDOW:
            print("⏱️  Clap window expired. Resetting...")
            self.clap_times = []
        # self.clap_times[0] → time of the FIRST clap in this sequence.
        # If more than DOUBLE_CLAP_WINDOW (1.5s) has passed since the first clap, reset.
        # self.clap_times = [] → clears the list, starting fresh.

        # --- Record this clap ---
        self.clap_times.append(current_time)
        # .append() adds the current time to the end of our clap_times list.
        # After 1st clap: [1713800001.2]
        # After 2nd clap: [1713800001.2, 1713800001.9]

        print(f"👏 Clap detected! ({len(self.clap_times)}/{TARGET_CLAP_COUNT})")
        # len(self.clap_times) = how many claps we've recorded so far.
        # This prints something like: "👏 Clap detected! (1/2)"

        # --- Check if we've reached the target clap count ---
        if len(self.clap_times) >= TARGET_CLAP_COUNT:
            self.trigger_action()
            # If we've collected enough claps, fire the action!
            self.clap_times = []
            # Reset the list so we can detect the next clap sequence.


    def trigger_action(self):
        # This method runs when the full clap pattern is detected.
        # It opens the website defined in ACTION_URL.

        print(f"\n🚀 Double clap detected! Opening: {ACTION_URL}\n")

        webbrowser.open(ACTION_URL)
        # webbrowser.open() → opens the URL in your default web browser.
        # It's that simple! Python's built-in webbrowser module handles it.

        # --- Optional: Open a local app instead of a website ---
        # Uncomment ONE of these lines to open an app instead:
        # os.system("calc")          # Windows Calculator
        # os.system("notepad")       # Windows Notepad
        # os.system("open -a Safari") # Mac Safari
        # os.startfile("C:/path/to/your/app.exe")  # Any Windows app


    def listen(self):
        # This is the MAIN LOOP — the heart of the program.
        # It continuously reads audio and checks for claps until stopped.

        self.start_stream()
        # Opens the microphone stream (defined above).

        self.running = True
        # Set running flag to True — the loop will keep going while this is True.

        print(f"\n✅ Listening for {TARGET_CLAP_COUNT} claps...")
        print("   Press Ctrl+C to stop.\n")

        try:
            # try/except = error handling. "try" runs the code, "except" catches errors.
            # This lets us stop gracefully with Ctrl+C instead of crashing.

            while self.running:
                # "while self.running" = keep looping as long as running is True.
                # This is an infinite loop — it only stops when self.running = False
                # or when the user presses Ctrl+C.

                volume = self.get_audio_volume()
                # Read a chunk of audio and get its peak volume (a single number).

                if self.is_clap(volume):
                    # If the volume is above our threshold, it might be a clap!
                    self.process_clap()
                    # Send it to process_clap() to record and check the pattern.

        except KeyboardInterrupt:
            # KeyboardInterrupt = what happens when user presses Ctrl+C.
            # Instead of crashing, we catch it here and stop cleanly.
            print("\n🛑 Stopped by user.")

        finally:
            # "finally" block ALWAYS runs — whether there was an error or not.
            # This is where we clean up and release resources.
            self.stop()


    def stop(self):
        # This method cleanly shuts down the microphone and audio engine.

        self.running = False
        # Set the flag to False — tells the while loop to stop (just in case).

        if self.stream:
            # Check if the stream exists (was it opened?).
            self.stream.stop_stream()
            # Stops the audio stream — like turning off the tap.
            self.stream.close()
            # Closes and releases the microphone resource.

        self.audio.terminate()
        # Shuts down the PyAudio engine completely.
        # Always do this! Not terminating can cause issues on next run.

        print("🎤 Microphone released. Goodbye!")


# --- STEP 4: RUN THE PROGRAM ---
# This is the entry point of the script.

if __name__ == "__main__":
    # if __name__ == "__main__" → this checks: "Is this script being run directly?"
    # If someone imports this file as a module, this block WON'T run.
    # If you run it directly (python clap_to_open.py), this WILL run.

    print("=" * 50)
    print("   👏 CLAP TO OPEN - Python Project")
    print("=" * 50)

    detector = ClapDetector()
    # Creates a new ClapDetector object using our class blueprint.
    # This calls __init__() automatically.

    detector.listen()
    # Starts the main listening loop.
    # The program will now listen for claps until you press Ctrl+C. 