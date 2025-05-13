# Forcer l'encodage en UTF-8 pour l'affichage
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()

# Définir les couleurs de la console : texte blanc sur fond bleu (équivalent à COLOR 1F)
$host.UI.RawUI.BackgroundColor = "DarkBlue"
$host.UI.RawUI.ForegroundColor = "White"
Clear-Host

# Définir le titre de la fenêtre
$host.UI.RawUI.WindowTitle = "AI FB ROBOT PRO - Robot 9"

# Redimensionner la console (équivalent à MODE con)
$size = $host.UI.RawUI.WindowSize
$size.Width = 60
$size.Height = 15
$host.UI.RawUI.WindowSize = $size
$host.UI.RawUI.BufferSize = $size

# Bannière
Write-Host "===============================================================================" 
Write-Host "                             AI FB ROBOT PRO                                   "
Write-Host "===============================================================================" 
Write-Host "                 Démarrage de Robot 9 en cours...                              "
Write-Host "===============================================================================" 
Write-Host ""

# Vérifier l'existence du répertoire
$robotPath = "C:\bon\robot9"
if (-Not (Test-Path $robotPath)) {
    Write-Host "Le répertoire de Robot 9 est introuvable !"
    Write-Host "===============================================================================" 
    Pause
    exit
}

# Activation de l'environnement virtuel
Write-Host "===============================================================================" 
Write-Host "Activation de l'environnement pour Robot 9..."
Write-Host "===============================================================================" 
$envPath = "C:\bon\robot9\env1\Scripts\Activate.ps1"
if (Test-Path $envPath) {
    & $envPath
} elseif (Test-Path "C:\bon\robot9\env1\Scripts\activate.bat") {
    cmd /c "C:\bon\robot9\env1\Scripts\activate.bat"
} else {
    Write-Host "[ERREUR] Environnement virtuel introuvable."
    Pause
    exit
}

# Navigation vers le dossier du robot
Write-Host "===============================================================================" 
Write-Host "Navigation vers le répertoire de Robot 9..."
Write-Host "===============================================================================" 
Set-Location "C:\bon\robot9"

# Exécuter le script Python
Write-Host "===============================================================================" 
Write-Host "Exécution du script de Robot 9..."
Write-Host "===============================================================================" 
python __post_in_groups__.py

# Fin
Write-Host "===============================================================================" 
Write-Host "Le processus de Robot 9 est terminé."
Write-Host "===============================================================================" 
Pause
