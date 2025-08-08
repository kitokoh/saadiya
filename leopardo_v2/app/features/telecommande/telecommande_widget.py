import json
import logging
import os
import platform
import requests
import subprocess
import sys
import webbrowser
from PyQt5.QtCore import QPropertyAnimation, pyqtProperty, QSettings, Qt, QTimer, QTime, QDateTime, QProcess, QSize, QPoint, QRect
from PyQt5.QtGui import QFont, QIcon, QColor, QPixmap, QMovie
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QSplitter, QTabWidget, QHBoxLayout,
    QPushButton, QLabel, QSizePolicy, QGraphicsDropShadowEffect, QDesktopWidget,
    QMainWindow, QTextEdit, QMessageBox, QDialog, QGraphicsOpacityEffect, QProgressBar,
    QToolButton, QWidgetAction, QListWidget, QListWidgetItem, QFrame, QMenu, QCheckBox,
    QDialogButtonBox, QFormLayout
)

class FirstTimeGuide(QDialog):
    SETTINGS_PATH = (
        os.path.expanduser("~/AppData/Roaming/saadiya/resources/settings.json")
        if os.name == "nt"
        else os.path.expanduser("~/.saadiya/resources/settings.json")
    )

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Leopardo AI - First Time Guide")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedSize(parent.size())

        self.settings = self.load_settings()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.init_ui()
        self.setLayout(self.layout)

        self.steps = self.get_steps()
        self.current_step = 0

        self.highlight_overlay = QLabel(self)
        self.init_highlight_overlay()

        self.show_step()

    def init_ui(self):
        self.overlay_label = QLabel()
        self.overlay_label.setAlignment(Qt.AlignCenter)
        self.overlay_label.setStyleSheet(self.get_label_stylesheet())
        self.layout.addWidget(self.overlay_label)

        nav_layout = QHBoxLayout()
        self.next_button = self.create_button("Next", "#3498db", "#2980b9", self.next_step)
        nav_layout.addWidget(self.next_button)

        self.close_button = self.create_button("Skip", "#e74c3c", "#c0392b", self.skip_guide)
        nav_layout.addWidget(self.close_button)

        self.layout.addLayout(nav_layout)

    def create_button(self, text, bg_color, hover_color, callback):
        button = QPushButton(text)
        button.setStyleSheet(self.get_button_stylesheet(bg_color, hover_color))
        button.clicked.connect(callback)
        return button

    def init_highlight_overlay(self):
        self.highlight_overlay.setStyleSheet(self.get_highlight_stylesheet())
        self.highlight_overlay.hide()

    def load_settings(self):
        try:
            if os.path.exists(self.SETTINGS_PATH):
                with open(self.SETTINGS_PATH, "r") as file:
                    return json.load(file)
            return {"remotefirst": "False"}
        except json.JSONDecodeError:
            QMessageBox.warning(self, "Error", "Invalid settings file. Recreating default settings.")
            return {"remotefirst": "False"}

    def save_settings(self):
        os.makedirs(os.path.dirname(self.SETTINGS_PATH), exist_ok=True)
        with open(self.SETTINGS_PATH, "w") as file:
            json.dump(self.settings, file)

    def get_steps(self):
        return [
            {
                "text": "Cliquez sur le bouton circulaire au centre pour accéder au panneau de contrôle.",
                "target": self.parent.open_panel_btn,
            },
            {
                "text": "Cliquez sur le bouton rectangulaire à gauche pour démarrer le robot FB.",
                "target": self.parent.button_tabs.widget(0) if self.parent.button_tabs.count() > 0 else None,
            },
        ]

    def show_step(self):
        if self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            self.overlay_label.setText(step["text"])
            self.highlight_widget(step["target"])
        else:
            QMessageBox.information(self, "Guide Complete", "Vous avez terminé le guide initial.")
            self.close()

    def highlight_widget(self, widget):
        if not widget or not widget.isVisible():
            return

        rect = widget.geometry()
        offset = widget.mapToGlobal(QPoint(0, 0))
        self.highlight_overlay.setGeometry(QRect(offset.x(), offset.y(), rect.width(), rect.height()))

        animation = QPropertyAnimation(self.highlight_overlay, b"geometry")
        animation.setDuration(500)
        animation.setStartValue(QRect(offset.x(), offset.y(), 0, 0))
        animation.setEndValue(QRect(offset.x(), offset.y(), rect.width(), rect.height()))
        animation.start()

        self.highlight_overlay.show()

    def next_step(self):
        self.highlight_overlay.hide()
        self.current_step += 1
        self.show_step()

    def skip_guide(self):
        self.settings["remotefirst"] = "True"
        self.save_settings()
        self.close()

    @staticmethod
    def get_label_stylesheet():
        return (
            "QLabel {"
            "    color: white;"
            "    font-size: 18px;"
            "    font-weight: bold;"
            "    background-color: rgba(0, 0, 0, 0.7);"
            "    border-radius: 10px;"
            "    padding: 15px;"
            "    font-family: Arial, sans-serif;"
            "}"
        )

    @staticmethod
    def get_button_stylesheet(bg_color, hover_color):
        return (
            f"QPushButton {{"
            f"    background-color: {bg_color};"
            f"    color: white;"
            f"    font-size: 14px;"
            f"    border-radius: 10px;"
            f"    padding: 10px 20px;"
            f"    font-family: Arial, sans-serif;"
            f"}}"
            f"QPushButton:hover {{"
            f"    background-color: {hover_color};"
            f"}}"
        )

    @staticmethod
    def get_highlight_stylesheet():
        return (
            "QLabel {"
            "    border: 3px solid #f39c12;"
            "    background-color: rgba(0, 0, 0, 0.5);"
            "}"
        )


