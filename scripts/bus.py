import sys
import psse
import element_info
from scripts import error_log as err
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
from PyQt5 import uic, QtCore

# Load ui files
uiBus = r'ui/bus.ui'
formBus, baseBus = uic.loadUiType(uiBus)


class Bus(baseBus, formBus):
    def __init__(self):
        super(baseBus, self).__init__()
        self.setupUi(self)
        self.out_file = ""
        self.bus_number = None
        self.channel_count = 0
        self.options = [False, False, False]
        self.time = 0
        self.lbl_Status.setText("")

        # Create list of elements for combobox
        user_options = [True, False, False, False, False, False, False, True, False]
        user_filter = [""] * 9
        _, bus_names_list = element_info.bus_info(user_options, user_filter)
        # self.bus_names = [(str(element[0]) + " " + element[1]).decode('latin1') for element in bus_names_list]
        self.bus_names = [(str(element[0]) + " " + element[1]) for element in bus_names_list]
        self.cmbox_BusNumber.addItem("")
        self.cmbox_BusNumber.addItems(self.bus_names)

        # Events
        self.btn_Initialize.clicked.connect(self.initialize)
        self.btn_Run.clicked.connect(self.run)

    def initialize(self):
        # Initialite PSSE
        err_msg = psse.initialize()
        if err_msg is not None:
            self.change_status_label(err_msg, False)
            return

        # Check bus number
        self.bus_number = psse.check_bus_number(self.cmbox_BusNumber.currentText())
        if self.bus_number == -1:
            self.change_status_label("Invalid bus number!", False)
            return

        # Check output channels
        self.options = [self.chkbox_Frequency.isChecked(), self.chkbox_Voltage.isChecked(),
                        self.chkbox_VoltageAngle.isChecked()]

        if any(self.options) is False:
            self.change_status_label("Check at least one output channel!", False)
            return

        # Check output file
        self.out_file = psse.check_out_file(self.line_FileName.text())
        self.line_FileName.setText(self.out_file.split('\\')[-1])

        # Add output channels
        self.channel_count = psse.add_bus_channels(self.out_file, self.bus_number, self.options)
        if type(self.channel_count) is str:
            self.change_status_label(self.channel_count, False)
            return 

        # Finish initializing
        self.btn_Run.setEnabled(True)
        self.btn_Lf_AddDisturbance.setEnabled(False)
        self.btn_Bf_AddDisturbance.setEnabled(False)
        self.btn_PlotGraph.setEnabled(False)
        self.change_status_label("Initialized", True)
        return

    def run(self):
        # Run dynamics
        try:
            new_time = float(self.line_PauseTime.text())
        except ValueError:
            self.change_status_label("Time of pause must be float value!", False)
            return
        if new_time > self.time:
            ierr = psse.run(new_time)
            print(ierr)
            if ierr == 0:
                self.time = new_time
                self.change_status_label("Run executed", True)
                self.lbl_RunTime.setText(f"Run time: {self.time:.2f} s")
            else:
                self.change_status_label(err.run(ierr), False)
        else:
            print("New time of pause must be greater than current time!")
            self.change_status_label("New time of pause must be greater than current time!", False)

    def change_status_label(self, messeage, status):
        self.lbl_Status.setText(messeage)
        if status:
            self.lbl_Status.setStyleSheet("color: green")
        else:
            self.lbl_Status.setStyleSheet("color: red")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    bus = Bus()
    bus.show()
    sys.exit(app.exec_())
