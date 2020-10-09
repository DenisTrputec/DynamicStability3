# <editor-fold desc="###  PSSEv35 API errors  ###">
def delete_all_plot_channels(ierr):
    error_list = ["No error occurred", "Prerequisite requirements for API are not met"]
    return "PSSE error: " + error_list[ierr]


def read(ierr):
    error_list = ["No error occurred", "Invalid flag for bus number or name value", "Invalid revision number",
                  "Unable to convert file", "Error opening temporary file", "Error opening power flow raw data file",
                  "Prerequisite requirements for API are not met"]
    return "PSSE error: " + error_list[ierr]


def readx(ierr):
    error_list = ["No error occurred", "Invalid revision number", "Unable to convert file",
                  "Error opening extended power flow raw data file", "Prerequisite requirements for API are not met"]
    return "PSSE error: " + error_list[ierr]


def case(ierr):
    error_list = ["No error occurred", "Saved case file is blank", "Error reading from saved case file",
                  "Error opening saved case file", "Prerequisite requirements for API are not met"]
    return "PSSE error: " + error_list[ierr]


def dyre_new(ierr):
    error_list = ["No error occurred", "Invalid STARTINDX value", "Error opening Dynamics Model Raw Data File",
                  "Prerequisite requirements for API are not met"]
    return "PSSE error: " + error_list[ierr]


def dynamics_solution_param_2(ierr):
    error_list = ["No error occurred", "Prerequisite requirements for API are not met"]
    return "PSSE error: " + error_list[ierr]


def strt_2(ierr):
    error_list = ["No error occurred", "Generators are not converted", "Invalid OPTIONS value",
                  "Prior initialization modified the loads - pick up original converted case",
                  "Error opening output file", "Prerequisite requirements for API are not met"]
    return "PSSE error: " + error_list[ierr]


def run(ierr):
    error_list = ["No error occurred", "Activity STRT needs to be executed", "Invalid OPTION value",
                  "Generators are not converted", "Error opening the current channel output file",
                  "Prerequisite requirements for API are not met"]
    return "PSSE error: " + error_list[ierr]

# </editor-fold desc>
