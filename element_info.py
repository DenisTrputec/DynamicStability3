# -*- coding: utf-8 -*-
"""
Documentation string.
"""

__author__ = "Denis Trputec"
__copyright__ = "HOPS 2020, Element information for 'Dinamička stabilnost'"
__credits__ = ["Denis Trputec"]
__license__ = "HOPS d.o.o."
__version__ = "1.0.1"
__maintainer__ = "Denis Trputec"
__email__ = "denis.trputec@hops.hr"
__status__ = "Development"


import os
import sys
from configparser import ConfigParser
psse_path = r'C:\Program Files\PTI\PSSE35\35.1\PSSBIN'
sys.path.append(psse_path)
os.environ['PATH'] += ';' + psse_path
import psspy

# Load config file
config_file_path = "config.ini"
config = ConfigParser()
config.read(config_file_path)

# <editor-fold desc="###  Common Functions  ###">


def start_psse():
    power_flow_file = config["path"]["raw"]

    # Start PSSE and import files
    psspy.psseinit(10000)
    if power_flow_file.split('.')[-1] == 'raw':
        psspy.read(0, power_flow_file)
    elif power_flow_file.split('.')[-1] == 'rawx':
        psspy.readx(power_flow_file)
    elif power_flow_file.split('.')[-1] == 'sav':
        psspy.case(power_flow_file)


def return_parameter_lengths(int_len, real_len, char_len):
    return [int_len, int_len + real_len, int_len + real_len + char_len]


def create_array(all_arrays):
    array = []
    for i in range(0, len(all_arrays[0][0])):
        element = []
        for j in range(0, len(all_arrays)):
            for k in range(0, len(all_arrays[j])):
                element.append(all_arrays[j][k][i])
        array.append(element)
    return array


def filter_array(parameter_lengths, array, user_filter):
    # Parameter_lengths because of different input types
    new_array = []
    for element in array:
        flags = [False] * len(element)
        for i in range(0, len(element)):
            if i < parameter_lengths[0]:
                if user_filter[i] != "":
                    try:
                        if int(user_filter[i]) == element[i]:
                            flags[i] = True
                    except ValueError:
                        pass
                else:
                    flags[i] = True
            elif i < parameter_lengths[1]:
                if user_filter[i] != "":
                    try:
                        if float(user_filter[i]) == element[i]:
                            flags[i] = True
                    except ValueError:
                        pass
                else:
                    flags[i] = True
            else:
                if user_filter[i] != "":
                    if user_filter[i] in element[i]:
                        flags[i] = True
                else:
                    flags[i] = True
        if all(flag is True for flag in flags):
            new_array.append(element)
    return new_array


def return_header(user_options, parameter_list):
    header = []
    for i in range(0, len(user_options)):
        if user_options[i]:
            header.append(parameter_list[i])
    return header


def return_info(user_options, array):
    info = []
    for i in range(0, len(array)):
        temp_array = []
        for j in range(0, len(user_options)):
            if user_options[j]:
                temp_array.append(array[i][j])
        info.append(temp_array)
    return info

# </editor-fold desc>


# <editor-fold desc="###  GUI Functions  ###">

def bus_info(user_options, user_filter):
    # Lists of parameters
    int_list = ['NUMBER', 'TYPE', 'AREA', 'ZONE']
    real_list = ['BASE', 'KV', 'ANGLED']
    char_list = ['NAME', 'EXNAME']
    parameter_list = int_list + real_list + char_list
    parameter_lengths = return_parameter_lengths(len(int_list), len(real_list), len(char_list))

    # Create array of bus data
    iierr, iarray = psspy.abusint(sid=-1, flag=2, string=int_list)
    rierr, rarray = psspy.abusreal(sid=-1, flag=2, string=real_list)
    cierr, carray = psspy.abuschar(sid=-1, flag=2, string=char_list)
    all_arrays = [iarray, rarray, carray]
    array = create_array(all_arrays)

    # Filters
    array = filter_array(parameter_lengths, array, user_filter)

    # Return information
    header = return_header(user_options, parameter_list)
    info = return_info(user_options, array)
    return header, info


def branch_info(user_options, user_filter):
    # Lists of parameters
    int_list = ['FROMNUMBER', 'TONUMBER', 'STATUS']
    real_list = ['AMPS', 'RATEA', 'P', 'Q', 'MVA']
    char_list = ['ID', 'FROMNAME', 'FROMEXNAME', 'TONAME', 'TOEXNAME']
    parameter_list = int_list + real_list + char_list
    parameter_lengths = return_parameter_lengths(len(int_list), len(real_list), len(char_list))

    # Create array of branch data
    iierr, iarray = psspy.aflowint(sid=-1, owner=1, ties=1, flag=2, string=int_list)
    rierr, rarray = psspy.aflowreal(sid=-1, owner=1, ties=1, flag=2, string=real_list)
    cierr, carray = psspy.aflowchar(sid=-1, owner=1, ties=1, flag=2, string=char_list)
    all_arrays = [iarray, rarray, carray]
    array = create_array(all_arrays)

    # Filters
    array = filter_array(parameter_lengths, array, user_filter)

    # Print information
    header = return_header(user_options, parameter_list)
    info = return_info(user_options, array)
    return header, info


