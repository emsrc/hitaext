; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
AppName=Hitaext
AppVerName=Hitaext 1.0
AppPublisher=Tilburg University - Erwin Marsi
AppPublisherURL=http://daeso.uvt.nl/
AppSupportURL=http://daeso.uvt.nl/
AppUpdatesURL=http://daeso.uvt.nl/
DefaultDirName={pf}\Hitaext
DefaultGroupName=Hitaext
LicenseFile=D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\COPYING
InfoBeforeFile=D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\README
InfoAfterFile=D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\iss\infoafter.txt
OutputDir=D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\iss
OutputBaseFilename=hitaext-1.0-setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\dist\hitaext.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\dist\wxmsw28uh_html_vc.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\dist\_controls_.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\dist\_core_.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\dist\_elementtree.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\dist\_gdi_.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\dist\_html.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\dist\_misc_.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\dist\_socket.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\dist\_ssl.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\dist\_windows_.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\dist\bz2.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\dist\library.zip"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\dist\MSVCR71.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\dist\pyexpat.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\dist\python25.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\dist\unicodedata.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\dist\w9xpopen.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\dist\wxbase28uh_net_vc.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\dist\wxbase28uh_vc.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\dist\wxmsw28uh_adv_vc.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\dist\wxmsw28uh_core_vc.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\doc\*"; DestDir: "{app}\doc"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\data\*"; DestDir: "{app}\data"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\README"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\INSTALL"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\CHANGES"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Documents and Settings\Erwin\Desktop\Projects\trunk\software\intern\hitaext\COPYING"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\Hitaext"; Filename: "{app}\hitaext.exe"
Name: "{commondesktop}\Hitaext"; Filename: "{app}\hitaext.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\hitaext.exe"; Description: "{cm:LaunchProgram,Hitaext}"; Flags: nowait postinstall skipifsilent

