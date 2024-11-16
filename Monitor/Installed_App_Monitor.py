import winreg

def get_installed_apps():
    """
    Retrieves a list of installed applications on a Windows system.

    This function scans the Windows registry for installed applications,
    checking both 64-bit and 32-bit registry paths, as well as user-specific
    installations.

    Returns:
        list: A list of strings, where each string is the display name of an
              installed application. The list may contain duplicates if an
              application is registered in multiple locations.

    Note:
        This function is specific to Windows operating systems and relies on
        the winreg module to access the Windows registry.
    """
    apps = []

    # Registry paths for 64-bit and 32-bit apps on Windows
    paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
    ]

    for root, path in paths:
        try:
            with winreg.OpenKey(root, path) as key:
                for i in range(0, winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            app_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            apps.append(app_name)
                    except (FileNotFoundError, OSError, IndexError):
                        # Skip entries that are incomplete or not accessible
                        continue
        except FileNotFoundError:
            # Skip paths that do not exist
            pass

    return apps