def machine_info(user_options, user_filter):
    # Lists of parameters
    int_list = ['NUMBER', 'STATUS']
    real_list = ['MBASE', 'GENTAP', 'PGEN', 'QGEN', 'MVA', 'PMAX', 'PMIN', 'QMAX', 'QMIN']
    char_list = ['ID', 'NAME', 'EXNAME']
    parameter_list = int_list + real_list + char_list
    parameter_lengths = return_parameter_lengths(len(int_list), len(real_list), len(char_list))

    # Create array of machine data
    iierr, iarray = psspy.amachint(sid=-1, flag=4, string=int_list)
    rierr, rarray = psspy.amachreal(sid=-1, flag=4, string=real_list)
    cierr, carray = psspy.amachchar(sid=-1, flag=4, string=char_list)
    all_arrays = [iarray, rarray, carray]
    array = create_array(all_arrays)

    # Filters
    array = filter_array(parameter_lengths, array, user_filter)

    # Print information
    header = return_header(user_options, parameter_list)
    info = return_info(user_options, array)
    return header, info


# </editor-fold>


# <editor-fold desc="###  CLI Functions  ###">

def cli_options():
    option = -1
    while option == -1:
        option = int(input("\nChoose option:\n\t1 - Bus Info\n\t2 - Branch Info\n\t3 - Machine Info\n\nOption: "))
        if option == 1:
            cli_bus_info()
        elif option == 2:
            cli_branch_info()
        elif option == 3:
            cli_machine_info()
        else:
            print("Invalid option!")
            option = -1


def cli_user_input(parameter_list):
    # Initialization
    user_options = [False] * len(parameter_list)
    user_filter = []

    # Filter by columns
    print(parameter_list)
    option_string = input("Options you want to print (use space (' ') to separate them): ")
    user_option_list = option_string.split(' ')
    for i in range(0, len(parameter_list)):
        if parameter_list[i] in user_option_list:
            user_options[i] = True

    # Filter by rows
    print("\nFilter by:")
    for i in range(0, len(parameter_list)):
        user_filter.append(input(parameter_list[i] + ": "))

    return user_options, user_filter


def cli_bus_info():
    # Lists of parameters
    int_list = ['NUMBER', 'TYPE', 'AREA', 'ZONE']
    real_list = ['BASE', 'KV', 'ANGLED']
    char_list = ['NAME', 'EXNAME']
    parameter_list = int_list + real_list + char_list
    parameter_lengths = return_parameter_lengths(len(int_list), len(real_list), len(char_list))

    # Create array of bus data
    iierr, iarray = psspy.abusint(sid=-1, flag=2, string=int_list)
    rierr, rarray = psspy.abusreal(sid=-1, flag=2, string=real_list)
    cierr, carray = psspy.abuschar(sid=-1, flag=2, string=char_list)
    all_arrays = [iarray, rarray, carray]
    array = create_array(all_arrays)

    # Filters
    user_options, user_filter = cli_user_input(parameter_list)
    array = filter_array(parameter_lengths, array, user_filter)

    # Print information
    print("\nOptions selected:")
    print(return_header(user_options, parameter_list))
    info = return_info(user_options, array)
    for element in info:
        print(element)


def cli_branch_info():
    # Lists of parameters
    int_list = ['FROMNUMBER', 'TONUMBER', 'STATUS']
    real_list = ['AMPS', 'RATEA', 'P', 'Q', 'MVA']
    char_list = ['ID', 'FROMNAME', 'FROMEXNAME', 'TONAME', 'TOEXNAME']
    parameter_list = int_list + real_list + char_list
    parameter_lengths = return_parameter_lengths(len(int_list), len(real_list), len(char_list))

    # Create array of branch data
    iierr, iarray = psspy.aflowint(sid=-1, owner=1, ties=1, flag=2, string=int_list)
    rierr, rarray = psspy.aflowreal(sid=-1, owner=1, ties=1, flag=2, string=real_list)
    cierr, carray = psspy.aflowchar(sid=-1, owner=1, ties=1, flag=2, string=char_list)
    all_arrays = [iarray, rarray, carray]
    array = create_array(all_arrays)

    # Filters
    user_options, user_filter = cli_user_input(parameter_list)
    array = filter_array(parameter_lengths, array, user_filter)

    # Print information
    print("\nOptions selected:")
    print(return_header(user_options, parameter_list))
    info = return_info(user_options, array)
    for element in info:
        print(element)


def cli_machine_info():
    # Lists of parameters
    int_list = ['NUMBER', 'STATUS']
    real_list = ['MBASE', 'GENTAP', 'PGEN', 'QGEN', 'MVA', 'PMAX', 'PMIN', 'QMAX', 'QMIN']
    char_list = ['ID', 'NAME', 'EXNAME']
    parameter_list = int_list + real_list + char_list
    parameter_lengths = return_parameter_lengths(len(int_list), len(real_list), len(char_list))

    # Create array of machine data
    iierr, iarray = psspy.amachint(sid=-1, flag=4, string=int_list)
    rierr, rarray = psspy.amachreal(sid=-1, flag=4, string=real_list)
    cierr, carray = psspy.amachchar(sid=-1, flag=4, string=char_list)
    all_arrays = [iarray, rarray, carray]
    array = create_array(all_arrays)

    # Filters
    user_options, user_filter = cli_user_input(parameter_list)
    array = filter_array(parameter_lengths, array, user_filter)

    # Print information
    print("\nOptions selected:")
    print(return_header(user_options, parameter_list))
    info = return_info(user_options, array)
    for element in info:
        print(element)

# </editor-fold">


if __name__ == '__main__':
    start_psse()
    cli_options()
