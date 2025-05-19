# Chemin vers le fichier de configuration de XMRig
$configPath = "C:\cpu_monero\config.json"
$logPath = "C:\cpu_monero\cpu_adjustment.log"

# Fonction pour écrire des logs
function Write-Log {
    param (
        [string]$Message
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "$timestamp - $Message"
    Add-Content -Path $logPath -Value $logMessage
    Write-Host $logMessage
}

# Fonction pour ajuster l'utilisation du CPU
function Adjust-CPUUsage {
    param (
        [int]$MaxUsagePercent
    )

    try {
        # Charger le fichier de configuration
        $config = Get-Content -Path $configPath -ErrorAction Stop | ConvertFrom-Json -ErrorAction Stop

        # Ajuster le paramètre max-threads-hint
        $config.cpu."max-threads-hint" = $MaxUsagePercent

        # Sauvegarder le fichier de configuration
        $config | ConvertTo-Json -Depth 10 | Set-Content -Path $configPath -ErrorAction Stop

        Write-Log "CPU usage adjusted to $MaxUsagePercent%"
    } catch {
        Write-Log "Failed to adjust CPU usage: $_"
    }
}

# Fonction pour redémarrer XMRig
function Restart-XMRig {
    try {
        # Tuer le processus XMRig s'il est en cours d'exécution
        $xmrigProcess = Get-Process -Name "xmrig" -ErrorAction SilentlyContinue
        if ($xmrigProcess) {
            Stop-Process -Name "xmrig" -Force -ErrorAction Stop
            Write-Log "XMRig process stopped."
        }

        # Redémarrer XMRig
        Start-Process -FilePath "C:\cpu_monero\xmrig.exe" -ArgumentList "--config=C:\cpu_monero\config.json" -NoNewWindow -ErrorAction Stop
        Write-Log "XMRig restarted with new configuration."
    } catch {
        Write-Log "Failed to restart XMRig: $_"
    }
}

# Fonction pour obtenir l'utilisation du CPU
function Get-CPUUsage {
    try {
        $cpuUsage = (Get-Counter '\Processor(_Total)\% Processor Time' -ErrorAction Stop).CounterSamples.CookedValue
        return [math]::Round($cpuUsage, 2)
    } catch {
        Write-Log "Failed to get CPU usage: $_"
        return $null
    }
}

# Boucle principale pour surveiller l'utilisation du CPU
Write-Log "Starting CPU usage adjustment script..."
while ($true) {
    # Obtenir l'utilisation actuelle du CPU
    $cpuUsage = Get-CPUUsage

    if ($cpuUsage -ne $null) {
        # Ajuster l'utilisation du CPU en fonction de la charge
        if ($cpuUsage -lt 30) {
            Adjust-CPUUsage -MaxUsagePercent 80  # Utilisation maximale si le CPU est peu utilisé
            Restart-XMRig
        } elseif ($cpuUsage -ge 30 -and $cpuUsage -lt 70) {
            Adjust-CPUUsage -MaxUsagePercent 50  # Utilisation moyenne
            Restart-XMRig
        } else {
            Adjust-CPUUsage -MaxUsagePercent 30  # Utilisation minimale si le CPU est très utilisé
            Restart-XMRig
        }
    }

    # Attendre 10 secondes avant de vérifier à nouveau
    Start-Sleep -Seconds 10
}