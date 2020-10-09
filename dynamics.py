import sys
import psse
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
from PyQt5 import uic, QtCore
from configparser import ConfigParser
from PIL import Image
from scripts.bus import Bus
from scripts.branch import Branch
from scripts.machine import Machine
from scripts.bus_info import BusInfo

# Load config file
config_file_path = "config.ini"
config = ConfigParser()
config.read(config_file_path)

# Load ui files
uiMainMenu = r'ui\main_menu.ui'
formMainMenu, baseMainMenu = uic.loadUiType(uiMainMenu)
uiImport = r'ui\import.ui'
formImport, baseImport = uic.loadUiType(uiImport)


def saveDefaultPaths(rawPath, dyrPath):
    config.set("path", "raw", rawPath)
    config.set("path", "dyr", dyrPath)
    with open(config_file_path, 'w') as handle:
        config.write(handle)


class MainMenu(baseMainMenu, formMainMenu):
    def __init__(self):
        super(baseMainMenu, self).__init__()

        self.setupUi(self)
        self.child_window = {"import": None, "bus": None, "branch": None, "machine": None}
        self.info_window = {"bus_info": None}
        self.image = Image.open("pics/croatian_ees_grid.jpg")
        self.raw_file = (config["path"]["raw"].split('/'))[-1]
        self.dyr_file = (config["path"]["dyr"].split('/'))[-1]

        psse.initialize()
        psse.read_files(config["path"]["raw"], config["path"]["dyr"])

        self.btn_Bus.clicked.connect(lambda: self.newWindow(Bus, "bus"))
        self.btn_Branch.clicked.connect(lambda: self.newWindow(Branch, "branch"))
        self.btn_Machine.clicked.connect(lambda: self.newWindow(Machine, "machine"))
        self.btn_Options.clicked.connect(lambda: self.newWindow(Import, "import"))

    def newWindow(self, cls, key):
        self.child_window[key] = cls()
        self.child_window[key].show()
        if key != "import":
            self.child_window[key].action_Bus.triggered.connect(lambda: self.openInfo(BusInfo, "bus_info"))
            self.child_window[key].action_ShowGrid.triggered.connect(lambda: self.image.show())
            # self.child_window[key].btn_Initialize.clicked.connect(self.child_window[key].initialize)
            self.refreshText(key)

    def openInfo(self, cls, key):
        self.info_window[key] = cls()
        self.info_window[key].show()

    def refreshText(self, key):
        self.child_window[key].lbl_Imported.setText("Imported files:\n" + self.raw_file + "\n" + self.dyr_file)

    def closeEvent(self, event):
        self.child_window = None
        self.info_window = None
        self.image = None
        event.accept()


class Import(baseImport, formImport):
    def __init__(self):
        super(baseImport, self).__init__()
        self.setupUi(self)
        self.line_PowerFlowData.setText(config["path"]["raw"])
        self.line_DynamicsData.setText(config["path"]["dyr"])

        self.btn_BrowsePfData.clicked.connect(self.browse)
        self.btn_BrowseDynData.clicked.connect(self.browse)
        self.accepted.connect(lambda: saveDefaultPaths(self.line_PowerFlowData.text(), self.line_DynamicsData.text()))

    def browse(self):
        sender = self.sender()
        if sender.objectName() == 'btn_BrowsePfData':
            file_path = QFileDialog.getOpenFileName(self, caption='Browse Power Flow Data File', directory='',
                                                    filter='*.raw; *.rawx; *.sav')
            self.line_PowerFlowData.setText(file_path[0])
        else:
            file_path = QFileDialog.getOpenFileName(self, caption='Browse Dynamics Data File', directory='',
                                                    filter='*.dyr')
            self.line_DynamicsData.setText(file_path[0])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec_())
