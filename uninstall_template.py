import os
import shutil
import subprocess
import sys

def run_as_admin(argv=None, debug=False):
    if os.name == 'nt':
        try:
            from ctypes import windll
            if windll.shell32.IsUserAnAdmin():
                return True
            if debug and sys.stderr:
                sys.stderr.write('stderr is available.\n')
            if argv is None:
                argv = sys.argv
            if hasattr(sys, '_MEIPASS'):
                # Support pyinstaller wrapped program.
                arguments = argv[1:]
            else:
                arguments = argv
            if debug and sys.stderr:
                sys.stderr.write(f'Run as admin: starting: {str(argv)}\n')
            windll.shell32.ShellExecuteW(None, "runas", argv[0], ' '.join(arguments), None, 1)
            if debug and sys.stderr:
                sys.stderr.write('Run as admin: finished\n')
            return False
        except Exception as e:
            if debug and sys.stderr:
                sys.stderr.write(f'Run as admin: failed: {str(e)}\n')
            return False
    else:
        return True

def remove_program_files():
    program_files_path = "C:\\Program Files\\Shopos Login"
    
    try:
        if not run_as_admin():
            return

        # Delete program files
        if os.path.exists(program_files_path):
            shutil.rmtree(program_files_path)
    except Exception as e:
        print(f"Failed to remove program files: {str(e)}")

def remove_autostart_entry():
    current_user = os.getlogin()
    autostart_path = f"C:\\Users\\{current_user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\login.pyw"
    
    try:
        if not run_as_admin():
            return

        # Delete autostart entry
        if os.path.exists(autostart_path):
            os.remove(autostart_path)
    except Exception as e:
        print(f"Failed to remove autostart entry: {str(e)}")

def remove_registry_entries():
    script_name = "login.py"  # Change this to your actual script name
    
    try:
        if not run_as_admin():
            return

        # Remove registry entries
        subprocess.Popen(["reg", "delete", f"HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{script_name}", "/f"])
    except Exception as e:
        print(f"Failed to remove registry entry: {str(e)}")

if __name__ == "__main__":
    print("Uninstalling Shopos Login...")
    
    # Remove autostart entry
    print("Removing autostart entry...")
    remove_autostart_entry()
    
    # Remove registry entries
    print("Removing registry entries...")
    remove_registry_entries()
    
    # Remove program files
    print("Removing program files...")
    remove_program_files()
    
    print("Shopos Login has been successfully uninstalled.")
