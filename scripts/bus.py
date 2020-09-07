import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
from PyQt5 import uic, QtCore

# Load ui files
uiBus = r'ui/bus.ui'
formBus, baseBus = uic.loadUiType(uiBus)


class Bus(baseBus, formBus):
    def __init__(self):
        super(baseBus, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    bus = Bus()
    bus.show()
    sys.exit(app.exec_())
