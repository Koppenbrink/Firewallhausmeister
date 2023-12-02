from helper import csv_location
import win32comext.shell.shell as shell
import subprocess
from os import path
import sys,os
from config import *

'''def resource_path(relative_path):
    bundle_dir = path.abspath(path.dirname(__file__))
    path_to_dat = path.join(bundle_dir, relative_path)

    return path_to_dat'''

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


csv_database = resource_path(csv_location)
def get_firewall_status():
    command = f'netsh advfirewall show allprofiles state'
    output = subprocess.check_output(command, text=True)
    return dict(zip(['domain','private','public'],[row.split()[1] for row in output.split("\n") if "State" in row]))

def extract_exe_name(file_path:str) -> str:
    '''
    extracts the name of an exe from a file path
    :param file_path: the file path from which the name should be extracted
    :return: the name of the exe
    '''
    i = 1
    exeName = ''
    while i <= len(file_path):
        if file_path[-i] == '\\':
            break
        if i > 4:
            exeName = file_path[-i] + exeName
        i += 1
    return exeName

def create_entry_for_rule(exe_name:str, file_path:str, action:str, direction:str, rule_name:str) -> bool:
    '''
    creates an entry in the database
    :param exe_name:
    :param file_path:
    :param action:
    :param direction:
    :param rule_name:
    :return:
    '''
    with  open(csv_database,'a') as f:
        f.write(f'{exe_name},{action},{direction},NaN,{file_path},{rule_name}\n')
    return True

def create_command_for_firewall_rule(file_path:str, action:str, direction:str) -> str:
    '''
    generates the command for creating a firewall rule for the exe in the given path and sets an entry in the database
    :param file_path: location of the exe
    :param action: what to do with it block/allow
    :param direction: direction for the rule in/out
    :return: the command to set the rule
    '''
    commands = ''

    exe_name = extract_exe_name(file_path)
    create_entry_for_rule(exe_name, file_path, action, direction, config['prefix'])
    if direction == 'both':
        for direction in ['in', 'out']:
            rule_name = f'{config["prefix"]} {exe_name} {direction} Firewallhausmeister'
            commands = commands + f'netsh advfirewall firewall add rule name="{rule_name}" dir={direction} program="{file_path}" profile=any action={action} && '
        commands = commands[:-4]
    else:
        rule_name = f'{config["prefix"]} {exe_name} {direction} Firewallhausmeister'
        commands = commands + f'netsh advfirewall firewall add rule name="{rule_name}" dir={direction} program="{file_path}" profile=any action={action}\n cmd /c'

    return commands

def set_rule(file_path:str, action:str, direction:str) -> str:
    """
    sets a rule for an .exe in the specified direction and creates an entry in the database
    :param file_path: location of the .exe
    :param action: what to do with it block/allow
    :param direction: the direction in which the rule should be set up
    :return:
    """
    commands = create_command_for_firewall_rule(file_path, action, direction)
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+commands)
    return True


def create_command_for_deleting_rules(list_of_entries):
    commands = ''
    for entry in list_of_entries:
        if entry[2] == 'both':
            for direction in ['in', 'out']:
                rule_name =f'{entry[5]} {entry[0]} {direction} Firewallhausmeister'
                commands = commands + f'netsh advfirewall firewall delete rule name = "{rule_name}" && '
        else:
            rule_name = f'{entry[5]} {entry[0]} {entry[2]} Firewallhausmeister'
            commands = commands + f'netsh advfirewall firewall delete rule name = "{rule_name}" && '
    commands = commands[:-4]
    return commands

def delete_rules(list_of_idxes):
    if not list_of_idxes:
        pass

    import win32comext.shell.shell as shell
    database = _load_database()

    list_of_entries = [database[x] for x in list_of_idxes]

    commands = create_command_for_deleting_rules(list_of_entries)
    database = _load_database()

    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+commands)

    # write new database to file
    _write_database([database[x] for x in range(len(database)) if x not in list_of_idxes])

def profile_switch(profile,action):
    """
    :param profile: profile ("domain","private", "public" or "all") to turn on/off
    :param action: "ON" or "OFF"
    :return: True if executed without error
    """
    command = f'netsh advfirewall set {profile}profile state {action}'
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c ' + command)

def interpreter(line):
    proc = subprocess.Popen(line, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    return out.decode(), err.decode()

def _is_exe(path):
    last_letters = path[-4:]==".exe"
    return os.path.isfile(path) and os.access(path, os.X_OK) and last_letters

def _load_database(check=False):
    with open(csv_database,'r')as f:
        database = [line.strip().split(',') for line in f]
    if check:
        for idx,line in enumerate(database):
            database[idx][3] = _is_exe(line[4])

    return database

def _write_database(database):
    with open(csv_database,'w')as f:
        for line in database:
            f.write(f'{line[0]},{line[1]},{line[2]},{line[3]},{line[4]},{line[5]}\n')

    return True
