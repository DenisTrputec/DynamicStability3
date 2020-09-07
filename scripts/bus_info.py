import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
from PyQt5 import uic, QtCore

# Load ui files
uiBus = r'ui\bus_info.ui'
formBus, baseBus = uic.loadUiType(uiBus)


class BusInfo(baseBus, formBus):
    def __init__(self):
        super(baseBus, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    bus = BusInfo()
    bus.show()
    sys.exit(app.exec_())
