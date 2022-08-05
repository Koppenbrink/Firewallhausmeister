import subprocess
import win32comext.shell.shell as shell
from helper import prefix

def run_win_cmd(cmd):
    result = []
    process = subprocess.Popen(cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    for line in process.stdout:
        result.append(line)
    errcode = process.returncode
    for line in result:
        print(line)
    if errcode is not None:
        raise Exception('cmd %s failed, see above for details', cmd)
    return result

def extract_exe_name(file_path):
    i = 1
    exeName = ''
    while i <= len(file_path):
        if file_path[-i] == '\\':
            break
        if i > 4:
            exeName = file_path[-i] + exeName
        i += 1
    return exeName

def create_command(file_path, action, dir):
    print('test')
    commands = ''
    if dir == 'both':
        for dir in ['in', 'out']:
            rulename = prefix + extract_exe_name(file_path) + ' ' + dir + ' Firewallhausmeister'
            commands = commands + f'netsh advfirewall firewall add rule name="{rulename}" dir={dir} program="{file_path}" profile=any action={action} && '
        commands = commands[:-4]
    else:
        rulename = prefix + extract_exe_name(file_path) + ' ' + dir + ' Firewallhausmeister'
        commands = commands + f'netsh advfirewall firewall add rule name="{rulename}" dir={dir} program="{file_path}" profile=any action={action}\n cmd /c'
    print(commands)
    return commands
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+commands)

def set_rule(file_path, action, dir):
    commands = create_command(file_path, action, dir)
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+commands)
