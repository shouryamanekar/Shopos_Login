; Shopos Login Installer Script
Outfile "ShoposLoginInstaller.exe"
RequestExecutionLevel admin

; MUI Settings
!include "MUI2.nsh"
!define MUI_ABORTWARNING
!define MUI_ICON "your_icon.ico"  ; Replace with your custom icon
!define MUI_UNICON "your_icon.ico"  ; Replace with your custom uninstaller icon
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "header.bmp"  ; Replace with your custom header image
!define MUI_LICENSEPAGE
!define MUI_LICENSEPAGE_TEXT "End User License Agreement"
!insertmacro MUI_PAGE_LICENSE "license.txt"  ; Specify your license agreement file

; Default section
Section

; Set the default installation directory to C:\Program Files\Shopos Login
SetOutPath "C:\Program Files\Shopos Login"  ; Specify the desired default installation directory

; Include Readme.txt in the installation
File "Readme.txt"  ; Copy your Readme.txt file

; Your installer will typically copy files and perform other tasks here.
File "installation.py"  ; Copy your Python script
File "login.py"  ; Copy your Login script
File "uninstall_template.py"  ; Copy the uninstaller

; Create the uninstaller
WriteUninstaller "$INSTDIR\Uninstall.exe"

SectionEnd

; User interface page to select installation location
Page Directory
Page InstFiles

; Uninstaller
UninstPage uninstConfirm
UninstPage instfiles

Section "Uninstall"
; Remove files, registry entries, etc.
RMDir /r "C:\Program Files\Shopos Login"
SectionEnd

Section "Run Installation Script"
; Execute the installation script
ExecWait '"$INSTDIR\python.exe" "$INSTDIR\installation.py"'

; Optionally, display a message box to inform the user when the installation script is complete
MessageBox MB_ICONINFORMATION|MB_OK "Installation script has been executed."
SectionEnd
