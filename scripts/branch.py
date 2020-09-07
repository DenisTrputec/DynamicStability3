import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
from PyQt5 import uic, QtCore

# Load ui files
uiBranch = r'ui\branch.ui'
formBranch, baseBranch = uic.loadUiType(uiBranch)


class Branch(baseBranch, formBranch):
    def __init__(self):
        super(baseBranch, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    branch = Branch()
    branch.show()
    sys.exit(app.exec_())
