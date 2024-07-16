from math import floor
from tkinter import *
from tkinter.ttk import *
import datetime
from threading import *
import time

with open("customize.txt", "r") as f:
    customization = f.read().splitlines()

APP_FONT = customization[0]
APP_COLOR = customization[1]
TEXT_COLOR = customization[2]

class NoHitApplication:
    def __init__(self):
        self.started = False
        self.root = Tk()
        self.root.title("No-Hit Timer")
        self.root.geometry("240x160")
        self.root.config(background=APP_COLOR)
        self.root.protocol('WM_DELETE_WINDOW', self.close_app)
        self.hits_count = StringVar()
        self.hits_count.set("Hits:  0")
        hit_counter = Label(self.root, textvariable=self.hits_count, font=(APP_FONT, 24), background=APP_COLOR, foreground=TEXT_COLOR)
        hit_counter.pack(padx=20, pady=0)
        hit_counter.bind("<Button>", lambda e: self.incrementCounter(e.num))
        self.timer_text = StringVar()
        self.timer_text.set("0:00:00")
        timer = Label(self.root, textvariable=self.timer_text, font=(APP_FONT, 24), background=APP_COLOR, foreground=TEXT_COLOR)
        timer.pack(padx=20, pady=20)
        self.start_button = Button(self.root, text="Start", command=self.startButtonClicked)
        self.start_button.pack(side="bottom")
        self.root.mainloop()

    def startButtonClicked(self):
        self.started = not self.started
        if self.started:
            self.start_button.config(text="Stop")
            self.hits_count.set("Hits:  0")
            self.start_time = datetime.datetime.now()
            t1 = Thread(target=self.runTimer)
            t1.start()
        else:
            self.start_button.config(text="Start")

    def runTimer(self):
        while self.started:
            current_time = datetime.datetime.now()
            diff = current_time - self.start_time
            convert = datetime.timedelta(seconds=floor(diff.total_seconds()))
            self.timer_text.set(f"{convert}")

    def incrementCounter(self, mouse_num):
        if not self.started or mouse_num == 2: # middle mouse
            return
        num_hits = int(self.hits_count.get().split(":  ")[1])
        if mouse_num == 1: # left click increments hit counter
            num_hits += 1
        elif mouse_num == 3 and num_hits > 0: # right click decrements hit counter
            num_hits -= 1
        self.hits_count.set(f"Hits:  {num_hits}")

    def close_app(self):
        self.started = False # stop the thread from running
        time.sleep(0.75) # give enough time for the thread to finish the job
        self.root.destroy()

app = NoHitApplication()