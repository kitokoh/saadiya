[Setup]
AppName=Leopardo V2
AppVersion=1.0
DefaultDirName={pf}\LeopardoV2
DefaultGroupName=Leopardo V2
UninstallDisplayIcon={app}\LeopardoV2.exe
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "dist\LeopardoV2.exe"; DestDir: "{app}"
Source: "..\..\resources\*"; DestDir: "{app}\resources"; Flags: recursesubdirs

[Icons]
Name: "{group}\Leopardo V2"; Filename: "{app}\LeopardoV2.exe"
Name: "{commondesktop}\Leopardo V2"; Filename: "{app}\LeopardoV2.exe"

[Run]
Filename: "{app}\LeopardoV2.exe"; Description: "Launch Leopardo V2"; Flags: nowait postinstall skipifsilent
