import keyboard
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
import time
import configparser
import sys, os
import pyautogui
from pathlib import Path

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config/config.ini')
config = configparser.ConfigParser()
config.read(r'.\config\config.ini')
config.sections()


class sakugaGUI(QWidget):

    def __init__(self):
        super().__init__()

        print(config.sections())

        width, height = pyautogui.size()
        dirlbl = QLabel('Save Location')

        changeDir = QPushButton()
        changeDir.clicked.connect(self.selectDirectory)
        changeDir.setIcon(QtGui.QIcon(r'.\AniShots\Anishots\148953.png'))

        savebttn = QPushButton('Save')
        savebttn.clicked.connect(self.saveConfigurations)

        frame1Button = QRadioButton('24 fps')
        frame2Button = QRadioButton('30 fps')
        self.frameGroup = QButtonGroup()
        self.frameGroup.addButton(frame1Button, 1)
        self.frameGroup.addButton(frame2Button, 2)
        self.frameGroup.buttonClicked.connect(self.change_format)

        self.jpegbttn = QRadioButton('JPEG')
        self.pngbttn = QRadioButton('PNG')
        self.bitmapbttn = QRadioButton('BITMAP')
        self.imgTypeGroup = QButtonGroup()
        self.imgTypeGroup.addButton(self.jpegbttn, 10)
        self.imgTypeGroup.addButton(self.bitmapbttn, 11)
        self.imgTypeGroup.addButton(self.pngbttn, 12)
        self.imgTypeGroup.buttonClicked.connect(self.set_framerate)

        self.dirLineEdit = QLineEdit()

        scrnKeyLabel = QLabel('Start/Stop')
        self.hotkeyLineEdit = QLineEdit()
        self.hotkeyLineEdit.setPlaceholderText(config['hotkey']['burst'])
        self.hotkeyLineEdit.setFixedWidth(20)
        self.hotkeyLineEdit.setMaxLength(1)
        regex = QtCore.QRegExp("[a-zA-Z_]+")
        validator = QtGui.QRegExpValidator(regex, self.hotkeyLineEdit)
        self.hotkeyLineEdit.setValidator(validator)
        self.hotkeyLineEdit.textChanged.connect(self.set_key)

        dirlayout = QHBoxLayout()
        dirlayout.addWidget(dirlbl)
        dirlayout.addWidget(self.dirLineEdit)
        dirlayout.addWidget(changeDir)

        hotKeyLayout = QHBoxLayout()
        hotKeyLayout.addWidget(self.hotkeyLineEdit)
        hotKeyLayout.addWidget(scrnKeyLabel)
        hotkeyFrame = QGroupBox('Burst Hotkey')
        hotkeyFrame.setLayout(hotKeyLayout)

        frameLayout = QVBoxLayout()
        frameLayout.addWidget(frame1Button)
        frameLayout.addWidget(frame2Button)
        groupBoxFrames = QGroupBox('Framerate')
        groupBoxFrames.setLayout(frameLayout)

        imageLayout = QVBoxLayout()
        imageLayout.addWidget(self.jpegbttn)
        imageLayout.addWidget(self.pngbttn)
        imageLayout.addWidget(self.bitmapbttn)
        groupBoxImage = QGroupBox('Image Format ')
        groupBoxImage.setLayout(imageLayout)

        burstFrameLayout = QVBoxLayout()
        burstFrameLayout.addWidget(hotkeyFrame)
        burstFrameLayout.addWidget(groupBoxFrames)

        radioLayout = QHBoxLayout()
        radioLayout.addWidget(groupBoxImage)
        radioLayout.addLayout(burstFrameLayout)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(radioLayout)
        mainLayout.addLayout(dirlayout)
        mainLayout.addWidget(savebttn)

        self.setLayout(mainLayout)
        self.setWindowTitle('Configure settings')
        self.setGeometry(width - 300, height - 250, 300, 150)
        self.show()

    def set_key(self):
        config['hotkey']['burst'] = self.hotkeyLineEdit.text()

    def change_format(self, button):
        config['ImageSettings']['type'] = button.text()

    def set_framerate(self):
        config['ImageSettings']['framerate'] = str(self.frameGroup.checkedId())

    def selectDirectory(self):

        """If the user has not selected a file, allow the user to navigate, else if they have entered a directory navigate to that directory"""

        if self.dirLineEdit.text() == '':
            sequence_path = QFileDialog.getExistingDirectory(self, 'Select a location to save the image burst')
            self.dirLineEdit.setText(sequence_path)
            config['paths']['defaultpath'] = self.dirLineEdit.text()
        else:
            try:
                sequence_path = QFileDialog.getExistingDirectory(self, 'Select a location to save the image burst',
                                                                 self.dirLineEdit.text())
                self.dirLineEdit.setText(sequence_path)
                config['paths']['defaultpath'] = self.dirLineEdit.text()
            except FileNotFoundError as exc:
                print(exc)

    def saveConfigurations(self):
        with open(r'.\config\config.ini', 'w') as configfile:
            config.write(configfile)

        sys.exit(qApp.exec_())


class SequenceNaming():

    def __init__(self):
        keyboard.press_and_release('space')
        print('Key s is pressed')
        app = QApplication([])
        self.button1 = QPushButton('save')
        self.linedit1 = QLineEdit()
        self.linedit1.setText('Sequence Name')
        self.window = QWidget()
        self.window.setWindowTitle('Enter name for sequence')
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.linedit1)
        self.layout.addWidget(self.button1)
        self.window.setLayout(self.layout)
        self.window.show()
        self.button1.clicked.connect(self.directory)
        app.exec_()

    def directory(self):
        self.window.close()
        print(self.linedit1.text())
        time.sleep(2)
        keyboard.press_and_release('space')


def stop_button():
    while True:
        if keyboard.is_pressed('s'):
            SequenceNaming()


def create_config_file():
    config['paths'] = {}
    paths = config['paths']
    paths['defaultpath'] = ''

    config['ImageSettings'] = {}
    image_config = config['ImageSettings']
    image_config['framerate'] = ''
    image_config['type'] = ''

    config['hotkey'] = {}
    hotkey = config['hotkey']
    hotkey['burst'] = 'S'

    with open(r'.\AniShots\Anishots\scripts\config\config.ini', 'w') as configfile:
        config.write(configfile)


if __name__ == '__main__':
    qApp = QApplication(sys.argv)
    s =   sakugaGUI()
    sys.exit(qApp.exec_())
    # create_config_file()
