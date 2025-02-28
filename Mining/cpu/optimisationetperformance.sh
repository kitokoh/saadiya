#!/bin/bash
echo "Optimisation du processeur et des performances..."
echo.

# Vérifier si le script est exécuté en tant que root
if [ "$EUID" -ne 0 ]; then
    echo "Ce script doit être exécuté en tant que root."
    exit 1
fi

# Détection de l'OS
echo "Détection du système d'exploitation..."
if grep -q "Linux" /etc/os-release; then
    echo "Système détecté : Linux."
    LINUX_OPTIMIZATION
elif [[ "$(uname)" == "Darwin" ]]; then
    echo "Système détecté : macOS."
    MACOS_OPTIMIZATION
else
    echo "Système non reconnu ou non pris en charge."
    exit 1
fi

# Fonction pour enregistrer les logs
LOG_FILE="/var/log/optimisation_performance.log"
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

LINUX_OPTIMIZATION() {
    log "Début des optimisations pour Linux."

    # Activer le mode Haute Performance
    log "Activation du mode Haute Performance..."
    sudo cpupower frequency-set -g performance
    if [ $? -eq 0 ]; then
        log "Mode Haute Performance activé avec succès."
    else
        log "Échec de l'activation du mode Haute Performance."
    fi

    # Désactiver l'économie d'énergie CPU
    log "Désactivation de l'économie d'énergie du processeur..."
    echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
    if [ $? -eq 0 ]; then
        log "Économie d'énergie du processeur désactivée avec succès."
    else
        log "Échec de la désactivation de l'économie d'énergie du processeur."
    fi

    # Désactiver l'Hyper-Threading (Intel)
    log "Désactivation de l'Hyper-Threading (Intel)..."
    for cpu in /sys/devices/system/cpu/cpu*/topology/thread_siblings_list; do
        echo 0 | sudo tee $cpu
    done
    if [ $? -eq 0 ]; then
        log "Hyper-Threading désactivé avec succès."
    else
        log "Échec de la désactivation de l'Hyper-Threading."
    fi

    # Activer le SMT (AMD)
    log "Activation du SMT (AMD)..."
    echo on | sudo tee /sys/devices/system/cpu/smt/control
    if [ $? -eq 0 ]; then
        log "SMT activé avec succès."
    else
        log "Échec de l'activation du SMT."
    fi

    # Désactiver la mise en veille automatique
    log "Désactivation de la mise en veille automatique..."
    sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
    if [ $? -eq 0 ]; then
        log "Mise en veille automatique désactivée avec succès."
    else
        log "Échec de la désactivation de la mise en veille automatique."
    fi

    # Nettoyer les fichiers temporaires
    log "Nettoyage des fichiers temporaires..."
    sudo rm -rf /tmp/*
    if [ $? -eq 0 ]; then
        log "Fichiers temporaires nettoyés avec succès."
    else
        log "Échec du nettoyage des fichiers temporaires."
    fi

    # Redémarrer le système
    log "Redémarrage dans 10 secondes..."
    sleep 10
    sudo reboot
}

MACOS_OPTIMIZATION() {
    log "Début des optimisations pour macOS."

    # Détection du type de processeur (Intel ou Apple Silicon)
    PROCESSOR_TYPE=$(sysctl -n machdep.cpu.brand_string)
    if [[ "$PROCESSOR_TYPE" == *"Apple"* ]]; then
        log "Processeur Apple Silicon détecté."
    else
        log "Processeur Intel détecté."
    fi

    # Désactiver la mise en veille automatique
    log "Désactivation de la mise en veille automatique..."
    sudo systemsetup -setcomputersleep Never
    if [ $? -eq 0 ]; then
        log "Mise en veille automatique désactivée avec succès."
    else
        log "Échec de la désactivation de la mise en veille automatique."
    fi

    # Activer le mode Haute Performance
    log "Activation du mode Haute Performance..."
    sudo pmset -a hibernatemode 0
    sudo pmset -a autopoweroff 0
    sudo pmset -a standby 0
    if [ $? -eq 0 ]; then
        log "Mode Haute Performance activé avec succès."
    else
        log "Échec de l'activation du mode Haute Performance."
    fi

    # Désactiver l'économie d'énergie
    log "Désactivation de l'économie d'énergie..."
    sudo pmset -a displaysleep 0
    sudo pmset -a disksleep 0
    if [ $? -eq 0 ]; then
        log "Économie d'énergie désactivée avec succès."
    else
        log "Échec de la désactivation de l'économie d'énergie."
    fi

    # Optimisations spécifiques pour Apple Silicon
    if [[ "$PROCESSOR_TYPE" == *"Apple"* ]]; then
        log "Application des optimisations spécifiques pour Apple Silicon..."
        # Désactiver la gestion dynamique de l'énergie (si applicable)
        sudo pmset -a lowpowermode 0
        if [ $? -eq 0 ]; then
            log "Gestion dynamique de l'énergie désactivée avec succès."
        else
            log "Échec de la désactivation de la gestion dynamique de l'énergie."
        fi
    fi

    # Nettoyer les fichiers temporaires
    log "Nettoyage des fichiers temporaires..."
    sudo rm -rf /private/var/folders/*
    sudo rm -rf /private/var/tmp/*
    if [ $? -eq 0 ]; then
        log "Fichiers temporaires nettoyés avec succès."
    else
        log "Échec du nettoyage des fichiers temporaires."
    fi

    # Redémarrer le système
    log "Redémarrage dans 10 secondes..."
    sleep 10
    sudo shutdown -r now
}