class AnimatedScreen(QLabel):
    def __init__(self, text="Ready to Control", parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(200)

        self.setStyleSheet(self.get_screen_stylesheet())

        self.apply_shadow_effect()
        self.add_text_glow_animation()
        self.add_pulsing_border_animation()

        self.background_movie = None
        self._text_opacity = 1.0
        self.text_animation = QPropertyAnimation(self, b"textOpacity")

    def get_text_opacity(self):
        return self._text_opacity

    def set_text_opacity(self, opacity):
        self._text_opacity = opacity
        self.setStyleSheet(
            f"""
            QLabel {{
                color: rgba(0, 255, 136, {int(opacity * 255)});
                font-size: 24px;
                font-weight: bold;
            }}
            """
        )

    textOpacity = pyqtProperty(float, get_text_opacity, set_text_opacity)

    def apply_shadow_effect(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(3, 3)
        shadow.setColor(QColor(0, 0, 0, 200))
        self.setGraphicsEffect(shadow)

    def get_screen_stylesheet(self):
        return """
            QLabel {
                background-color: rgba(45, 45, 45, 180);
                color: #00ff88;
                font-size: 24px;
                font-weight: bold;
                border-radius: 15px;
                padding: 15px;
                border: 2px solid #00ff88;
            }
        """

    def add_text_glow_animation(self):
        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)

        self.glow_animation = QPropertyAnimation(effect, b"opacity")
        self.glow_animation.setDuration(2000)
        self.glow_animation.setStartValue(0.8)
        self.glow_animation.setKeyValueAt(0.5, 1.0)
        self.glow_animation.setEndValue(0.8)
        self.glow_animation.setLoopCount(-1)
        self.glow_animation.start()

    def add_pulsing_border_animation(self):
        self.border_animation = QPropertyAnimation(self, b"styleSheet")
        self.border_animation.setDuration(1500)
        self.border_animation.setLoopCount(-1)

        start_style = """
            QLabel {
                background-color: rgba(45, 45, 45, 180);
                color: #00ff88;
                font-size: 24px;
                font-weight: bold;
                border-radius: 15px;
                padding: 15px;
                border: 3px solid #00ff88;
            }
        """
        end_style = """
            QLabel {
                background-color: rgba(45, 45, 45, 180);
                color: #00ff88;
                font-size: 24px;
                font-weight: bold;
                border-radius: 15px;
                padding: 15px;
                border: 3px solid #8800ff;
            }
        """

        self.border_animation.setStartValue(start_style)
        self.border_animation.setEndValue(end_style)
        self.border_animation.start()

    def set_background_gif(self, gif_path):
        if self.background_movie:
            self.background_movie.stop()

        self.background_movie = QMovie(gif_path)
        if self.background_movie.isValid():
            self.setMovie(self.background_movie)
            self.background_movie.start()
        else:
            print(f"Erreur : Le fichier GIF '{gif_path}' est introuvable ou invalide.")

    def add_typing_text(self, text, interval=100):
        self.current_text = ""
        self.full_text = text
        self.typing_timer = QTimer(self)
        self.typing_timer.timeout.connect(self._append_next_char)
        self.typing_timer.start(interval)

    def _append_next_char(self):
        if len(self.current_text) < len(self.full_text):
            self.current_text += self.full_text[len(self.current_text)]
            self.setText(self.current_text)
        else:
            self.typing_timer.stop()

    def add_progress_bar(self):
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(10, self.height() - 30, self.width() - 20, 20)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: rgba(45, 45, 45, 180);
                border: 1px solid #00ff88;
                border-radius: 10px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #00ff88;
                border-radius: 10px;
            }
        """)
        self.progress_bar.setValue(50)


class TelecommandeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.is_dark_theme = True
        self.settings = self.load_settings()

        self.initUI()

    def load_settings(self):
        settings_path = os.path.expanduser(
            "~/AppData/Roaming/saadiya/resources/settings.json" if os.name == "nt" else "~/.saadiya/resources/settings.json"
        )
        if not os.path.exists(settings_path):
            os.makedirs(os.path.dirname(settings_path), exist_ok=True)
            default_settings = {
                "language": "en",
                "fb_robot": "False",
                "multi_fb": "False",
                "walplus": "False",
                "wa_crm": "False",
                "fb_comment": "False",
                "insta": "False",
                "in_job": "False",
                "blog": "False",
                "ytb": "False",
                "pin": "False",
                "x": "False",
                "tok": "False",
                "remotefirst": "False",
                "pannel": "first"
            }
            with open(settings_path, "w") as file:
                json.dump(default_settings, file)
            return default_settings
        else:
            with open(settings_path, "r") as file:
                return json.load(file)

    def save_settings(self):
        settings_path = os.path.expanduser(
            "~/AppData/Roaming/saadiya/resources/settings.json" if os.name == "nt" else "~/.saadiya/resources/settings.json"
        )
        with open(settings_path, "w") as file:
            json.dump(self.settings, file)

    def initUI(self):
        self.setWindowTitle("Leopardo AI - Remote Control")
        self.setWindowIcon(QIcon('../resources/icons/robot-icons-30504-Windows.ico'))

        self.setFixedSize(450, 730)

        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(5, 5, 5, 5)

        screen_geometry = QDesktopWidget().availableGeometry()
        window_width = 450
        window_height = 700

        x = screen_geometry.width() - window_width - 10
        y = (screen_geometry.height() - window_height) // 2 - 70

        self.move(x, y)

        self.screen = AnimatedScreen("Ready to Control", self)
        self.screen.set_background_gif("resources/gifs/1.gif")
        self.screen.get_screen_stylesheet()
        self.screen.add_pulsing_border_animation()
        main_layout.addWidget(self.screen)

        self.change_background_gif("resources/gifs/1.gif")

        central_layout = QHBoxLayout()

        left_buttons = QVBoxLayout()

        button_actions = {
            "FB Robot": lambda: self.execute_robot_in_tab("FB Robot","Robot satarting","resources/gifs/fb_robot.gif"),
            "Multi FB": lambda: self.execute_robot_in_tab("Multi FB","Robot satarting","resources/gifs/multi_fb.gif"),
            "WA +": lambda: self.execute_robot_in_tab("WA +","Robot satarting","resources/gifs/wa.gif"),
            "WA CRM": lambda: self.execute_robot_in_tab("WA CRM","Robot satarting","resources/gifs/wa_crm.gif"),
            "FB Semi-Auto": lambda: self.execute_robot_in_tab("FB Semi-Auto","Robot satarting","resources/gifs/fb_comment.gif"),
            "Insta": lambda: self.execute_robot_in_tab("Insta","Robot satarting","resources/gifs/insta.gif"),
        }
        self.button_states = {
            "FB Robot": False
        }
        for name, icon in [("FB Robot", "resources/icons/fb_robot.ico"), ("Multi FB", "resources/icons/multi_fb.ico"),
                        ("WA +", "resources/icons/wa.png"), ("WA CRM", "resources/icons/wa_crm.png"),("FB Semi-Auto", "resources/icons/fb_comment.png"),("Insta", "resources/icons/insta.ico")]:
            btn = self.create_small_button(name, icon)
            self.apply_shadow_effect(btn)
            left_buttons.addWidget(btn)

            if name in button_actions:
                btn.clicked.connect(button_actions[name])

        circle_buttons_layout = QVBoxLayout()
        self.open_panel_btn = self.create_circular_button2("Panel" , "resources/icons/openpanel.png")
        self.start_robots_btn = self.create_circular_button2("Start All", "resources/icons/pannel.png")
        self.choice_module_btn = self.create_circular_button2("Strategie", "resources/icons/school.png")

        button_actions2 = {
            "IN Job": lambda: self.execute_robot_in_tab("IN Job","Robot satarting","resources/gifs/in_job.gif"),
            "Blog": lambda: self.execute_robot_in_tab("Blog","Robot satarting","resources/gifs/blog.gif"),
            "YTB": lambda: self.execute_robot_in_tab("YTB","Robot satarting","resources/gifs/ytb.gif"),
            "PIN": lambda: self.execute_robot_in_tab("PIN","Robot satarting","resources/gifs/pin.gif"),
            "X": lambda: self.execute_robot_in_tab("X","Robot satarting","resources/gifs/x.gif"),
            "TOK": lambda: self.execute_robot_in_tab("TOK","Robot satarting","resources/gifs/tok.gif"),
        }

        self.button_actionss = {
            "FB Robot": lambda: self.execute_robot_in_tab("FB Robot","Robot satarting","resources/gifs/fb_robot.gif"),
            "WA +": lambda: self.execute_robot_in_tab("WA +","Robot satarting","resources/gifs/1.gif"),
            "WA CRM": lambda: self.execute_robot_in_tab("WA CRM","Robot satarting","resources/gifs/1.gif"),
            "FB Semi-Auto": lambda: self.execute_robot_in_tab("FB Semi-Auto","Robot satarting","resources/gifs/1.gif"),
            "Insta": lambda: self.execute_robot_in_tab("Insta","Robot satarting","resources/gifs/1.gif"),
            "IN Job": lambda: self.execute_robot_in_tab("IN Job","Robot satarting","resources/gifs/1.gif"),
            "Blog": lambda: self.execute_robot_in_tab("Blog","Robot satarting","resources/gifs/1.gif"),
            "YTB": lambda: self.execute_robot_in_tab("YTB","Robot satarting","resources/gifs/1.gif"),
            "PIN": lambda: self.execute_robot_in_tab("PIN","Robot satarting","resources/gifs/1.gif"),
            "X": lambda: self.execute_robot_in_tab("X","Robot satarting","resources/gifs/1.gif"),
            "TOK": lambda: self.execute_robot_in_tab("TOK","Robot satarting","resources/gifs/1.gif"),
        }
        for btn in [self.open_panel_btn, self.start_robots_btn, self.choice_module_btn]:
            self.apply_shadow_effect(btn)
            circle_buttons_layout.addWidget(btn)

        right_buttons = QVBoxLayout()
        for name, icon in [("IN Job", "resources/icons/in_job.ico"), ("Blog", "resources/icons/blog.png"),
                        ("YTB", "resources/icons/ytb.ico"), ("PIN", "resources/icons/pin.png"),("X", "resources/icons/x.png"),
                        ("TOK", "resources/icons/tok.ico")]:
            btn = self.create_small_button(name, icon)
            self.apply_shadow_effect(btn)
            right_buttons.addWidget(btn)

            if name in button_actions2:
                btn.clicked.connect(button_actions2[name])

        central_layout.addLayout(left_buttons)
        central_layout.addLayout(circle_buttons_layout)
        central_layout.addLayout(right_buttons)

        main_layout.addLayout(central_layout)

        button_layout = QHBoxLayout()

        self.theme_button = QPushButton("Theme")
        self.theme_button.clicked.connect(self.toggle_theme)
        self.theme_button.setStyleSheet(self.get_button_stylesheet())
        button_layout.addWidget(self.theme_button)

        self.leds_layout = QHBoxLayout()
        self.green_led = self.create_led("green")
        self.yellow_led = self.create_led("yellow")
        self.red_led = self.create_led("red")
        self.leds_layout.addWidget(self.green_led)
        self.leds_layout.addWidget(self.yellow_led)
        self.leds_layout.addWidget(self.red_led)
        button_layout.addLayout(self.leds_layout)

        self.radio_button = QPushButton("Off")
        self.radio_button.setCheckable(True)
        self.radio_button.clicked.connect(self.toggle_radio)
        self.radio_button.setStyleSheet(self.get_radio_stylesheet())
        button_layout.addWidget(self.radio_button)

        main_layout.addLayout(button_layout)

        self.open_panel_btn.clicked.connect(self.handle_button_click)
        self.start_robots_btn.clicked.connect(self.handle_start_all_robots)
        self.choice_module_btn.clicked.connect(self.start_countdown)

        footer_layout = QHBoxLayout()

        self.footer = QLabel()
        self.footer.setAlignment(Qt.AlignLeft)
        self.footer.setStyleSheet("""
            QLabel {
                color: #aaa;
                font-size: 12px;
                font-style: italic;
                margin-top: 10px;
            }
        """)
        self.apply_shadow_effect(self.footer)
        footer_layout.addWidget(self.footer)

        self.update_footer()
        timer = QTimer(self)
        timer.timeout.connect(self.update_footer)
        timer.start(1000)

        self.timer_label = QLabel("Time : 00:00:00")
        self.timer_label.setAlignment(Qt.AlignRight)
        self.timer_label.setStyleSheet("""
            QLabel {
                color: #ff6347;
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
            }
        """)
        self.apply_shadow_effect(self.timer_label)
        footer_layout.addWidget(self.timer_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.time_remaining = QTime(0, 5, 0)

        self.splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(self.splitter)

        self.button_tabs = QTabWidget()
        self.splitter.addWidget(self.button_tabs)

        self.processes = {}
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_terminal_tab)

        main_layout.addLayout(footer_layout)

        self.splitter.addWidget(self.tab_widget)

        self.setLayout(main_layout)

    def activate_light1(self, message):
        self.screen.change_style(message, self.get_light_stylesheet1())
        QTimer.singleShot(20000, self.reset_light1)

    def reset_light1(self):
        self.screen.change_style("Ready to Control", self.screen.get_screen_stylesheet())

    def get_light_stylesheet1(self):
        return """
            QLabel {
                background-color: #ff4500;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border: 2px solid #8b0000;
                border-radius: 15px;
                padding: 15px;
            }
        """

    def change_background_gif(self, gif_path):
        if gif_path:
            if self.screen.background_movie:
                current_gif = self.screen.background_movie.fileName()
                if current_gif != gif_path:
                    self.screen.set_background_gif(gif_path)
                else:
                    print("Le GIF sélectionné est déjà en cours d'affichage.")
            else:
                self.screen.set_background_gif(gif_path)
        else:
            print("Erreur : Aucun chemin de GIF valide n'a été fourni.")

    def apply_shadow_effect(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setOffset(2, 2)
        shadow.setColor(QColor(0, 0, 0, 160))
        widget.setGraphicsEffect(shadow)

    def update_footer(self):
        current_time = QDateTime.currentDateTime().toString("hh:mm:ss AP")
        footer_text = f"©2025 Nova360 AI - Remote Control | {current_time}"
        self.footer.setText(footer_text)

    def create_led(self, color):
        led = QLabel()
        led.setFixedSize(30, 30)
        led.setStyleSheet(f"background-color: gray; border-radius: 15px;")
        return led

    def toggle_theme(self):
        print("Theme toggled!")

    def toggle_radio(self):
        if self.radio_button.isChecked():
            self.activate_light1("feu Marketing  ")
            self.change_background_gif("resources/gifs/on.gif")
            self.radio_button.setText("On")
            self.green_led.setStyleSheet("background-color: green; border-radius: 15px;")
            self.yellow_led.setStyleSheet("background-color: gray; border-radius: 15px;")
            self.red_led.setStyleSheet("background-color: gray; border-radius: 15px;")
        else:
            self.radio_button.setText("Off")
            self.green_led.setStyleSheet("background-color: gray; border-radius: 15px;")
            self.close_all_tabs()

    def close_terminal_tab(self, index):
        widget = self.tab_widget.widget(index)
        if widget:
            if index in self.processes:
                process = self.processes[index]
                try:
                    if process.state() != QProcess.NotRunning:
                        process.terminate()
                        if not process.waitForFinished(5000):
                            process.kill()
                except Exception as e:
                    logging.error(f"Error closing process: {e}")
                finally:
                    del self.processes[index]
            self.tab_widget.removeTab(index)

    def close_all_tabs(self):
        for index in range(self.tab_widget.count()):
            self.close_terminal_tab(index)

    def handle_start_all_robots(self):
        self.start_robots_btn.setText("Starting...")
        self.start_robots_btn.setEnabled(False)
        self.change_background_gif("resources/gifs/start_all.gif")
        dialog = self.create_popup()
        if dialog.exec_() == QDialog.Accepted:
            self.start_all_robots()
        else:
            self.reset_start_button()

    def reset_start_button(self):
        self.start_robots_btn.setText("Start All")
        self.start_robots_btn.setEnabled(True)

    def start_all_robots(self):
        try:
            for action_name, action_func in self.button_actionss.items():
                action_func()
        except Exception as e:
            print(f"Erreur lors du démarrage des robots : {e}")
        finally:
            QTimer.singleShot(5000, lambda: self.reset_start_button())

    def create_popup(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Confirmation")
        dialog.setWindowIcon(QIcon("resources/icons/confirmation.ico"))
        dialog.setFixedSize(400, 200)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #222831;
                border-radius: 10px;
            }
            QLabel {
                color: #eeeeee;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton {
                border: 1px solid #00adb5;
                border-radius: 5px;
                color: #eeeeee;
                padding: 8px 15px;
                background-color: #00adb5;
            }
            QPushButton:hover {
                background-color: #393e46;
            }
            QPushButton:pressed {
                background-color: #007b83;
            }
        """)
        layout = QVBoxLayout(dialog)
        label = QLabel("Do you want to start all the robots?")
        label.setFont(QFont("Arial", 14))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        button_layout = QVBoxLayout()
        confirm_button = QPushButton("yes, Start ")
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(confirm_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        confirm_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)
        return dialog

    def handle_button_click(self):
        self.change_background_gif("resources/gifs/pannel.gif")
        print("Button clicked")

    def start_countdown(self):
        self.time_remaining = QTime(0, 5, 0)
        self.timer.start(1000)
        self.timer_label.setText(f"Temps restant: {self.time_remaining.toString('hh:mm:ss')}")
        self.change_background_gif("resources/gifs/strategie.gif")
        QTimer.singleShot(3000, self.open_website)

    def open_website(self):
        webbrowser.open("https://nova360.turknovatech.com/")

    def update_timer(self):
        if self.time_remaining > QTime(0, 0, 0):
            self.time_remaining = self.time_remaining.addSecs(-1)
            self.timer_label.setText(f"Temps restant: {self.time_remaining.toString('hh:mm:ss')}")
        else:
            self.timer.stop()
            self.timer_label.setText("Exécution du programme!")

    def create_small_button(self, text, icon_path):
        button = QPushButton(text)
        button.setIcon(QIcon(icon_path))
        return button

    def create_circular_button2(self, name, icon_path):
        button = QPushButton(name)
        button.setFixedSize(100, 100)
        button.setStyleSheet(self.get_circular_button_stylesheet2(name, icon_path))
        return button

    def get_circular_button_stylesheet2(self, button_name, icon_path):
        return f"""
        QPushButton {{
            background-color: transparent;
            background-image: url({icon_path});
            background-position: center;
            background-repeat: no-repeat;
            background-size: cover;
            color: #00ff00;
            font-size: 14px;
            font-weight: bold;
            text-align: center;
            border-radius: 50px;
            border: 2px solid #4caf50;
            padding-top: 65px;
        }}
        QPushButton:hover {{
            background-color: transparent;
            background-image: url({icon_path});
            background-position: center;
            background-repeat: no-repeat;
            background-size: cover;
            color: #007BFF;
            border: 2px solid #76ff03;
            transform: scale(1.1);
        }}
        QPushButton:pressed {{
            background-color: transparent;
            background-image: url({icon_path});
            background-position: center;
            background-repeat: no-repeat;
            background-size: cover;
            color: #ffffff;
            border: 2px solid #1b5e20;
        }}
        """

    def get_button_stylesheet(self):
        return """
            QPushButton {
                background-color: lightblue;
                padding: 10px;
                border: 2px solid darkblue;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: skyblue;
            }
        """

    def get_radio_stylesheet(self):
        return """
            QPushButton {
                background-color: lightgray;
                padding: 10px;
                border: 2px solid gray;
                border-radius: 15px;
            }
            QPushButton:checked {
                background-color: green;
                color: white;
            }
        """

    def run_executable_in_tab(self, executable_path, output_widget):
        if not os.path.exists(executable_path):
            output_widget.append(f"[Erreur] Le fichier exécutable est introuvable : {executable_path}")
            logging.error(f"Executable not found: {executable_path}")
            return None

        process = QProcess(self)

        process.readyReadStandardOutput.connect(
            lambda: output_widget.append(
                process.readAllStandardOutput().data().decode("utf-8", errors="ignore")
            )
        )
        process.readyReadStandardError.connect(
            lambda: output_widget.append(
                f"[Erreur] {process.readAllStandardError().data().decode('utf-8', errors='ignore')}"
            )
        )

        def handle_error(error):
            error_messages = {
                QProcess.FailedToStart: "Le processus n'a pas pu démarrer.",
                QProcess.Crashed: "Le processus a crashé.",
                QProcess.Timedout: "Le processus a expiré.",
                QProcess.WriteError: "Erreur lors de l'écriture dans le processus.",
                QProcess.ReadError: "Erreur lors de la lecture depuis le processus.",
            }
            message = error_messages.get(error, "Erreur inconnue.")
            output_widget.append(f"[Erreur] {message}")
            logging.error(f"Process error: {message}")

        process.errorOccurred.connect(handle_error)

        def handle_finished(exit_code, exit_status):
            status_message = (
                "Terminé avec succès." if exit_status == QProcess.NormalExit else "Le processus s'est arrêté de manière anormale."
            )
            output_widget.append(f"[Info] Processus terminé avec le code {exit_code}: {status_message}")
            logging.info(f"Process finished: {status_message} (Exit code: {exit_code})")

        process.finished.connect(handle_finished)

        try:
            process.start(executable_path)
            logging.info(f"Process started: {executable_path}")
            output_widget.append(f"[Info] Processus démarré : {executable_path}")
        except Exception as e:
            logging.error(f"Failed to start process: {e}")
            output_widget.append(f"[Erreur] Impossible de démarrer le processus : {e}")
            return None

        return process

    def execute_robot_in_tab(self, robot_name, message, gif_path):
        self.activate_light1(message)
        self.change_background_gif(gif_path)

        if not hasattr(self, 'tab_widget') or self.tab_widget is None:
            logging.error("tab_widget is not initialized.")
            return

        if self.button_states.get(robot_name, False):
            logging.warning(f"{robot_name} is already running.")
            return

        robot_path = self.get_robot_path(robot_name)
        if not robot_path or not os.path.exists(robot_path):
            logging.error(f"Executable not found: {robot_path}")
            return

        button = self.find_button_by_name(robot_name)
        if button:
            button.setEnabled(False)
        self.button_states[robot_name] = True

        terminal_output = QTextEdit()
        terminal_output.setReadOnly(True)

        tab_title = f"{robot_name} "
        index = self.tab_widget.addTab(terminal_output, tab_title)
        self.tab_widget.setCurrentIndex(index)

        process = self.run_executable_in_tab(robot_path, terminal_output)

        def on_process_finished():
            self.button_states[robot_name] = False
            if button:
                button.setEnabled(True)
            logging.info(f"{robot_name} execution finished.")

        process.finished.connect(on_process_finished)

        if not self.radio_button.isChecked():
            self.close_terminal_tab(index)

    def get_robot_path(self, robot_name):
        executable_name = {
            "FB Robot": "fb_robot.exe",
            "Multi FB": "multi_fb.exe",
            "WA +": "wa.exe",
            "WA CRM": "wa_crm.exe",
            "FB Semi-Auto": "fb_semiauto.exe",
            "Insta": "insta.exe",
            "IN Job": "in_job.exe",
            "Blog": "blog.exe",
            "YTB": "ytb.exe",
            "PIN": "pin.exe",
            "X": "x.exe",
            "TOK": "tok.exe",
            "Mail": "mail.exe",
            "Reddit": "reddit.exe",
            "Snap": "snap.exe",
        }.get(robot_name)

        if not executable_name:
            logging.error(f"No executable defined for robot: {robot_name}")
            return None

        if platform.system() == "Windows":
            user_profile = os.getenv('APPDATA')
            if not user_profile:
                logging.error("APPDATA environment variable not found.")
                return None
            robot_path = os.path.join(user_profile, 'saadiya', 'resources', 'tools', executable_name)
        elif platform.system() == "Darwin":
            user_profile = os.getenv('HOME')
            if not user_profile:
                logging.error("HOME environment variable not found.")
                return None
            robot_path = os.path.join(user_profile, 'Library', 'Application Support', 'saadiya', 'resources', 'tools', executable_name.replace(".exe", ""))
        else:
            logging.error(f"Unsupported OS detected: {platform.system()}")
            return None

        if os.path.exists(robot_path):
            logging.info(f"Executable found: {robot_path}")
            return robot_path
        else:
            logging.warning(f"Executable not found: {robot_path}")
            return None

    def find_button_by_name(self, name):
        for button in self.findChildren(QPushButton):
            if button.text() == name:
                return button
        return None
