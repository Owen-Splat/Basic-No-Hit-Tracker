from math import floor
from tkinter import *
from tkinter.ttk import *
import datetime
from threading import *

with open("customize.txt", "r") as f:
    customization = f.read().splitlines()

APP_FONT = customization[0]
APP_COLOR = customization[1]
TEXT_COLOR = customization[2]


class NoHitApplication:
    def __init__(self):
        self.started = False
        self.timer_thread = None
        self.stop = Event()

        # create the root application window and connect the close button to a function that'll close the timer thread
        self.root = Tk()
        self.root.title("No-Hit Timer")
        self.root.geometry("240x160")
        self.root.resizable(False, False)
        self.root.config(background=APP_COLOR)
        self.root.protocol('WM_DELETE_WINDOW', self.close_app)

        # create a hit counter label and connect mouse clicks to a function to update the counter
        self.hits_count = StringVar()
        self.hits_count.set("Hits:  0")
        hit_counter = Label(self.root, textvariable=self.hits_count, font=(APP_FONT, 24), background=APP_COLOR, foreground=TEXT_COLOR)
        hit_counter.pack(padx=20, pady=0)
        hit_counter.bind("<Button>", lambda e: self.updateCounter(e.num))

        # create the timer text
        self.timer_text = StringVar()
        self.timer_text.set("0:00:00")
        timer = Label(self.root, textvariable=self.timer_text, font=(APP_FONT, 24), background=APP_COLOR, foreground=TEXT_COLOR)
        timer.pack(padx=20, pady=20)

        # create the start button and connect it to a function for when it is pressed
        self.start_button = Button(self.root, text="Start", command=self.startButtonClicked)
        self.start_button.pack(side="bottom")

        # run the root application window
        self.root.mainloop()


    def startButtonClicked(self):
        """Flips a boolean value for if the timer is running or not
        
        If the timer should be running, change the button text to 'Stop', reset the Hit counter and start the timer thread"""

        self.started = not self.started
        if self.started:
            self.start_button.config(text="Stop")
            self.hits_count.set("Hits:  0")
            self.start_time = datetime.datetime.now()
            self.timer_thread = Thread(target=self.runTimer)
            self.timer_thread.start()
        else:
            self.start_button.config(text="Start")
            self.timer_thread = None


    def runTimer(self):
        """Continuously compares the start datetime to the current datetime, and converts to hours:minutes:seconds"""

        while self.started and not self.stop.isSet():
            current_time = datetime.datetime.now()
            diff = current_time - self.start_time
            convert = datetime.timedelta(seconds=floor(diff.total_seconds()))
            self.timer_text.set(f"{convert}")


    def updateCounter(self, mouse_num):
        """Updates the hit counter on mouse button click

        Left-click increments, right-click decrements. Middle click is ignored"""

        if not self.started or mouse_num == 2:
            return

        num_hits = int(self.hits_count.get().split(":  ")[1])

        if mouse_num == 1:
            num_hits += 1
        elif mouse_num == 3 and num_hits > 0:
            num_hits -= 1
        
        self.hits_count.set(f"Hits:  {num_hits}")


    def close_app(self):
        """Tell the timer thread that it should close before closing the root application window"""

        self.stop.set()
        if self.timer_thread is not None:
            self.timer_thread.join(timeout=3)
        self.root.destroy()

# initialize the class containing the root application window
app = NoHitApplication()