import sys
import os
import platform
import webbrowser
import requests
import zipfile
import shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton,
    QProgressBar, QLabel, QMessageBox, QHBoxLayout, QFrame,
    QCheckBox, QGroupBox, QTabWidget, QTextEdit, QComboBox,
    QStackedWidget, QSizePolicy, QSpacerItem, QFileDialog,
    QGraphicsOpacityEffect, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import (
    Qt, QThread, pyqtSignal, QSize, QTimer, QPropertyAnimation,
    QEasingCurve, QPoint, QParallelAnimationGroup, QSequentialAnimationGroup
)
from PyQt5.QtGui import (
    QFont, QPixmap, QIcon, QColor, QPalette, QMovie, QLinearGradient,
    QPainter, QBrush, QRadialGradient
)
from qt_material import apply_stylesheet
from urllib.request import urlopen
from urllib.error import URLError
import ctypes
import winreg
from packaging import version
import subprocess
class InstallerThread(QThread):
    progress_signal = pyqtSignal(int, str)
    finished_signal = pyqtSignal(bool, str)
    log_signal = pyqtSignal(str)
    dependency_signal = pyqtSignal(str, bool, str)
    download_progress = pyqtSignal(str, int, int)

    def __init__(self, options):
        super().__init__()
        self._is_running = True
        self.options = options
        self.install_path = options.get('install_path', os.path.expanduser("~"))
        self.temp_dir = os.path.join(self.install_path, "mayan-temp")

        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def run(self):
        try:
            self.log_signal.emit("=== Début du processus d'installation ===")

            steps = [
                ("Vérification des prérequis...", 5),
                ("Installation des dépendances système...", 15),
                ("Téléchargement des composants...", 25),
                ("Création de l'environnement virtuel...", 35),
                ("Installation de Mayan EDMS...", 55),
                ("Configuration de la base de données...", 75),
                ("Création des répertoires nécessaires...", 85),
                ("Finalisation de l'installation...", 95),
                ("Installation terminée", 100)
            ]

            for step, progress in steps:
                if not self._is_running:
                    self.finished_signal.emit(False, "Installation annulée par l'utilisateur")
                    return

                self.progress_signal.emit(progress, step)
                self.log_signal.emit(f"\n▶ {step}")

                try:
                    if "prérequis" in step:
                        self.check_prerequisites()
                    elif "dépendances système" in step:
                        self.install_system_dependencies()
                    elif "Téléchargement" in step:
                        self.download_components()
                    elif "environnement virtuel" in step:
                        self.create_virtualenv()
                    elif "Mayan EDMS" in step:
                        self.install_mayan()
                    elif "base de données" in step:
                        self.setup_database()
                    elif "répertoires" in step:
                        self.create_directories()
                    elif "Finalisation" in step:
                        self.finalize_installation()
                except Exception as e:
                    self.log_signal.emit(f"⚠ Erreur: {str(e)}")
                    raise

                self.msleep(300)

            self.finished_signal.emit(True, "Installation terminée avec succès!")
            self.log_signal.emit("\n✅ Installation terminée avec succès!")

        except Exception as e:
            self.log_signal.emit(f"\n❌ ERREUR CRITIQUE: {str(e)}")
            self.finished_signal.emit(False, f"Erreur lors de l'installation: {str(e)}")
        finally:
            self.cleanup_temp_files()

    def check_prerequisites(self):
        checks = [
            ("Python 3.7+", self.check_python_version, ""),
            ("Pip", self.check_pip, ""),
            ("Connexion Internet", self.check_internet, ""),
            ("Espace disque (2GB min)", self.check_disk_space, ""),
            ("Outils de compilation", self.check_compiler_tools, "")
        ]

        all_ok = True
        for name, check_func, extra in checks:
            try:
                result, msg = check_func()
                self.dependency_signal.emit(name, result, msg)
                if not result:
                    all_ok = False
            except Exception as e:
                self.dependency_signal.emit(name, False, f"Erreur: {str(e)}")
                all_ok = False

        if not all_ok:
            raise Exception("Certains prérequis ne sont pas satisfaits")

    def check_python_version(self):
        python_version = platform.python_version_tuple()
        v = f"{python_version[0]}.{python_version[1]}"
        ok = int(python_version[0]) >= 3 and (int(python_version[0]) > 3 or int(python_version[1]) >= 7)
        return ok, f"Version détectée: {platform.python_version()}"

    def check_pip(self):
        try:
            pip_version = subprocess.check_output(["pip", "--version"]).decode().split()[1]
            return True, f"Version: {pip_version}"
        except:
            return False, "Pip non trouvé"

    def check_internet(self):
        try:
            urlopen('https://pypi.org', timeout=3)
            return True, "Connecté"
        except URLError:
            return False, "Pas de connexion"

    def check_disk_space(self):
        try:
            if platform.system() == "Windows":
                free_bytes = ctypes.c_ulonglong(0)
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                    ctypes.c_wchar_p(os.path.splitdrive(self.install_path)[0]),
                    None, None, ctypes.pointer(free_bytes))
                gb = free_bytes.value / (1024**3)
                ok = gb > 2
                return ok, f"{gb:.1f} GB libre(s)"
            else:
                stat = os.statvfs(self.install_path)
                gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
                ok = gb > 2
                return ok, f"{gb:.1f} GB libre(s)"
        except:
            return True, "Non vérifié"

    def check_compiler_tools(self):
        if platform.system() != "Windows":
            return True, "Non requis"

        try:
            # Vérifier Visual Studio Build Tools
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\VisualStudio\14.0")
                winreg.CloseKey(key)
                return True, "Visual Studio 2015+ trouvé"
            except:
                pass

            # Vérifier standalone Build Tools
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\VisualStudio\SxS\VS7")
                version = winreg.QueryValueEx(key, "15.0")[0]
                winreg.CloseKey(key)
                if version:
                    return True, f"Visual Studio {version} trouvé"
            except:
                pass

            return False, "Installez Visual Studio Build Tools"
        except:
            return False, "Outils non trouvés"

    def install_system_dependencies(self):
        if not self.options.get('install_deps', True):
            self.log_signal.emit("Installation des dépendances système désactivée")
            return

        system = platform.system()
        self.log_signal.emit(f"🔧 Système détecté: {system}")

        if system == "Windows":
            self.install_windows_dependencies()
        elif system == "Linux":
            self.install_linux_dependencies()
        elif system == "Darwin":
            self.install_macos_dependencies()

    def install_windows_dependencies(self):
        """Solution robuste pour python-ldap sur Windows"""
        try:
            # Solution 1: Essayer d'installer depuis Gohlke
            python_version = f"{sys.version_info.major}{sys.version_info.minor}"
            wheel_filename = f"python_ldap-3.4.3-cp{python_version}-cp{python_version}-win_amd64.whl"
            wheel_path = os.path.join(self.temp_dir, wheel_filename)

            if not os.path.exists(wheel_path):
                base_url = "https://download.lfd.uci.edu/pythonlibs/z4tqcw5k/"
                url = f"{base_url}{wheel_filename}"
                self.log_signal.emit(f"Téléchargement de {url}...")

                response = requests.get(url, stream=True)
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0

                with open(wheel_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            self.download_progress.emit(wheel_filename, downloaded, total_size)

                self.log_signal.emit("Vérification du wheel...")
                if not zipfile.is_zipfile(wheel_path):
                    raise Exception("Fichier wheel invalide")

            self.log_signal.emit("Installation du wheel python-ldap...")
            subprocess.run([sys.executable, "-m", "pip", "install", wheel_path], check=True)

        except Exception as e:
            self.log_signal.emit(f"⚠ Échec méthode 1: {str(e)}")

            # Solution 2: Installer sans LDAP
            self.log_signal.emit("Tentative d'installation sans LDAP...")
            self.options['no_ldap'] = True

    def install_linux_dependencies(self):
        if os.path.exists("/etc/debian_version"):
            self.log_signal.emit("Distribution Debian/Ubuntu détectée")
            deps = [
                "python3-dev", "python3-venv", "libjpeg-dev",
                "zlib1g-dev", "libpq-dev", "libffi-dev",
                "build-essential", "ghostscript", "libldap2-dev",
                "libsasl2-dev", "libssl-dev", "libxml2-dev",
                "libxslt1-dev", "libmagic1", "poppler-utils"
            ]
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y"] + deps, check=True)
        elif os.path.exists("/etc/redhat-release"):
            self.log_signal.emit("Distribution RHEL/CentOS/Fedora détectée")
            deps = [
                "python3-devel", "libjpeg-turbo-devel",
                "zlib-devel", "postgresql-devel",
                "libffi-devel", "gcc", "ghostscript",
                "openldap-devel", "cyrus-sasl-devel",
                "openssl-devel", "libxml2-devel",
                "libxslt-devel", "file-devel",
                "poppler-utils"
            ]
            subprocess.run(["sudo", "dnf", "install", "-y"] + deps, check=True)

    def install_macos_dependencies(self):
        self.log_signal.emit("macOS détecté - installation via Homebrew")
        deps = [
            "jpeg", "libpq", "ghostscript", "openldap",
            "cyrus-sasl", "openssl", "libxml2",
            "libxslt", "libmagic", "poppler"
        ]
        subprocess.run(["brew", "install"] + deps, check=True)

    def download_components(self):
        if self.options.get('download_sample_docs', False):
            self.download_with_progress(
                "https://github.com/mayan-edms/mayan-edms-sample-documents/archive/master.zip",
                "mayan-sample-docs.zip",
                "Documents exemples"
            )

            zip_path = os.path.join(self.temp_dir, "mayan-sample-docs.zip")
            extract_path = os.path.join(self.install_path, "mayan-data")

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)

    def download_with_progress(self, url, filename, description):
        filepath = os.path.join(self.temp_dir, filename)
        self.log_signal.emit(f"Téléchargement {description} depuis {url}...")

        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    self.download_progress.emit(filename, downloaded, total_size)

        self.log_signal.emit(f"✅ {description} téléchargé avec succès")
        return filepath

    def create_virtualenv(self):
        if not self.options.get('create_venv', True):
            self.log_signal.emit("Création d'environnement virtuel désactivée")
            return

        venv_dir = os.path.join(self.install_path, "mayan-venv")
        self.log_signal.emit(f"🌍 Création de l'environnement virtuel dans {venv_dir}")

        if not os.path.exists(venv_dir):
            subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
            self.log_signal.emit("✅ Environnement virtuel créé avec succès")

    def install_mayan(self):
        venv_dir = os.path.join(self.install_path, "mayan-venv")
        pip_path = os.path.join(venv_dir, "bin", "pip") if platform.system() != "Windows" else os.path.join(venv_dir, "Scripts", "pip.exe")

        self.log_signal.emit("⬆ Mise à jour de pip...")
        subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)

        self.log_signal.emit("📦 Installation de Mayan EDMS...")
        if self.options.get('no_ldap', False):
            subprocess.run([pip_path, "install", "mayan-edms", "--global-option=build_ext", "--global-option=--disable-ldap"], check=True)
            self.log_signal.emit("✅ Mayan EDMS installé sans support LDAP")
        else:
            try:
                subprocess.run([pip_path, "install", "mayan-edms"], check=True)
                self.log_signal.emit("✅ Mayan EDMS installé avec succès")
            except subprocess.CalledProcessError:
                self.log_signal.emit("⚠ Tentative alternative sans LDAP...")
                subprocess.run([pip_path, "install", "mayan-edms", "--global-option=build_ext", "--global-option=--disable-ldap"], check=True)
                self.log_signal.emit("✅ Mayan EDMS installé sans support LDAP")

    def setup_database(self):
        venv_dir = os.path.join(self.install_path, "mayan-venv")
        mayan_path = os.path.join(venv_dir, "bin", "mayan-edms.py") if platform.system() != "Windows" else os.path.join(venv_dir, "Scripts", "mayan-edms.exe")

        data_dir = os.path.join(self.install_path, "mayan-data")
        self.log_signal.emit(f"🗄 Configuration dans le répertoire: {data_dir}")

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            self.log_signal.emit("📂 Répertoire de données créé")

        self.log_signal.emit("💾 Initialisation de la base de données...")
        subprocess.run([mayan_path, "initialsetup", "--no-dependencies"], cwd=data_dir, check=True)
        self.log_signal.emit("✅ Base de données configurée")

    def create_directories(self):
        if not self.options.get('create_data_dir', True):
            return

        data_dir = os.path.join(self.install_path, "mayan-data")
        dirs = ["media", "documents", "settings", "backups", "indexes"]

        for dir_name in dirs:
            dir_path = os.path.join(data_dir, dir_name)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                self.log_signal.emit(f"📂 Répertoire créé: {dir_path}")

    def finalize_installation(self):
        if platform.system() == "Windows":
            self.create_windows_shortcut()

        if self.options.get('create_desktop_icon', True):
            self.create_desktop_icon()

    def create_windows_shortcut(self):
        try:
            import winshell
            from win32com.client import Dispatch

            desktop = winshell.desktop()
            venv_dir = os.path.join(self.install_path, "mayan-venv")
            mayan_path = os.path.join(venv_dir, "Scripts", "mayan-edms.exe")
            data_dir = os.path.join(self.install_path, "mayan-data")

            path = os.path.join(desktop, "Mayan EDMS.lnk")
            target = mayan_path
            wDir = data_dir
            icon = os.path.join(venv_dir, "Lib", "site-packages", "mayan", "static", "mayan", "img", "logo.png")

            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = wDir
            shortcut.Arguments = "runserver"
            shortcut.IconLocation = icon
            shortcut.save()

            self.log_signal.emit("📝 Raccourci créé sur le bureau")
        except Exception as e:
            self.log_signal.emit(f"⚠ Impossible de créer le raccourci: {str(e)}")

    def create_desktop_icon(self):
        """Crée une icône de bureau personnalisée"""
        try:
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            icon_path = os.path.join(self.temp_dir, "mayan_icon.ico")

            # Créer une icône temporaire
            self.generate_icon_file(icon_path)

            # Créer un fichier .desktop (Linux)
            if platform.system() == "Linux":
                desktop_file = os.path.join(desktop_path, "mayan-edms.desktop")
                with open(desktop_file, 'w') as f:
                    f.write(f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Mayan EDMS
Comment=Système de gestion de documents
Exec={os.path.join(self.install_path, "mayan-venv", "bin", "mayan-edms.py")} runserver
Icon={icon_path}
Terminal=true
Categories=Office;""")
                os.chmod(desktop_file, 0o755)
                self.log_signal.emit("🖥 Icône de bureau créée (Linux)")

        except Exception as e:
            self.log_signal.emit(f"⚠ Impossible de créer l'icône de bureau: {str(e)}")

    def generate_icon_file(self, output_path):
        """Génère un fichier d'icône temporaire"""
        from PIL import Image, ImageDraw
        img = Image.new('RGBA', (256, 256), (0, 168, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.ellipse([(50, 50), (206, 206)], fill=(255, 255, 255, 255))
        img.save(output_path, format='ICO', sizes=[(256, 256)])

    def cleanup_temp_files(self):
        """Nettoie les fichiers temporaires"""
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                self.log_signal.emit("🧹 Fichiers temporaires nettoyés")
        except Exception as e:
            self.log_signal.emit(f"⚠ Erreur nettoyage fichiers temporaires: {str(e)}")

    def stop(self):
        self._is_running = False
        self.quit()

class AnimatedButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setEasingCurve(QEasingCurve.OutQuad)
        self._animation.setDuration(200)

        self._shadow = QGraphicsDropShadowEffect()
        self._shadow.setBlurRadius(10)
        self._shadow.setColor(QColor(0, 0, 0, 150))
        self._shadow.setOffset(0, 3)
        self.setGraphicsEffect(self._shadow)

        self._shadow_anim = QPropertyAnimation(self._shadow, b"offset")
        self._shadow_anim.setEasingCurve(QEasingCurve.OutQuad)
        self._shadow_anim.setDuration(200)

        self._group = QParallelAnimationGroup()
        self._group.addAnimation(self._animation)
        self._group.addAnimation(self._shadow_anim)

    def enterEvent(self, event):
        self._group.stop()
        self._animation.setStartValue(self.geometry())
        self._animation.setEndValue(self.geometry().adjusted(-5, -3, 5, 3))
        self._shadow_anim.setStartValue(QPoint(0, 3))
        self._shadow_anim.setEndValue(QPoint(0, 6))
        self.log_signal.emit(f"⚠ Erreur nettoyage fichiers temporaires: {str(e)}")

    def stop(self):
        self._is_running = False
        self.quit()

class AnimatedButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setEasingCurve(QEasingCurve.OutQuad)
        self._animation.setDuration(200)

        self._shadow = QGraphicsDropShadowEffect()
        self._shadow.setBlurRadius(10)
        self._shadow.setColor(QColor(0, 0, 0, 150))
        self._shadow.setOffset(0, 3)
        self.setGraphicsEffect(self._shadow)

        self._shadow_anim = QPropertyAnimation(self._shadow, b"offset")
        self._shadow_anim.setEasingCurve(QEasingCurve.OutQuad)
        self._shadow_anim.setDuration(200)

        self._group = QParallelAnimationGroup()
        self._group.addAnimation(self._animation)
        self._group.addAnimation(self._shadow_anim)

    def enterEvent(self, event):
        self._group.stop()
        self._animation.setStartValue(self.geometry())
        self._animation.setEndValue(self.geometry().adjusted(-5, -3, 5, 3))
        self._shadow_anim.setStartValue(QPoint(0, 3))
        self._shadow_anim.setEndValue(QPoint(0, 6))
        self._group.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._group.stop()
        self._animation.setStartValue(self.geometry())
        self._animation.setEndValue(self.geometry().adjusted(5, 3, -5, -3))
        self._shadow_anim.setStartValue(self._shadow.offset())
        self._shadow_anim.setEndValue(QPoint(0, 3))
        self._group.start()
        super().leaveEvent(event)

class GradientLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._gradient = QLinearGradient(0, 0, 0, 1)
        self._gradient.setColorAt(0, QColor("#0097e6"))
        self._gradient.setColorAt(1, QColor("#00a8ff"))
        self._gradient.setCoordinateMode(QLinearGradient.ObjectMode)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        self._gradient.setFinalStop(0, self.height())
        painter.setBrush(QBrush(self._gradient))
        painter.drawRoundedRect(self.rect(), 5, 5)

        painter.setPen(QColor("#ffffff"))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())

class MayanInstaller(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Installateur Mayan EDMS Pro")
        self.setWindowIcon(QIcon(self.create_icon()))
        self.setMinimumSize(1000, 750)

        # Configuration
        self.install_thread = None
        self.install_options = {
            'create_venv': True,
            'install_deps': True,
            'create_data_dir': True,
            'launch_after': True,
            'download_sample_docs': False,
            'create_desktop_icon': True,
            'install_path': os.path.expanduser("~")
        }

        self.setup_ui()
        self.check_python_version()

    def create_icon(self):
        """Crée une icône avec dégradé"""
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QRadialGradient(32, 32, 32)
        gradient.setColorAt(0, QColor("#00a8ff"))
        gradient.setColorAt(1, QColor("#0097e6"))

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, 64, 64)

        painter.setPen(QColor("#ffffff"))
        font = QFont()
        font.setBold(True)
        font.setPointSize(20)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), Qt.AlignCenter, "M")

        painter.end()
        return pixmap

    def check_python_version(self):
        python_version = platform.python_version_tuple()
        if int(python_version[0]) < 3 or (int(python_version[0]) == 3 and int(python_version[1]) < 7):
            self.show_error_message(
                "Version Python incompatible",
                "Mayan EDMS nécessite Python 3.7 ou supérieur.",
                f"Version détectée: {platform.python_version()}"
            )
            sys.exit(1)

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layout principal avec fond dégradé
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_widget.setLayout(main_layout)

        # Barre de titre personnalisée
        self.setup_title_bar(main_layout)

        # Corps principal
        body_widget = QWidget()
        body_widget.setObjectName("mainBody")
        body_layout = QVBoxLayout()
        body_layout.setContentsMargins(30, 30, 30, 30)
        body_layout.setSpacing(20)

        # Widget empilé pour les différentes pages
        self.stacked_widget = QStackedWidget()

        # Création des pages
        self.create_welcome_page()
        self.create_install_page()
        self.create_finish_page()

        body_layout.addWidget(self.stacked_widget)
        body_widget.setLayout(body_layout)

        # AJOUTER LE BODY_WIDGET AU MAIN_LAYOUT
        main_layout.addWidget(body_widget)

        # Pied de page
        self.setup_footer(main_layout)

        # Appliquer le style
        self.apply_styles()

        # Animation d'entrée
        self.setup_entrance_animation()

    def setup_title_bar(self, main_layout):
        title_bar = QWidget()
        title_bar.setFixedHeight(60)
        title_bar.setObjectName("titleBar")
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(15, 0, 15, 0)

        # Logo et titre
        logo = QLabel()
        logo.setPixmap(QPixmap(self.create_icon()).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        title = QLabel("Mayan EDMS Pro Installer")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)

        # Boutons de la barre de titre
        minimize_btn = QPushButton("─")
        minimize_btn.setFixedSize(30, 30)
        minimize_btn.clicked.connect(self.showMinimized)

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.clicked.connect(self.close)

        title_layout.addWidget(logo)
        title_layout.addWidget(title)
        title_layout.addStretch()
        title_layout.addWidget(minimize_btn)
        title_layout.addWidget(close_btn)
        title_bar.setLayout(title_layout)

        main_layout.addWidget(title_bar)

    def create_welcome_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(30)

        # Animation/Image d'en-tête
        header = QLabel()
        header.setAlignment(Qt.AlignCenter)

        # Utiliser un GIF si disponible, sinon une image statique
        if hasattr(QMovie, 'supportedFormats'):
            movie = QMovie()
            movie.setFileName(":/animations/welcome.gif")  # Remplacez par un vrai chemin si disponible
            if movie.isValid():
                header.setMovie(movie)
                movie.start()
            else:
                header.setPixmap(QPixmap(self.create_icon()).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            header.setPixmap(QPixmap(self.create_icon()).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Titre avec effet de dégradé
        title = GradientLabel("Bienvenue dans l'installation de Mayan EDMS")
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setFixedHeight(60)

        # Description
        desc = QLabel("""
        <p style='text-align: center; font-size: 14px;'>
        Mayan EDMS est un système de gestion de documents open-source complet<br>
        avec indexation, classification et contrôle d'accès avancé.
        </p>
        <p style='text-align: center; font-size: 12px; color: #666;'>
        Cet installateur va configurer Mayan EDMS avec toutes ses dépendances<br>
        et options sur votre ordinateur.
        </p>
        """)
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)

        # Bouton Commencer
        start_btn = AnimatedButton("Commencer l'installation")
        start_btn.setIcon(QIcon.fromTheme("system-run"))
        start_btn.setFixedSize(250, 50)
        start_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        # Options avancées
        advanced_btn = QPushButton("Options avancées")
        advanced_btn.setFlat(True)
        advanced_btn.clicked.connect(self.show_advanced_options)

        # Ajout des éléments avec des espaceurs pour centrer verticalement
        layout.addStretch()
        layout.addWidget(header)
        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addStretch()
        layout.addWidget(start_btn, alignment=Qt.AlignCenter)
        layout.addWidget(advanced_btn, alignment=Qt.AlignCenter)
        layout.addStretch()

        page.setLayout(layout)
        self.stacked_widget.addWidget(page)

    def create_install_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # Onglets
        tab_widget = QTabWidget()
        tab_widget.setObjectName("mainTabs")

        # Onglet Installation
        install_tab = self.create_install_tab()
        tab_widget.addTab(install_tab, "Installation")

        # Onglet Prérequis
        prereq_tab = self.create_prereq_tab()
        tab_widget.addTab(prereq_tab, "Prérequis")

        # Onglet Journal
        log_tab = self.create_log_tab()
        tab_widget.addTab(log_tab, "Journal")

        # Onglet Avancé
        advanced_tab = self.create_advanced_tab()
        tab_widget.addTab(advanced_tab, "Avancé")

        layout.addWidget(tab_widget)
        page.setLayout(layout)
        self.stacked_widget.addWidget(page)

    def create_install_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)

        # Options d'installation
        options_group = QGroupBox("Options d'installation")
        options_group.setObjectName("optionsGroup")
        options_layout = QVBoxLayout()

        # Chemin d'installation
        path_layout = QHBoxLayout()
        path_label = QLabel("Répertoire d'installation:")
        self.path_edit = QLabel(self.install_options['install_path'])
        path_btn = QPushButton("Parcourir...")
        path_btn.setFixedWidth(100)
        path_btn.clicked.connect(self.select_install_path)

        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(path_btn)

        # Cases à cocher
        self.venv_check = QCheckBox("Créer un environnement virtuel (recommandé)")
        self.venv_check.setChecked(self.install_options['create_venv'])
        self.venv_check.stateChanged.connect(lambda: self.update_option('create_venv', self.venv_check.isChecked()))

        self.deps_check = QCheckBox("Installer les dépendances système")
        self.deps_check.setChecked(self.install_options['install_deps'])
        self.deps_check.stateChanged.connect(lambda: self.update_option('install_deps', self.deps_check.isChecked()))

        self.data_dir_check = QCheckBox("Créer le répertoire de données")
        self.data_dir_check.setChecked(self.install_options['create_data_dir'])
        self.data_dir_check.stateChanged.connect(lambda: self.update_option('create_data_dir', self.data_dir_check.isChecked()))

        self.launch_check = QCheckBox("Lancer Mayan EDMS après l'installation")
        self.launch_check.setChecked(self.install_options['launch_after'])
        self.launch_check.stateChanged.connect(lambda: self.update_option('launch_after', self.launch_check.isChecked()))

        self.sample_docs_check = QCheckBox("Télécharger des documents exemples")
        self.sample_docs_check.setChecked(self.install_options['download_sample_docs'])
        self.sample_docs_check.stateChanged.connect(lambda: self.update_option('download_sample_docs', self.sample_docs_check.isChecked()))

        self.desktop_icon_check = QCheckBox("Créer une icône sur le bureau")
        self.desktop_icon_check.setChecked(self.install_options['create_desktop_icon'])
        self.desktop_icon_check.stateChanged.connect(lambda: self.update_option('create_desktop_icon', self.desktop_icon_check.isChecked()))

        # Ajout des options
        options_layout.addLayout(path_layout)
        options_layout.addWidget(self.venv_check)
        options_layout.addWidget(self.deps_check)
        options_layout.addWidget(self.data_dir_check)
        options_layout.addWidget(self.launch_check)
        options_layout.addWidget(self.sample_docs_check)
        options_layout.addWidget(self.desktop_icon_check)
        options_group.setLayout(options_layout)

        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setObjectName("mainProgress")

        # Animation de progression
        self.progress_animation = QPropertyAnimation(self.progress_bar, b"value")
        self.progress_animation.setEasingCurve(QEasingCurve.OutQuad)

        # Label d'état
        self.status_label = QLabel("Prêt à installer")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.setObjectName("statusLabel")

        # Boutons
        button_layout = QHBoxLayout()
        self.install_btn = AnimatedButton("Commencer l'installation")
        self.install_btn.setIcon(QIcon.fromTheme("system-run"))
        self.install_btn.clicked.connect(self.start_installation)

        self.cancel_btn = AnimatedButton("Annuler")
        self.cancel_btn.setIcon(QIcon.fromTheme("process-stop"))
        self.cancel_btn.clicked.connect(self.cancel_installation)
        self.cancel_btn.setEnabled(False)

        button_layout.addWidget(self.install_btn)
        button_layout.addWidget(self.cancel_btn)

        # Assemblage onglet installation
        layout.addWidget(options_group)
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        layout.addLayout(button_layout)
        tab.setLayout(layout)

        return tab

    def create_prereq_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        title = QLabel("Vérification des prérequis système")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)
        layout.addSpacing(20)

        # Liste des prérequis
        self.prereq_status = {
            "Python 3.7+": {"label": QLabel("Non vérifié"), "status": False, "desc": QLabel()},
            "Pip": {"label": QLabel("Non vérifié"), "status": False, "desc": QLabel()},
            "Connexion Internet": {"label": QLabel("Non vérifié"), "status": False, "desc": QLabel()},
            "Espace disque (2GB min)": {"label": QLabel("Non vérifié"), "status": False, "desc": QLabel()},
            "Outils de compilation": {"label": QLabel("Non vérifié"), "status": False, "desc": QLabel()}
        }

        for name, data in self.prereq_status.items():
            group = QGroupBox(name)
            group.setObjectName("prereqGroup")
            group_layout = QVBoxLayout()

            status_layout = QHBoxLayout()
            status_layout.addWidget(QLabel("Statut:"))
            status_layout.addWidget(data['label'])
            status_layout.addStretch()

            group_layout.addLayout(status_layout)
            group_layout.addWidget(QLabel("Détails:"))
            group_layout.addWidget(data['desc'])

            group.setLayout(group_layout)
            layout.addWidget(group)

        layout.addStretch()

        # Bouton de vérification
        verify_btn = AnimatedButton("Vérifier à nouveau")
        verify_btn.setIcon(QIcon.fromTheme("view-refresh"))
        verify_btn.clicked.connect(self.check_prerequisites)
        layout.addWidget(verify_btn, alignment=Qt.AlignCenter)

        tab.setLayout(layout)
        return tab

    def create_log_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setObjectName("logOutput")

        # Boutons de contrôle du journal
        control_layout = QHBoxLayout()
        clear_btn = QPushButton("Effacer le journal")
        clear_btn.setIcon(QIcon.fromTheme("edit-clear"))
        clear_btn.clicked.connect(self.log_output.clear)

        save_btn = QPushButton("Enregistrer sous...")
        save_btn.setIcon(QIcon.fromTheme("document-save"))
        save_btn.clicked.connect(self.save_log_file)

        control_layout.addWidget(clear_btn)
        control_layout.addWidget(save_btn)

        layout.addWidget(self.log_output)
        layout.addLayout(control_layout)
        tab.setLayout(layout)
        return tab

    def create_advanced_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)

        title = QLabel("Options avancées")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)
        layout.addSpacing(20)

        # Options avancées
        advanced_group = QGroupBox("Configuration avancée")
        advanced_layout = QVBoxLayout()

        # Sélecteur de thème
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Thème de l'interface:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark Teal", "Dark Amber", "Light Blue", "Light Cyan"])
        self.theme_combo.currentTextChanged.connect(self.change_theme)

        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()

        # Options de débogage
        self.debug_check = QCheckBox("Activer le mode débogage")
        self.debug_check.setChecked(False)

        # Réinitialisation
        reset_btn = QPushButton("Réinitialiser les paramètres")
        reset_btn.setIcon(QIcon.fromTheme("document-revert"))
        reset_btn.clicked.connect(self.reset_settings)

        advanced_layout.addLayout(theme_layout)
        advanced_layout.addWidget(self.debug_check)
        advanced_layout.addWidget(reset_btn)
        advanced_layout.addStretch()
        advanced_group.setLayout(advanced_layout)

        layout.addWidget(advanced_group)
        layout.addStretch()

        tab.setLayout(layout)
        return tab

    def create_finish_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)

        # Animation de succès
        success_anim = QLabel()
        success_anim.setAlignment(Qt.AlignCenter)

        if hasattr(QMovie, 'supportedFormats'):
            movie = QMovie()
            movie.setFileName(":/animations/success.gif")  # Remplacez par un vrai chemin si disponible
            if movie.isValid():
                success_anim.setMovie(movie)
                movie.start()
            else:
                # Fallback à une icône statique
                success_anim.setPixmap(QPixmap(self.create_icon()).scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            success_anim.setPixmap(QPixmap(self.create_icon()).scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Message de succès
        success_msg = QLabel("Installation terminée avec succès!")
        success_font = QFont()
        success_font.setPointSize(18)
        success_font.setBold(True)
        success_msg.setFont(success_font)
        success_msg.setAlignment(Qt.AlignCenter)
        success_msg.setObjectName("successMessage")

        # Instructions
        instructions = QLabel("""
        <p style='text-align: center;'>
        Mayan EDMS a été installé avec succès sur votre système.
        </p>
        <p style='text-align: center; font-family: monospace; background: #f0f0f0; padding: 10px; border-radius: 5px;'>
        Pour démarrer Mayan EDMS:<br>
        <b>~/mayan-venv/bin/mayan-edms.py runserver</b>
        </p>
        <p style='text-align: center;'>
        Puis ouvrez <a href='http://localhost:8000'>http://localhost:8000</a> dans votre navigateur.
        </p>
        """)
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setWordWrap(True)
        instructions.setOpenExternalLinks(True)

        # Boutons
        btn_layout = QHBoxLayout()
        launch_btn = AnimatedButton("Lancer Mayan EDMS maintenant")
        launch_btn.setIcon(QIcon.fromTheme("system-run"))
        launch_btn.clicked.connect(self.launch_mayan)

        close_btn = AnimatedButton("Fermer")
        close_btn.setIcon(QIcon.fromTheme("window-close"))
        close_btn.clicked.connect(self.close)

        btn_layout.addWidget(launch_btn)
        btn_layout.addWidget(close_btn)

        # Ajout des éléments
        layout.addStretch()
        layout.addWidget(success_anim)
        layout.addWidget(success_msg)
        layout.addWidget(instructions)
        layout.addStretch()
        layout.addLayout(btn_layout)

        page.setLayout(layout)
        self.stacked_widget.addWidget(page)

    def setup_footer(self, main_layout):
        footer = QWidget()
        footer.setObjectName("footer")
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(15, 10, 15, 10)

        version = QLabel("Mayan EDMS Installer v2.0")
        version.setObjectName("versionLabel")

        copyright = QLabel("© 2024 Mayan EDMS - Système de Gestion de Documents Open Source")
        copyright.setObjectName("copyrightLabel")

        footer_layout.addWidget(version)
        footer_layout.addStretch()
        footer_layout.addWidget(copyright)
        footer.setLayout(footer_layout)

        main_layout.addWidget(footer)

    def apply_styles(self):
        self.setStyleSheet("""
            /* Fenêtre principale */
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
            }

            /* Barre de titre */
            #titleBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2c3e50, stop:1 #34495e);
                color: white;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }

            #titleBar QLabel {
                color: white;
            }

            #titleBar QPushButton {
                background: transparent;
                color: white;
                font-size: 16px;
                border: none;
                min-width: 30px;
                max-width: 30px;
                min-height: 30px;
                max-height: 30px;
                border-radius: 3px;
            }

            #titleBar QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
            }

            #titleBar QPushButton#closeButton:hover {
                background: #e74c3c;
            }

            /* Corps principal */
            #mainBody {
                background: #f5f7fa;
                border-left: 1px solid #ddd;
                border-right: 1px solid #ddd;
            }

            /* Onglets */
            #mainTabs QTabBar::tab {
                padding: 8px 15px;
                background: #ecf0f1;
                border: 1px solid #ddd;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                margin-right: 2px;
            }

            #mainTabs QTabBar::tab:selected {
                background: white;
                color: #3498db;
                font-weight: bold;
            }

            #mainTabs QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 0 5px 5px 5px;
                background: white;
                margin-top: -1px;
            }

            /* Groupes */
            #optionsGroup, #prereqGroup {
                border: 1px solid #ddd;
                border-radius: 5px;
                background: white;
            }

            #optionsGroup::title, #prereqGroup::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
                color: #3498db;
            }

            /* Barre de progression */
            #mainProgress {
                border: 1px solid #ddd;
                border-radius: 5px;
                text-align: center;
                background: white;
                height: 25px;
            }

            #mainProgress::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0097e6, stop:1 #00a8ff);
                border-radius: 4px;
            }

            /* Journal */
            #logOutput {
                font-family: 'Courier New', monospace;
                font-size: 11px;
                background-color: #1a1a1a;
                color: #e0e0e0;
                border: 1px solid #333;
                border-radius: 3px;
                padding: 5px;
            }

            /* Message de statut */
            #statusLabel {
                font-weight: bold;
                color: #2c3e50;
            }

            /* Message de succès */
            #successMessage {
                color: #27ae60;
            }

            /* Pied de page */
            #footer {
                background: #ecf0f1;
                border-bottom-left-radius: 5px;
                border-bottom-right-radius: 5px;
                border: 1px solid #ddd;
                border-top: none;
            }

            #versionLabel {
                color: #7f8c8d;
                font-size: 10px;
            }

            #copyrightLabel {
                color: #7f8c8d;
                font-size: 10px;
            }

            /* Cases à cocher */
            QCheckBox {
                spacing: 8px;
            }

            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }

            QCheckBox::indicator:unchecked {
                border: 1px solid #bdc3c7;
                background: white;
                border-radius: 3px;
            }

            QCheckBox::indicator:checked {
                border: 1px solid #3498db;
                background: #3498db;
                border-radius: 3px;
                image: url(:/icons/checkmark);
            }
        """)

        # Style des boutons
        btn_style = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0097e6, stop:1 #00a8ff);
                color: white;
                border: none;
                padding: 12px 25px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 150px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00a8ff, stop:1 #0097e6);
            }
            QPushButton:pressed {
                background: #0078b5;
            }
            QPushButton:disabled {
                background: #bdc3c7;
                color: #7f8c8d;
            }
        """

        if hasattr(self, 'install_btn'):
            self.install_btn.setStyleSheet(btn_style)
            self.cancel_btn.setStyleSheet("""
                QPushButton {
                    background: #e84118;
                    color: white;
                    border: none;
                    padding: 12px 25px;
                    border-radius: 5px;
                    font-weight: bold;
                    min-width: 150px;
                }
                QPushButton:hover {
                    background: #c23616;
                }
                QPushButton:pressed {
                    background: #a52e12;
                }
                QPushButton:disabled {
                    background: #bdc3c7;
                    color: #7f8c8d;
                }
            """)

    def setup_entrance_animation(self):
        """Configure l'animation d'entrée de la fenêtre"""
        self.setWindowOpacity(0)

        opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        opacity_anim.setDuration(500)
        opacity_anim.setStartValue(0)
        opacity_anim.setEndValue(1)
        opacity_anim.setEasingCurve(QEasingCurve.OutCubic)

        pos = self.pos()
        self.move(pos.x(), pos.y() - 20)
        pos_anim = QPropertyAnimation(self, b"pos")
        pos_anim.setDuration(500)
        pos_anim.setStartValue(QPoint(pos.x(), pos.y() - 20))
        pos_anim.setEndValue(pos)
        pos_anim.setEasingCurve(QEasingCurve.OutCubic)

        group = QParallelAnimationGroup()
        group.addAnimation(opacity_anim)
        group.addAnimation(pos_anim)

        group.start()

    def select_install_path(self):
        path = QFileDialog.getExistingDirectory(
            self,
            "Sélectionner le répertoire d'installation",
            self.install_options['install_path']
        )
        if path:
            self.install_options['install_path'] = path
            self.path_edit.setText(path)

    def update_option(self, option, value):
        self.install_options[option] = value

    def show_advanced_options(self):
        self.stacked_widget.setCurrentIndex(1)
        self.log_output.append("Options avancées disponibles dans l'onglet 'Avancé'")

    def change_theme(self, theme_name):
        theme_map = {
            "Dark Teal": "dark_teal.xml",
            "Dark Amber": "dark_amber.xml",
            "Light Blue": "light_blue.xml",
            "Light Cyan": "light_cyan.xml"
        }

        apply_stylesheet(QApplication.instance(), theme_map[theme_name], invert_secondary=True)

    def reset_settings(self):
        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Êtes-vous sûr de vouloir réinitialiser tous les paramètres?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.install_options = {
                'create_venv': True,
                'install_deps': True,
                'create_data_dir': True,
                'launch_after': True,
                'download_sample_docs': False,
                'create_desktop_icon': True,
                'install_path': os.path.expanduser("~")
            }

            # Mettre à jour l'interface
            self.venv_check.setChecked(True)
            self.deps_check.setChecked(True)
            self.data_dir_check.setChecked(True)
            self.launch_check.setChecked(True)
            self.sample_docs_check.setChecked(False)
            self.desktop_icon_check.setChecked(True)
            self.path_edit.setText(os.path.expanduser("~"))

            self.log_output.append("Paramètres réinitialisés aux valeurs par défaut")

    def save_log_file(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer le journal",
            os.path.join(self.install_options['install_path'], "mayan_install.log"),
            "Fichiers texte (*.log *.txt)"
        )

        if path:
            with open(path, 'w') as f:
                f.write(self.log_output.toPlainText())
            self.log_output.append(f"Journal enregistré sous {path}")

    def show_error_message(self, title, message, details=""):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)

        if details:
            msg.setDetailedText(details)

        msg.exec_()

    def start_installation(self):
        self.install_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.log_output.clear()

        # Vérifier les prérequis avant de commencer
        if not self.check_prerequisites():
            self.install_btn.setEnabled(True)
            self.cancel_btn.setEnabled(False)
            return

        self.install_thread = InstallerThread(self.install_options)
        self.install_thread.progress_signal.connect(self.update_progress)
        self.install_thread.finished_signal.connect(self.installation_finished)
        self.install_thread.log_signal.connect(self.update_log)
        self.install_thread.dependency_signal.connect(self.update_dependency_status)
        self.install_thread.download_progress.connect(self.update_download_progress)
        self.install_thread.start()

    def check_prerequisites(self):
        try:
            python_version = platform.python_version_tuple()
            if int(python_version[0]) < 3 or (int(python_version[0]) == 3 and int(python_version[1]) < 7):
                self.show_error_message(
                    "Python incompatible",
                    "Mayan EDMS nécessite Python 3.7 ou supérieur.",
                    f"Version détectée: {platform.python_version()}"
                )
                return False

            try:
                subprocess.check_call(["pip", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                self.show_error_message(
                    "Pip manquant",
                    "Pip n'est pas installé ou n'est pas dans le PATH.",
                    "Installez pip ou ajoutez-le à votre PATH."
                )
                return False

            try:
                urlopen('https://pypi.org', timeout=3)
            except URLError:
                reply = QMessageBox.question(
                    self,
                    "Pas de connexion Internet",
                    "Aucune connexion Internet détectée. Certaines fonctionnalités "
                    "pourraient ne pas être disponibles. Voulez-vous continuer?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return False

            return True
        except Exception as e:
            self.show_error_message(
                "Erreur de vérification",
                "Une erreur est survenue lors de la vérification des prérequis.",
                str(e)
            )
            return False

    def cancel_installation(self):
        if self.install_thread and self.install_thread.isRunning():
            reply = QMessageBox.question(
                self,
                "Confirmation",
                "Êtes-vous sûr de vouloir annuler l'installation?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.install_thread.stop()
                self.status_label.setText("Installation annulée")
                self.log_output.append(">>> Installation annulée par l'utilisateur")
                self.install_btn.setEnabled(True)
                self.cancel_btn.setEnabled(False)

    def update_progress(self, value, message):
        self.progress_animation.stop()
        self.progress_animation.setStartValue(self.progress_bar.value())
        self.progress_animation.setEndValue(value)
        self.progress_animation.setDuration(500)
        self.progress_animation.start()

        self.status_label.setText(message)

    def update_log(self, message):
        self.log_output.append(message)
        scroll_bar = self.log_output.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

    def update_dependency_status(self, dependency, status, message):
        for name, data in self.prereq_status.items():
            if name.startswith(dependency):
                data['label'].setText("✔ Disponible" if status else "✖ Manquant")
                data['label'].setStyleSheet("color: #27ae60;" if status else "color: #e84118;")
                data['desc'].setText(message)
                data['status'] = status
                break

    def update_download_progress(self, filename, downloaded, total):
        if total > 0:
            percent = int((downloaded / total) * 100)
            self.log_output.append(f"Téléchargement {filename}: {downloaded}/{total} bytes ({percent}%)")

    def installation_finished(self, success, message):
        self.install_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)

        if success:
            self.stacked_widget.setCurrentIndex(2)  # Page de fin
            if self.install_options['launch_after']:
                QTimer.singleShot(1000, self.launch_mayan)
        else:
            self.show_error_message(
                "Erreur d'installation",
                "L'installation n'a pas abouti.",
                message
            )

        self.progress_bar.setValue(0)
        self.status_label.setText("Prêt à installer")

    def launch_mayan(self):
        venv_dir = os.path.join(self.install_options['install_path'], "mayan-venv")
        data_dir = os.path.join(self.install_options['install_path'], "mayan-data")

        if platform.system() == "Windows":
            mayan_path = os.path.join(venv_dir, "Scripts", "mayan-edms.exe")
            subprocess.Popen(["start", "cmd", "/k", mayan_path, "runserver"], shell=True, cwd=data_dir)
        else:
            mayan_path = os.path.join(venv_dir, "bin", "mayan-edms.py")
            subprocess.Popen(["x-terminal-emulator", "-e", mayan_path, "runserver"], cwd=data_dir)

        QTimer.singleShot(3000, lambda: webbrowser.open("http://localhost:8000"))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Appliquer un thème moderne par défaut
    apply_stylesheet(app, theme='dark_teal.xml', invert_secondary=True)

    # Créer et afficher la fenêtre principale
    installer = MayanInstaller()

    # Animation d'apparition
    installer.setWindowOpacity(0)
    opacity_anim = QPropertyAnimation(installer, b"windowOpacity")
    opacity_anim.setDuration(500)
    opacity_anim.setStartValue(0)
    opacity_anim.setEndValue(1)
    opacity_anim.setEasingCurve(QEasingCurve.OutCubic)

    pos = installer.pos()
    installer.move(pos.x(), pos.y() - 20)
    pos_anim = QPropertyAnimation(installer, b"pos")
    pos_anim.setDuration(500)
    pos_anim.setStartValue(QPoint(pos.x(), pos.y() - 20))
    pos_anim.setEndValue(pos)
    pos_anim.setEasingCurve(QEasingCurve.OutCubic)

    group = QParallelAnimationGroup()
    group.addAnimation(opacity_anim)
    group.addAnimation(pos_anim)

    installer.show()
    group.start()

    sys.exit(app.exec_())
