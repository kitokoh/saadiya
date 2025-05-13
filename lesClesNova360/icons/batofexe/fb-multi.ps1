# Pour forcer l'encodage en UTF-8
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()

# Définir les couleurs de la console : texte blanc sur fond bleu (équivalent à COLOR 1F)
$host.UI.RawUI.BackgroundColor = "DarkBlue"
$host.UI.RawUI.ForegroundColor = "White"
Clear-Host

# Définir le titre de la fenêtre
$host.UI.RawUI.WindowTitle = "AI FB ROBOT PRO - System Info & Robot Execution"

# Redimensionner la fenêtre de la console (équivalent à MODE con)
$size = $host.UI.RawUI.WindowSize
$size.Width = 60
$size.Height = 15
$host.UI.RawUI.WindowSize = $size
$host.UI.RawUI.BufferSize = $size

# Affichage de la bannière
Write-Host "===============================================================================" 
Write-Host "                             AI FB ROBOT PRO                                   "
Write-Host "===============================================================================" 
Write-Host "              Initializing system and preparing robots...                     "
Write-Host "===============================================================================" 
Write-Host ""
Write-Host "Please hold on while we gather necessary system information..."
Write-Host ""

# Initialiser le compteur de robots
$robotCount = 0

# Rechercher les dossiers cachés dans C:\bon qui commencent par "robot"
$robotDirs = Get-ChildItem -Path "C:\bon" -Directory -Hidden -Name | Where-Object { $_ -like "robot*" }

# Compter le nombre de répertoires de robots trouvés
$robotCount = $robotDirs.Count

# Afficher le nombre de répertoires détectés
Write-Host "===============================================================================" 
Write-Host "$robotCount hidden robot directories detected."
Write-Host "===============================================================================" 

# Si aucun dossier robot n'est trouvé, quitter le script
if ($robotCount -eq 0) {
    Write-Host "No robot directories found! Exiting program."
    Write-Host "===============================================================================" 
    Pause
    exit
}

# Message de démarrage pour les robots
Write-Host ""
Write-Host "===============================================================================" 
Write-Host "Launching robots now. Thank you for your patience..."
Write-Host "===============================================================================" 

# Exécuter chaque robot dans une fenêtre PowerShell séparée
$counter = 1
foreach ($robotDir in $robotDirs) {
    Write-Host "===============================================================================" 
    Write-Host "Launching Robot $counter in a new window..."
    Write-Host "===============================================================================" 

    # Créer une nouvelle fenêtre PowerShell minimisée pour chaque robot
    Start-Process powershell -ArgumentList "-NoExit", "-Command", {
        # Réinitialiser l'affichage pour chaque robot
        $host.UI.RawUI.BackgroundColor = "DarkBlue"
        $host.UI.RawUI.ForegroundColor = "White"
        Clear-Host
        $host.UI.RawUI.WindowTitle = "Robot $counter - AI FB ROBOT PRO"

        # Activer l'environnement virtuel du robot
        Write-Host "===============================================================================" 
        Write-Host "Activating environment for Robot $counter..."
        Write-Host "===============================================================================" 
        Set-Location "C:\bon\$robotDir\env$counter\Scripts"
        .\Activate.ps1

        # Naviguer vers le répertoire du robot
        Write-Host "===============================================================================" 
        Write-Host "Navigating to Robot $counter directory..."
        Write-Host "===============================================================================" 
        Set-Location "C:\bon\$robotDir"

        # Exécuter le script Python du robot
        Write-Host "===============================================================================" 
        Write-Host "Executing Robot $counter script..."
        Write-Host "===============================================================================" 
        python __post_in_groupsx__.py

        # Affichage de la fin du processus du robot
        Write-Host "===============================================================================" 
        Write-Host "Robot $counter process completed."
        Write-Host "===============================================================================" 
        Pause
    }

    $counter++
}

# Fin de l'exécution
Write-Host "===============================================================================" 
Write-Host "All robots have successfully started in separate minimized windows."
Write-Host "===============================================================================" 
Pause
