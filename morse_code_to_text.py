from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QGridLayout
import sys
from morse_converter import MorseConverter as mc


class MouseClicksMorse(QWidget):

    def __init__(self):
        super().__init__()
        self.inputArea = InputArea()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Mouse Clicks - Morse Code Conversion')

        self.inputArea.update_labels.connect(self.updateLabels)
        self.inputArea.clear_labels.connect(self.clearLabels)

        inst = QLabel()
        inst.setText('Instructions:\n Dot (.)\t:  Left Click\n Dash (-)\t:  Double Left Click\n Next Letter\t:  Right Click\n Next Word\t:  Double Right Click')
        font = QtGui.QFont("MoolBoran", 16)
        font.setStyleHint(QtGui.QFont.TypeWriter)
        inst.setFont(font)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(inst, 1, 3)
        grid.addWidget(self.inputArea, 1, 0, 8, 1)
        grid.addWidget(self.inputArea.photo, 2, 3)
        grid.addWidget(self.inputArea.outputMorse, 4, 3, 2, 1)
        grid.addWidget(self.inputArea.outputConverted, 6, 3, 2, 1)
        grid.addWidget(self.inputArea.clearButton, 8, 3)
        self.setLayout(grid)

        self.setWindowTitle('Mouse Clicks - Morse Code Conversion')

        self.show()

    def updateLabels(self):
        self.inputArea.outputMorse.setText('Morse Code: <b>' + self.inputArea.message.replace('*', ' ').replace('.', '·'))
        if self.inputArea.message[-1] == '*':
            self.inputArea.outputConverted.setText('Conv. Text: <b>' + mc._morseToText(self.inputArea.message))

    def clearLabels(self):
        self.inputArea.outputMorse.setText('Morse Code: ')
        self.inputArea.outputConverted.setText('Conv. Text: ')
        self.inputArea.message = ''


class InputArea(QWidget):

    update_labels = pyqtSignal()
    clear_labels = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.setInterval(250)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timeout)
        self.click_count = 0
        self.message = ''
        self.temp = ''

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)
        self.setPalette(p)
        self.setAutoFillBackground(True)
        image_path="morse_img.jpg"
        pixmap=QtGui.QPixmap(image_path)
        resized_width = 620
        resized_height = 1000
        pixmap = pixmap.scaled(resized_width, resized_height, Qt.KeepAspectRatio)
        self.photo=QLabel()
        self.photo.setPixmap(pixmap)
        self.photo.setScaledContents(True)

        self.outputMorse = QLabel()
        self.outputMorse.setText('Morse Code: ')
        self.outputConverted = QLabel()
        self.outputConverted.setText('Conv. Text: ')
        font = QtGui.QFont("Consolas", 12)
        font.setStyleHint(QtGui.QFont.TypeWriter)
        self.outputMorse.setFont(font)
        self.outputConverted.setFont(font)

        self.clearButton = QPushButton('Clear All')
        self.clearButton.clicked.connect(self.sendClearSignal)

    def mousePressEvent(self, event):
        self.click_count += 1
        if event.button() == Qt.LeftButton:
            self.temp = '.'
        if event.button() == Qt.RightButton:
            self.temp = '*'
        if not self.timer.isActive():
            self.timer.start()

    def timeout(self):
        if self.click_count > 1:
            if self.temp == '*':
                self.message += '**'
            else:
                self.message += '-'
        else:
            self.message += self.temp
        self.click_count = 0
        self.update_labels.emit()

    def sendClearSignal(self):
        self.clear_labels.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MouseClicksMorse()
    sys.exit(app.exec_())
