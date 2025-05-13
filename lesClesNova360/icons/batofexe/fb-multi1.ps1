# Forcer l'encodage UTF-8
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()

# Définir les couleurs de la console : texte blanc sur fond bleu
$host.UI.RawUI.BackgroundColor = "DarkBlue"
$host.UI.RawUI.ForegroundColor = "White"
Clear-Host

# Définir le titre de la fenêtre
$host.UI.RawUI.WindowTitle = "AI FB ROBOT PRO - Robot 1"

# Redimensionner la fenêtre de la console
$size = $host.UI.RawUI.WindowSize
$size.Width = 60
$size.Height = 15
$host.UI.RawUI.WindowSize = $size
$host.UI.RawUI.BufferSize = $size

# Afficher la bannière
Write-Host "===============================================================================" 
Write-Host "                             AI FB ROBOT PRO                                   "
Write-Host "===============================================================================" 
Write-Host "                  Démarrage de Robot 1 en cours...                            "
Write-Host "===============================================================================" 
Write-Host ""

# Vérifier si le répertoire de Robot 1 existe
$robot1Dir = "C:\bon\robot1"
if (-Not (Test-Path $robot1Dir)) {
    Write-Host "Le répertoire de Robot 1 est introuvable !"
    Write-Host "===============================================================================" 
    Pause
    exit
}

# Activer l'environnement virtuel de Robot 1
Write-Host "===============================================================================" 
Write-Host "Activation de l'environnement pour Robot 1..."
Write-Host "===============================================================================" 
Set-Location "C:\bon\robot1\env1\Scripts"
.\Activate.ps1

# Naviguer vers le répertoire de Robot 1
Write-Host "===============================================================================" 
Write-Host "Navigation vers le répertoire de Robot 1..."
Write-Host "===============================================================================" 
Set-Location $robot1Dir

# Exécuter le script Python de Robot 1
Write-Host "===============================================================================" 
Write-Host "Exécution du script de Robot 1..."
Write-Host "===============================================================================" 
python __post_in_groupsx__.py

# Afficher un message de fin
Write-Host "===============================================================================" 
Write-Host "Le processus de Robot 1 est terminé."
Write-Host "===============================================================================" 
Pause
