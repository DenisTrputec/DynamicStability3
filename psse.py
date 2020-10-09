# -*- coding: utf-8 -*-
"""
Documentation string.
"""

__author__ = "Denis Trputec"
__copyright__ = "HOPS 2020, Dinamička stabilnost"
__credits__ = ["Elvis Mikac", "Denis Trputec"]
__license__ = "HOPS d.o.o."
__version__ = "1.0.1"
__maintainer__ = "Denis Trputec"
__email__ = "denis.trputec@hops.hr"
__status__ = "Development"


import os
import sys
from scripts import error_log as err

psse_path = r'C:\Program Files\PTI\PSSE35\35.1\PSSBIN'
sys.path.append(psse_path)
os.environ['PATH'] += ';' + psse_path
import psspy
from psspy import _i, _f
import redirect
redirect.psse2py()


def initialize():
    psspy.psseinit(10000)
    ierr = psspy.delete_all_plot_channels()
    if ierr != 0:
        msg = err.delete_all_plot_channels(ierr)
        return msg


def read_files(power_flow_file, dynamics_file):
    # If there is error return message string, else return None

    # if not os.path.exists(power_flow_file):
    #     print("No power flow file!")
    if power_flow_file.split('.')[-1] == 'raw':
        ierr = psspy.read(0, power_flow_file)
        if ierr != 0:
            msg = err.read(ierr)
            return msg
    elif power_flow_file.split('.')[-1] == 'rawx':
        ierr = psspy.readx(power_flow_file)
        if ierr != 0:
            msg = err.readx(ierr)
            return msg
    elif power_flow_file.split('.')[-1] == 'sav':
        ierr = psspy.case(power_flow_file)
        if ierr != 0:
            msg = err.case(ierr)
            return msg

    ierr = psspy.dyre_new([1, 1, 1, 1], dynamics_file, "", "", "")
    if ierr != 0:
        msg = err.dyre_new(ierr)
        return msg
    ierr = psspy.dynamics_solution_param_2([_i, _i, _i, _i, _i, _i, _i, _i], [_f, _f, 0.002, _f, _f, _f, _f, _f])
    if ierr != 0:
        msg = err.dynamics_solution_param_2(ierr)
        return msg
    psspy.cong(0)


# <editor-fold desc="### Check user input ###">

def check_out_file(file_name):
    chars_to_remove = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    file_name = ''.join(i for i in file_name if i not in chars_to_remove)
    if file_name == "":
        file_name = "default_name"
    if file_name.endswith('.out') or file_name.endswith('.outx'):
        return "out_files\\" + file_name
    else:
        return "out_files\\" + file_name + '.outx'


def check_bus_number(user_choice):
    # Get all bus numbers in system
    iierr, iarray = psspy.abusint(sid=-1, flag=2, string=["NUMBER"])
    bus_numbers = iarray[0]

    # Get user bus number
    try:
        user_bus_number = int(user_choice.split(' ')[0] if ' ' in user_choice else user_choice)
    except ValueError:
        return -1

    # Check if exists
    return user_bus_number if user_bus_number in bus_numbers else -1

# </editor-fold>


# <editor-fold desc="### Add Channels ###">

def add_bus_channels(out_file, bus_number, options):
    # Initialization
    channel_counter = 0
    # Add Channels
    if options[0]:
        psspy.bus_frequency_channel([-1, bus_number], r"""Hz""")
        channel_counter += 1
    if options[1]:
        psspy.voltage_channel([-1, -1, -1, bus_number], r"""kV""")
        channel_counter += 1
    if options[2]:
        psspy.voltage_and_angle_channel([-1, -1, -1, bus_number], [r"""kV""", r"""DEG"""])
        channel_counter += 2
    # Initialize a PSSE dynamic simulation for state-space simulations and specify the Channel Output File
    ierr = psspy.strt_2(0, out_file)
    if ierr != 0:
        msg = err.dyre_new(ierr)
        return msg
    # Return channel counter
    return channel_counter


