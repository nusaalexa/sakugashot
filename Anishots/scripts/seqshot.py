import sys
from mss import mss
import mss.tools
from PyQt5 import QtWidgets, QtCore, QtGui
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os
import errno
import time
import win32api
import cv2
import matplotlib.pyplot as plt


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.sequence = []

        root = tk.Tk()
        root.withdraw()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)
        self.path = filedialog.askdirectory(title="Choose output folder")
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        print('Capture the screen...')
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def image_to_array(self,_image):
        _image = cv2.imread(_image, flags=cv2.IMREAD_COLOR)
        self.sequence.append(_image)

    def array_to_image(self, array):
        for i, imgarr in enumerate(array):
            plt.imsave(os, path.join(path, '{0}_{1}.png'.format(name, i)), imgarr)


    def screenshot(self, amount, i):
        file = []
        with mss.mss() as sct:
            for _ in range(amount):
                image = 'run%s.png' %i
                file =sct.shot(output =image, mon= 1)
                self.image_to_array(file)

    def __setup(self):
        i = 0
        state_left = 1  # left button down
        time.sleep(3)  # temp wait to ensure it doesn't run after the mouse event that clicks compile

        while True:
            a = win32api.GetKeyState(0x01)
            if a != state_left:
                self.screenshot(1, i)
            else:
                print('HERE')
                i += 1
                self.screenshot(1, i)
        time.sleep(0.005)

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

    def crop_im(self, image, crop_v):
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        im = Image.open(image)
        cropped_image = im.crop((x1, y1, x2, y2))

        cropped_image.save('cropped%s.png' %crop_v)

    def mouseReleaseEvent(self, event):
        self.close()
        self.make_change()
        self.__setup()
        self.crop_im()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())