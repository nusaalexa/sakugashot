from mss import mss
import mss.tools
import os, os.path
import errno
import win32api
import time
import tkinter as tk
from tkinter import filedialog
from PIL import Image

class ScreenShotMSS():

    def __init__(self):
        #self.start_pt = beginning
        #self.end_pt = end

        root = tk.Tk()
        root.withdraw()
        self.path = filedialog.askdirectory(title ="Choose output folder")
        self.make_change()

    def screenshot(self, amount, i):
        file = []
        with mss.mss() as sct:
            for _ in range(amount):
                image = 'run%s.png' %i
                file=sct.shot(output =image, mon= 2)
                print(file)
                self.crop_im(image, i)

    def make_dir(self):
        try:
            os.mkdir(self.path)
            print("Successfully created the directory %s" % self.path)

        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(self.path):
                pass
            else:
                print("Creation of the directory %s failed" % self.path)

    def change_dir(self):
        try:
            os.chdir(self.path)
        except OSError as exc:
            raise

    def make_change(self):
        self.make_dir()
        self.change_dir()

    def crop_im(self, image, i):
        im = Image.open(image)
        cropped_image = im.crop((30, 30, 30, 30))

        cropped_image.save('L_2d_cropped%s.png' %i)

    def optimise(self):
        pass

    def setup(self):
        i = 0
        state_left = 1  # left button down
        # frame_ps = float(input("select an interval e.g 0.05 >>\t"))
        # instance creation

        #time.sleep(5)  # temp wait to ensure it doesn't run after the mouse event that clicks compile

        while True:
            a = win32api.GetKeyState(0x01)
            if a != state_left:
                pass
            else:
                i += 1
                self.screenshot(1, i)
                print(i)

            #time.sleep(0.005)

if __name__ == '__main__':
    start = ScreenShotMSS()
    start.setup()


#TODO: SNIP screenshot or area in python
#TODO: Image buffer


