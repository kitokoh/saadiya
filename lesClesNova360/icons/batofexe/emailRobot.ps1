# Set UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Set window title and colors
$host.UI.RawUI.WindowTitle = "AI EMAILING ROBOT PRO - System Insights & Email Execution"
$host.UI.RawUI.ForegroundColor = "White"
$host.UI.RawUI.BackgroundColor = "DarkGreen"
Clear-Host

Write-Host "==============================================================================="
Write-Host "                             AI EMAILING ROBOT PRO                              "
Write-Host "===============================================================================" 
Write-Host "         Preparing to launch your email automation robots... Please wait...    "
Write-Host "===============================================================================" 
Write-Host ""

# Initialize counter
$robotDirs = Get-ChildItem -Path "C:\emailingbot" -Directory -Force | Where-Object { $_.Name -like "robot*" }
$robotCount = $robotDirs.Count

Write-Host "===============================================================================" 
Write-Host "$robotCount hidden emailing robot directories detected."
Write-Host "===============================================================================" 

if ($robotCount -eq 0) {
    Write-Host "No robot directories found. Exiting the program."
    Write-Host "===============================================================================" 
    Pause
    exit
}

Write-Host ""
Write-Host "===============================================================================" 
Write-Host "Launching Email robots. Please standby..."
Write-Host "===============================================================================" 

# Launch each robot
$i = 1
foreach ($dir in $robotDirs) {
    Write-Host "===============================================================================" 
    Write-Host "Launching Robot $i in a new minimized PowerShell window..."
    Write-Host "===============================================================================" 

    $envPath = "C:\emailingbot\robot$i\env$i\Scripts"
    $scriptPath = "C:\emailingbot\robot$i\__send_email__.py"

    Start-Process powershell -ArgumentList "-NoExit", "-Command `"cd '$envPath'; .\activate; cd ..; python __send_email__.py; Pause`"" -WindowStyle Minimized
    $i++
}

Write-Host "===============================================================================" 
Write-Host "All Email robots have been successfully launched."
Write-Host "===============================================================================" 
Pause
