import os
import sys
import requests
import tempfile
import subprocess
import json
import time
import ctypes
import shutil
import hashlib

# ----------------- Configuration -----------------
APP_INFO_FILE = os.path.join(os.getenv('APPDATA'), 'saadiya', 'resources', 'app_info.json')
# APP_INFO_FILE = "app_info.json"
VERSION_URL = "https://leopardo-ai.web.app/version.json"
LOG_FILE = os.path.join(tempfile.gettempdir(), "leopardo_update.log")
MAX_RETRIES = 3
RETRY_DELAY = 2
INSTALL_DIR = r"C:\Program Files\Leopardo AI"
APP_EXE = "main.exe"

# ----------------- Logging -----------------
def setup_logging():
    def log(message, level="INFO"):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        full_msg = f"{timestamp} [{level}] {message}"
        
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(full_msg + '\n')
        
        print(full_msg)
    
    return log

log = setup_logging()

# ----------------- Core Functions -----------------
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def elevate_privileges():
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit(0)
    except Exception as e:
        log(f"Failed to elevate privileges: {str(e)}", "ERROR")
        sys.exit(1)

def load_app_info():
    try:
        with open(APP_INFO_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        log(f"Error loading config: {str(e)}", "ERROR")
        return None

def fetch_update_info():
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(VERSION_URL, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if not all(k in data for k in ['latest_version', 'url']):
                raise ValueError("Missing required fields")
                
            return data
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            log(f"Attempt {attempt + 1} failed: {str(e)}", "WARNING")
    
    return None

def download_file(url, dest_path):
    try:
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            downloaded = 0
            
            with open(dest_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    progress = (downloaded / total_size) * 100 if total_size > 0 else 0
                    print(f"\rDownloading: {progress:.1f}%", end='')
            
            print("\nDownload complete")
            return True
    except Exception as e:
        log(f"Download failed: {str(e)}", "ERROR")
        return False

def verify_file_hash(file_path, expected_hash):
    if not expected_hash or not os.path.exists(file_path):
        return False
    
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    
    return sha256.hexdigest().lower() == expected_hash.lower()

def create_backup(app_info):
    backup_dir = os.path.join(tempfile.gettempdir(), "LeopardoBackup")
    try:
        os.makedirs(backup_dir, exist_ok=True)
        backup_path = os.path.join(backup_dir, APP_EXE)
        
        if os.path.exists(app_info['exe_path']):
            shutil.copy2(app_info['exe_path'], backup_path)
            return backup_path
    except Exception as e:
        log(f"Backup failed: {str(e)}", "ERROR")
    return None

def create_update_script(temp_exe_path, app_info):
    bat_content = f"""@echo off
chcp 65001 >nul
echo === Leopardo AI Updater ===
echo Current: {app_info['current_version']} -> New: {app_info['new_version']}

:: Close running app
taskkill /f /im "{APP_EXE}" >nul 2>&1
timeout /t 3 >nul

:: Create install dir if missing
if not exist "{INSTALL_DIR}" (
    mkdir "{INSTALL_DIR}"
)

:: Replace executable
echo Installing new version...
move /Y "{temp_exe_path}" "{app_info['exe_path']}" >nul

:: Verify
if not exist "{app_info['exe_path']}" (
    echo ! Installation failed
    pause
    exit /b 1
)

:: Launch
start "" "{app_info['exe_path']}"

:: Cleanup
del "%~f0" >nul
"""

    script_path = os.path.join(tempfile.gettempdir(), "leopardo_update.bat")
    try:
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(bat_content)
        return script_path
    except Exception as e:
        log(f"Script creation failed: {str(e)}", "ERROR")
        return None

# ----------------- Main Update Process -----------------
def perform_update():
    if not is_admin():
        log("Elevating privileges...")
        elevate_privileges()
        return

    log("=== Starting update process ===")
    
    # Load current config
    app_info = load_app_info()
    if not app_info:
        log("Cannot load application info", "ERROR")
        return

    # Get update info
    update_info = fetch_update_info()
    if not update_info:
        log("Cannot fetch update info", "ERROR")
        return

    current_version = app_info.get('current_version', '0.0.0')
    new_version = update_info['latest_version']
    
    log(f"Current version: {current_version}")
    log(f"Available version: {new_version}")
    log(f"Release notes: {update_info.get('release_notes', 'No notes')}")

    # Version comparison
    if tuple(map(int, current_version.split('.'))) >= tuple(map(int, new_version.split('.'))):
        log("Already up to date")
        return

    # Download new version
    temp_exe = os.path.join(tempfile.gettempdir(), "leopardo_new.exe")
    log(f"Downloading from: {update_info['url']}")
    if not download_file(update_info['url'], temp_exe):
        return

    # Verify file hash if available
    if 'sha256' in update_info:
        log("Verifying file hash...")
        if not verify_file_hash(temp_exe, update_info['sha256']):
            log("File verification failed! Possible corrupted download.", "ERROR")
            os.remove(temp_exe)
            return
        log("File verification successful")

    # Create backup
    backup_path = create_backup(app_info)
    if backup_path:
        log(f"Backup created at: {backup_path}")

    # Prepare update script
    app_info['new_version'] = new_version
    script_path = create_update_script(temp_exe, app_info)
    if not script_path:
        return

    # Update version in config
    app_info['current_version'] = new_version
    try:
        with open(APP_INFO_FILE, 'w', encoding='utf-8') as f:
            json.dump(app_info, f, indent=4)
    except Exception as e:
        log(f"Failed to save config: {str(e)}", "WARNING")

    # Execute update
    log("Launching update...")
    try:
        subprocess.Popen([script_path], shell=True)
        log("Update started, closing current instance...")
        time.sleep(2)
        sys.exit(0)
    except Exception as e:
        log(f"Failed to launch updater: {str(e)}", "ERROR")

if __name__ == "__main__":
    try:
        perform_update()
    except Exception as e:
        log(f"Critical error: {str(e)}", "CRITICAL")
    finally:
        log("=== Process finished ===")