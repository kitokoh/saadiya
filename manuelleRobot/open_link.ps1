# Chemin vers le fichier JSON
$jsonPath = "C:\bon\robot1\data.json"

# Lire le fichier JSON
$jsonContent = Get-Content -Raw -Path $jsonPath | ConvertFrom-Json

# Extraire les liens du JSON
$links = $jsonContent.groups

# Ouvrir les liens par groupes de 10
$groupSize = 10
$totalLinks = $links.Count
$numGroups = [math]::Ceiling($totalLinks / $groupSize)

for ($i = 0; $i -lt $numGroups; $i++) {
    $startIdx = $i * $groupSize
    $endIdx = [math]::Min(($startIdx + $groupSize - 1), ($totalLinks - 1))

    Write-Host "Opening group $i..."

    for ($j = $startIdx; $j -le $endIdx; $j++) {
        $link = $links[$j]
        # Spécifier le chemin vers Google Chrome
        $chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
        Start-Process $chromePath $link
    }

    # Mettre en pause le script
    Write-Host "Press any key to continue..."
    [void][System.Console]::ReadKey($true)
}

Write-Host "All links have been opened."





