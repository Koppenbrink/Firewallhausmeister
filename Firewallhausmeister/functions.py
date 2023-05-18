from helper import config

prefix = config['prefix']

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
    with  open('./resources/list_of_rules.csv','a') as f:
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
    create_entry_for_rule(exe_name, file_path, action, direction, prefix)
    if direction == 'both':
        for direction in ['in', 'out']:
            rule_name = f'{prefix} {exe_name} {direction} Firewallhausmeister'
            commands = commands + f'netsh advfirewall firewall add rule name="{rule_name}" dir={direction} program="{file_path}" profile=any action={action} && '
        commands = commands[:-4]
    else:
        rule_name = f'{prefix} {exe_name} {direction} Firewallhausmeister'
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
    import win32comext.shell.shell as shell
    commands = create_command_for_firewall_rule(file_path, action, direction)
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+commands)
    return True


def create_command_for_deleting_rule(entry):
    commands = ''
    if entry[2] == 'both':
        for direction in ['in', 'out']:
            rule_name =f'{entry[5]} {entry[0]} {direction} Firewallhausmeister'
            commands = commands + f'netsh advfirewall firewall delete rule name ="{rule_name}" && '
        commands = commands[:-4]
    else:
        rule_name = f'{entry[5]} {entry[0]} {entry[2]} Firewallhausmeister'
        commands = commands + f'netsh advfirewall firewall delete rule name ="{rule_name}"'
    return commands

def delete_rule(entry):
    import win32comext.shell.shell as shell
    commands = create_command_for_deleting_rule(entry)
    print(commands)
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+commands)

def _is_exe(path):
    import os
    print(path)
    return os.path.isfile(path) and os.access(path, os.X_OK)

def _load_database(check=False):
    with open('./resources/list_of_rules.csv','r')as f:
        database = [line.strip().split(',') for line in f]
    if check:
        for idx,line in enumerate(database):
            database[idx][3] = _is_exe(line[4])

    return database

def _write_database(database):
    with open('./resources/list_of_rules.csv','w')as f:
        for line in database:
            f.write(f'{line[0]},{line[1]},{line[2]},{line[3]},{line[4]},{line[5]}\n')

    return True
