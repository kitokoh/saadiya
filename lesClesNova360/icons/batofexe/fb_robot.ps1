# Configuration
$fichier = "C:\bon\python.txt"
Write-Host "[INFO] Chemin du fichier à modifier : $fichier"

# Vérifier si le fichier existe
Write-Host "[INFO] Vérification de l'existence du fichier..."
if (-Not (Test-Path $fichier)) {
    Write-Host "[ERREUR] Le fichier $fichier n'existe pas."
    exit
}
Write-Host "[INFO] Fichier trouvé."

# Lire la première ligne
Write-Host "[INFO] Lecture de la première ligne du fichier..."
$premiere_ligne = Get-Content -Path $fichier -TotalCount 1

Write-Host "[INFO] Première ligne lue : $premiere_ligne"

# Vérifier les conditions (début et fin de ligne)
if ($premiere_ligne.StartsWith("A1a9003") -and $premiere_ligne.EndsWith("212")) {
    Write-Host "[INFO] Conditions remplies. Préparation de la modification..."

    # Remplacer A1a9003 par A1a9333
    $nouvelle_ligne = $premiere_ligne -replace "^A1a9003", "A1a9333"
    Write-Host "[INFO] Nouvelle ligne après modification : $nouvelle_ligne"

    # Lire tout le contenu du fichier
    $reste = Get-Content -Path $fichier | Select-Object -Skip 1

    # Créer un nouveau contenu
    $nouveau_contenu = @()
    $nouveau_contenu += $nouvelle_ligne
    $nouveau_contenu += $reste

    # Écrire dans le fichier original
    $nouveau_contenu | Set-Content -Path $fichier
    Write-Host "[SUCCES] Modification réussie dans $fichier."
} else {
    Write-Host "[INFO] Conditions non remplies. Aucune modification n'a été effectuée."
}

Write-Host "[INFO] Fin du script."
Pause
