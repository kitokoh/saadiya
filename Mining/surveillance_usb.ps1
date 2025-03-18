# Configuration
$sourceFolder = "C:\Chemin\Vers\Votre\Dossier"  # Dossier à copier
$logDir = "C:\Chemin\Vers\Logs"
$logFile = Join-Path -Path $logDir -ChildPath ("USB_Copy_Log_" + (Get-Date -Format "yyyy-MM-dd") + ".txt")
$requiredSpaceGB = 1  # Espace disque requis (Go)

# Créer le dossier de logs s'il n'existe pas
if (!(Test-Path -Path $logDir)) { New-Item -Path $logDir -ItemType Directory }

# Fonction pour écrire dans le fichier journal
function Write-Log {
    param ([string]$message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "$timestamp - $message"
    Add-Content -Path $logFile -Value $logMessage
    Write-Host $logMessage  # Affichage en console
}

# Vérification de l'espace disque
function Check-DiskSpace {
    param ([string]$driveLetter, [double]$requiredSpaceGB)
    try {
        $drive = Get-PSDrive -Name $driveLetter -ErrorAction Stop
        $freeSpaceGB = [math]::Round($drive.Free / 1GB, 2)
        if ($freeSpaceGB -ge $requiredSpaceGB) {
            return $true
        } else {
            Write-Log "⚠️ Espace insuffisant sur $driveLetter : $freeSpaceGB Go libre, requis : $requiredSpaceGB Go."
            return $false
        }
    } catch {
        Write-Log "❌ Erreur : Impossible d’accéder à $driveLetter."
        return $false
    }
}

# Fonction de copie robuste avec Robocopy
function Copy-FolderToUSB {
    param ([string]$usbDrive)
    $destinationFolder = Join-Path -Path $usbDrive -ChildPath (Split-Path -Leaf $sourceFolder)
    
    if (Test-Path -Path $sourceFolder) {
        if (-not (Test-Path -Path $destinationFolder)) {
            Write-Log "🔄 Copie en cours de $sourceFolder vers $destinationFolder..."
            Start-Process -NoNewWindow -FilePath "robocopy.exe" -ArgumentList "`"$sourceFolder`" `"$destinationFolder`" /E /MT:8 /R:2 /W:2 /LOG+:`"$logFile`"" -Wait
            Write-Log "✅ Copie terminée avec succès."
        } else {
            Write-Log "ℹ️ Le dossier existe déjà : $destinationFolder."
        }
    } else {
        Write-Log "❌ Le dossier source n'existe pas : $sourceFolder."
    }
}

# Fonction principale
function Monitor-USB {
    Write-Log "🔍 Surveillance des clés USB en cours..."
    $previousDrives = @()

    while ($true) {
        $currentDrives = Get-WmiObject -Query "SELECT * FROM Win32_Volume WHERE DriveType=2" | Select-Object -ExpandProperty DriveLetter
        $newDrives = $currentDrives | Where-Object { $previousDrives -notcontains $_ }

        if ($newDrives) {
            foreach ($drive in $newDrives) {
                Write-Log "🔹 Clé USB détectée : $drive"
                if (Check-DiskSpace -driveLetter $drive -requiredSpaceGB $requiredSpaceGB) {
                    Copy-FolderToUSB -usbDrive $drive
                }
            }
        }

        $previousDrives = $currentDrives
        Start-Sleep -Seconds 5
    }
}

# Lancer la surveillance
Monitor-USB
