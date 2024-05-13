import winreg

def get_installed_programs():
    installed_programs = []

    for hkey in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
        for subkey in [r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', r'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall']:
            try:
                with winreg.OpenKey(hkey, subkey) as key:
                    i = 0
                    while True:
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                try:
                                    # Try to get the display name of the installed program
                                    program_name = winreg.QueryValueEx(subkey, 'DisplayName')[0]
                                    # Only add the program to the list if its name does not start with 'Security Update'
                                    if not program_name.startswith('Security Update') and not program_name.startswith('Microsoft'):
                                        installed_programs.append(program_name)
                                except EnvironmentError:
                                    pass
                            i += 1
                        except WindowsError:
                            break
            except FileNotFoundError:
                pass

    return installed_programs

installed_programs = get_installed_programs()
for program in installed_programs:
    print(program)