import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
from PyQt5 import uic, QtCore

# Load ui files
uiMachine = r'ui\machine.ui'
formMachine, baseMachine = uic.loadUiType(uiMachine)


class Machine(baseMachine, formMachine):
    def __init__(self):
        super(baseMachine, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    machine = Machine()
    machine.show()
    sys.exit(app.exec_())