def add_branch_channels(out_file, from_bus_number, to_bus_number, circuit_id, option_mva, option_pq, option_p):
    # Initialization
    channel_counter = 0
    # Add Channels
    if option_mva == 1:
        psspy.branch_mva_channel([-1, -1, -1, from_bus_number, to_bus_number], circuit_id, r"""MVA""")
        channel_counter += 1
    if option_pq == 1:
        psspy.branch_p_and_q_channel([-1, -1, -1, from_bus_number, to_bus_number], circuit_id, [r"""P""", r"""Q"""])
        channel_counter += 2
    if option_p == 1:
        psspy.branch_p_channel([-1, -1, -1, from_bus_number, to_bus_number], circuit_id, r"""P""")
        channel_counter += 1
    # Initialize a PSSE dynamic simulation for state-space simulations and specify the Channel Output File
    psspy.strt(0, out_file)
    # Return channel counter
    return channel_counter


def add_machine_channels(out_file, bus_number, machine_id, option_deg, option_p):
    # Initialization
    channel_counter = 0
    # Add Channels
    if option_deg == 1:
        psspy.machine_array_channel([-1, 1, bus_number], machine_id, r"""DEG""")
        channel_counter += 1
    if option_p == 1:
        psspy.machine_array_channel([-1, 2, bus_number], machine_id, r"""P""")
        channel_counter += 1
    # Initialize a PSSE dynamic simulation for state-space simulations and specify the Channel Output File
    psspy.strt(0, out_file)
    # Return plot counter
    return channel_counter

# </editor-fold>


def run(time):
    # Run dynamics
    ierr = psspy.run(tpause=time)
    return ierr


# <editor-fold desc="### Disturbance ###">

def line_fault(from_bus_number, to_bus_number, circuit_id, time):
    # Add branch fault
    psspy.dist_branch_fault(from_bus_number, to_bus_number, circuit_id)
    psspy.run(tpause=time)
    psspy.dist_clear_fault(1)
    psspy.dist_branch_trip(from_bus_number, to_bus_number, circuit_id)


def bus_fault(bus_number, time):
    psspy.dist_bus_fault(bus_number)
    psspy.run(tpause=time)
    psspy.dist_clear_fault()
    psspy.dist_bus_trip(bus_number)

# </editor-fold>


# <editor-fold desc="###  Check if element exist  ###">
def check_if_bus_exist(bus_number):
    iierr, iarray = psspy.abusint(sid=-1, flag=2, string=['NUMBER'])
    for i in range(0, len(iarray[0])):
        if iarray[0][i] == bus_number:
            return True
    return False


def check_if_branch_exist(bus1_number, bus2_number, circuit_id):
    iierr, iarray = psspy.aflowint(sid=-1, owner=1, ties=1, flag=2, string=['FROMNUMBER', 'TONUMBER'])
    cierr, carray = psspy.aflowchar(sid=-1, owner=1, ties=1, flag=2, string=['ID'])
    for i in range(0, len(iarray[0])):
        if iarray[0][i] == bus1_number and (iarray[1][i] == bus2_number):
            if carray[0][i] == circuit_id:
                return True
            try:
                if int(carray[0][i]) == int(circuit_id):
                    return True
            except ValueError:
                return False
    return False


def check_if_machine_exist(bus_number, machine_id):
    iierr, iarray = psspy.amachint(sid=-1, flag=4, string=['NUMBER'])
    cierr, carray = psspy.amachchar(sid=-1, flag=4, string=['ID'])
    for i in range(0, len(iarray[0])):
        if iarray[0][i] == bus_number:
            if carray[0][i] == machine_id:
                return True
            try:
                if int(carray[0][i]) == int(machine_id):
                    return True
            except ValueError:
                return False
    return False


# </editor-fold>


if __name__ == '__main__':
    initialize()
    read_files("", "")
