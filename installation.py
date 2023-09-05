import tkinter as tk
from tkinter import simpledialog
import shutil
import os
import ctypes
import getpass
import subprocess
import sys

def create_uninstall_script():
    # Define the source and destination paths for uninstall.py
    source_uninstall_script = 'C:\\Users\\ASUS\\Documents\\College\\Projects\\Login\\Installation\\uninstall_template.py'  # Replace with the actual path to your uninstall script template
    destination_uninstall_script = 'C:\\Program Files\\Shopos Login\\uninstall.py'
    
    # Copy the uninstall script from the predefined location to the installation directory
    shutil.copy(source_uninstall_script, destination_uninstall_script)

def register_in_programs_and_features(script_path):
    script_name = os.path.splitext(os.path.basename(script_path))[0]
    uninstall_key = f"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{script_name}"
    
    try:
        # Create an uninstaller registry entry
        subprocess.Popen(["reg", "add", f"HKLM\\{uninstall_key}", "/ve", "/t", "REG_SZ", "/d", script_name])
        subprocess.Popen(["reg", "add", f"HKLM\\{uninstall_key}", "/t", "REG_SZ", "/v", "DisplayName", "/d", script_name])
        subprocess.Popen(["reg", "add", f"HKLM\\{uninstall_key}", "/t", "REG_SZ", "/v", "UninstallString", "/d", f'pythonw.exe "{script_path}"'])
    except Exception as e:
        status_label.config(text=f"Failed to add to Programs and Features: {str(e)}")

def install_script():
    autostart_option = autostart_var.get()
    
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)
    
    destination_folder = "C:\\Program Files\\Shopos Login"
    
    # Check if the destination folder exists; if not, create it
    if not os.path.exists(destination_folder):
        try:
            os.makedirs(destination_folder)
        except Exception as e:
            status_label.config(text=f"Failed to create destination folder: {str(e)}")
            return
    
    # Prompt the user for username and password
    username = simpledialog.askstring("Input", "Enter your username:")
    password = simpledialog.askstring("Input", "Enter your password:", show='*')
    
    # Source and destination paths for the program script
    source_script_path = r'C:\Users\ASUS\Documents\College\Projects\Login\Installation\login.py'
    destination_script_path = os.path.join(destination_folder, 'login.py')
    
    try:
        # Copy the program script to the destination folder
        shutil.copy(source_script_path, destination_script_path)
        
        # Create the uninstall script
        create_uninstall_script()
        
        # Register the uninstaller in "Programs and Features"
        register_in_programs_and_features(destination_script_path)
        
        # Check if autostart is selected
        if autostart_option:
            current_user = getpass.getuser()
            autostart_path = f"C:\\Users\\{current_user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\login.pyw"
            
            # Create a shortcut in the startup folder
            with open(autostart_path, "w") as shortcut_file:
                shortcut_file.write(f'pythonw.exe "{destination_script_path}"')
        
        status_label.config(text="Installation successful.")
    except Exception as e:
        status_label.config(text=f"Installation failed: {str(e)}")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Create the main window
window = tk.Tk()
window.title('Script Installation')

# Create and pack GUI elements
autostart_var = tk.IntVar()
autostart_checkbox = tk.Checkbutton(window, text="Add to autostart", variable=autostart_var)
autostart_checkbox.pack()

install_button = tk.Button(window, text="Install", command=install_script)
install_button.pack()

status_label = tk.Label(window, text="")
status_label.pack()

window.mainloop()
