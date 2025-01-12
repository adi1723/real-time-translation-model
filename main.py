import os
import threading
import tkinter as tk
from tkinter import ttk
from gtts import gTTS
import speech_recognition as sr
from playsound import playsound
from deep_translator import GoogleTranslator
import webbrowser

# Function to open a webpage
def open_webpage(url):
    webbrowser.open(url)

# Create the main window
win = tk.Tk()
win.geometry("900x600")
win.title("Real-Time Voice Translator")

# Set the icon
icon = tk.PhotoImage(file="icon.png")  # Ensure 'icon.png' exists in the working directory
win.iconphoto(False, icon)

# Set background color
win.configure(bg="#f0f8ff")

# Add a title label
title_label = tk.Label(win, text="Real-Time Voice Translator", font=("Helvetica", 20, "bold"), fg="#333", bg="#f0f8ff")
title_label.pack(pady=10)

# Create labels and text boxes for input and output
input_label = tk.Label(win, text="Recognized Text", font=("Helvetica", 14), fg="#555", bg="#f0f8ff")
input_label.pack(pady=5)
input_text = tk.Text(win, height=5, width=60, font=("Helvetica", 12))
input_text.pack(pady=5)

output_label = tk.Label(win, text="Translated Text", font=("Helvetica", 14), fg="#555", bg="#f0f8ff")
output_label.pack(pady=5)
output_text = tk.Text(win, height=5, width=60, font=("Helvetica", 12))
output_text.pack(pady=5)

# Language codes and names
language_codes = {
    "English": "en",
    "Hindi": "hi"
}
language_names = list(language_codes.keys())

# Dropdown for input language
input_lang_label = tk.Label(win, text="Select Input Language:", font=("Helvetica", 12), fg="#555", bg="#f0f8ff")
input_lang_label.pack()
input_lang = ttk.Combobox(win, values=language_names, state="readonly", font=("Helvetica", 12))
input_lang.set("English")
input_lang.pack(pady=5)

# Dropdown for output language
output_lang_label = tk.Label(win, text="Select Output Language:", font=("Helvetica", 12), fg="#555", bg="#f0f8ff")
output_lang_label.pack()
output_lang = ttk.Combobox(win, values=language_names, state="readonly", font=("Helvetica", 12))
output_lang.set("Hindi")
output_lang.pack(pady=5)

# Variables for execution state
keep_running = False

# Function to update translation
def update_translation():
    global keep_running
    if keep_running:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                # Clear previous text
                input_text.delete(1.0, tk.END)
                output_text.delete(1.0, tk.END)
                input_label.config(text="Listening...")

                # Recognize speech
                audio = recognizer.listen(source)
                speech = recognizer.recognize_google(audio)
                input_text.insert(tk.END, speech)

                # Translate speech
                translated = GoogleTranslator(
                    source=language_codes[input_lang.get()],
                    target=language_codes[output_lang.get()]
                ).translate(speech)
                output_text.insert(tk.END, translated)

                # Convert translation to speech
                tts = gTTS(text=translated, lang=language_codes[output_lang.get()])
                temp_audio_file = "output.mp3"
                tts.save(temp_audio_file)

                # Play the audio
                playsound(temp_audio_file)

                # Cleanup audio file
                os.remove(temp_audio_file)
            except Exception as e:
                output_text.insert(tk.END, f"Error: {e}")

        # Call the function again after a delay
        win.after(1000, update_translation)

# Function to start translation
def start_translation():
    global keep_running
    if not keep_running:
        keep_running = True
        threading.Thread(target=update_translation).start()

# Function to stop execution
def stop_execution():
    global keep_running
    keep_running = False
    input_label.config(text="Recognized Text")

# Function to open about page
def open_about():
    about_win = tk.Toplevel(win)
    about_win.title("About")
    about_win.geometry("400x300")
    about_win.configure(bg="#f0f8ff")

    about_label = tk.Label(about_win, text="About", font=("Helvetica", 16, "bold"), fg="#333", bg="#f0f8ff")
    about_label.pack(pady=10)

    about_text = tk.Text(about_win, height=10, width=40, font=("Helvetica", 12))
    about_text.insert(tk.END, """
This is a real-time voice translator.
Developed by: Aditya Kapadane
""")
    about_text.config(state=tk.DISABLED)
    about_text.pack(pady=5)

    close_btn = tk.Button(about_win, text="Close", command=about_win.destroy, bg="#555", fg="#fff", font=("Helvetica", 12))
    close_btn.pack(pady=10)

# Add control buttons
start_button = tk.Button(win, text="Start Translation", command=start_translation, bg="#4caf50", fg="#fff", font=("Helvetica", 14))
start_button.pack(pady=10)

stop_button = tk.Button(win, text="Stop Translation", command=stop_execution, bg="#f44336", fg="#fff", font=("Helvetica", 14))
stop_button.pack(pady=10)

about_button = tk.Button(win, text="About", command=open_about, bg="#2196f3", fg="#fff", font=("Helvetica", 14))
about_button.pack(pady=10)

# Run the GUI
def animate_title():
    colors = ["#4caf50", "#f44336", "#2196f3", "#ff9800"]
    for i in range(len(colors)):
        title_label.config(fg=colors[i])
        win.update_idletasks()
        win.after(500)
    win.after(2000, animate_title)

animate_title()
win.mainloop()