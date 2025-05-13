# Set UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Set console appearance
$host.UI.RawUI.WindowTitle = "AI BLOGGING ROBOT PRO - System Insights & Robot Execution"
$host.UI.RawUI.ForegroundColor = "Gray"
$host.UI.RawUI.BackgroundColor = "DarkBlue"
Clear-Host

Write-Host "==============================================================================="
Write-Host "                            AI BLOGGING ROBOT PRO                              "
Write-Host "==============================================================================="
Write-Host "           Preparing to launch your blogging automation robots...             "
Write-Host "==============================================================================="
Write-Host ""
Write-Host "Gathering necessary system information... Please wait..."
Write-Host ""

# Get hidden directories matching robot*
$robotDirs = Get-ChildItem -Path "C:\bloggingbot" -Directory -Force | Where-Object { $_.Name -like "robot*" }
$robotCount = $robotDirs.Count

Write-Host "==============================================================================="
Write-Host "$robotCount hidden blogging robot directories detected."
Write-Host "==============================================================================="

if ($robotCount -eq 0) {
    Write-Host "No robot directories found. Exiting the program."
    Write-Host "===============================================================================" 
    Pause
    exit
}

Write-Host ""
Write-Host "==============================================================================="
Write-Host "Launching Blogging robots. Please standby..."
Write-Host "==============================================================================="

# Launch each robot
$i = 1
foreach ($dir in $robotDirs) {
    Write-Host "===============================================================================" 
    Write-Host "Launching Robot $i in a new PowerShell window..."
    Write-Host "===============================================================================" 

    $envPath = "C:\bloggingbot\robot$i\env$i\Scripts"
    $scriptPath = "C:\bloggingbot\robot$i\__post_blog__.py"

    Start-Process powershell -ArgumentList "-NoExit", "-Command `"cd '$envPath'; .\activate; cd ..; python __post_blog__.py; Pause`"" -WindowStyle Minimized
    $i++
}

Write-Host "===============================================================================" 
Write-Host "All Blogging robots have been successfully launched."
Write-Host "===============================================================================" 
Pause
