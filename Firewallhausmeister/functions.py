import win32comext.shell.shell as shell
from helper import praefix

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

def create_command_for_firewall_rule(file_path:str, action:str, dir:str) -> str:
    '''
    generates the command for creating a firewall rule for the exe in the given path
    :param file_path: location of the exe
    :param action: what to do with it block/allow
    :param dir: direction for the rule in/out
    :return: the command to set the rule
    '''
    commands = ''
    if dir == 'both':
        for dir in ['in', 'out']:
            rule_name = praefix + extract_exe_name(file_path) + ' ' + dir + ' Firewallhausmeister'
            commands = commands + f'netsh advfirewall firewall add rule name="{rule_name}" dir={dir} program="{file_path}" profile=any action={action} && '
        commands = commands[:-4]
    else:
        rule_name = praefix + extract_exe_name(file_path) + ' ' + dir + ' Firewallhausmeister'
        commands = commands + f'netsh advfirewall firewall add rule name="{rule_name}" dir={dir} program="{file_path}" profile=any action={action}\n cmd /c'
    return commands

def set_rule(file_path:str, action:str, direction:str) -> str:
    '''
    sets a rule for a .exe in the specified direction
    :param file_path: location of the .exe
    :param action: what to do with it block/allow
    :param direction: the direction in which the rule should be set up
    :return:
    '''
    commands = create_command_for_firewall_rule(file_path, action, direction)
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+commands)
    return True
