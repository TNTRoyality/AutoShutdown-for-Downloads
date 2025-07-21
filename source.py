import os
import time
import threading
import subprocess
import tkinter as tk

FOLDER = r"C:\Program Files (x86)\Steam\steamapps\downloading"
shutdown_cancelled = False

def is_folder_empty(path):
    return len(os.listdir(path)) == 0

def countdown_and_shutdown():
    global shutdown_cancelled
    for i in range(10, 0, -1):
        if shutdown_cancelled:
            message.set("Shutdown cancelled.")
            cancel_button.pack_forget()
            return
        message.set(f"The folder is empty.\nThe PC will shut down in {i} seconds.")
        root.update()
        time.sleep(1)
    subprocess.run("shutdown /s /t 0", shell=True)

def monitor():
    global shutdown_cancelled
    while True:
        if is_folder_empty(FOLDER):
            message.set("The download has finished.\nThe PC will shut down in 10 seconds.")
            cancel_button.pack(pady=10)
            shutdown_cancelled = False
            countdown_and_shutdown()
            break
        else:
            message.set("Waiting for download to finish...")
            cancel_button.pack_forget()
        root.update()
        time.sleep(4)

def cancel_shutdown():
    global shutdown_cancelled
    shutdown_cancelled = True

root = tk.Tk()
root.title("Download Monitor")
root.geometry("450x200")
root.resizable(False, False)
root.configure(bg="#282c34")

font_style = ("Segoe UI", 14)
text_color = "#ffffff"
button_color = "#ff4c4c"

message = tk.StringVar()
message.set("Starting...")

label = tk.Label(
    root,
    textvariable=message,
    font=font_style,
    fg=text_color,
    bg="#282c34",
    wraplength=420,
    justify="center"
)
label.pack(expand=True, padx=10)

cancel_button = tk.Button(
    root,
    text="Cancel Shutdown",
    font=("Segoe UI", 12),
    bg=button_color,
    fg="white",
    activebackground="#cc0000",
    command=cancel_shutdown
)

thread = threading.Thread(target=monitor)
thread.daemon = True
thread.start()

root.mainloop()