import sys
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QTextBrowser, QCheckBox, 
                            QPushButton, QFrame, QLabel, QScrollArea, QSizePolicy)
from PyQt5.QtCore import Qt, QDate, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QTextDocument, QTextCursor
from demarrage.baseDialog import BaseDialog
from typing import List, Dict, Optional, Tuple, Callable
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QTextEdit, QPushButton, QSlider, QCheckBox, 
                            QMessageBox, QDialog, QDialogButtonBox)
from PyQt5.QtCore import QRect

class TermsDialog(BaseDialog):
    def init_ui(self):
        # Configuration de la fenêtre
        self.setMinimumSize(700, 650)
        self.setWindowTitle("Conditions d'Utilisation")
        
        # Layout principal avec espacement et marges modernes
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 20)
        layout.setSpacing(20)
        
        # En-tête stylisé avec effet de profondeur
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(5)
        
        # Icône et titre
        self.label = QLabel("Conditions d'Utilisation")
        self.label.setObjectName("titleLabel")
        self.label.setAlignment(Qt.AlignCenter)
        
        # Sous-titre avec version et date
        version_label = QLabel(f"Version 2.3.1 • {QDate.currentDate().toString('dd MMMM yyyy')}")
        version_label.setObjectName("versionLabel")
        version_label.setAlignment(Qt.AlignCenter)
        
        # Séparateur décoratif
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setObjectName("separator")
        
        header_layout.addWidget(self.label)
        header_layout.addWidget(version_label)
        header_layout.addWidget(separator)
        
        # Zone de texte avec barre de défilement moderne
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setObjectName("scrollArea")
        
        self.terms_text = QTextBrowser()
        self.terms_text.setOpenExternalLinks(True)
        self.terms_text.setObjectName("termsText")
        self.terms_text.document().setDocumentMargin(20)
        self.load_terms_content()
        
        # Animation de défilement automatique au début
        cursor = self.terms_text.textCursor()
        cursor.movePosition(QTextCursor.Start)
        self.terms_text.setTextCursor(cursor)
        
        scroll_area.setWidget(self.terms_text)
        
        # Case à cocher avec animation et style moderne
        self.accept_checkbox = QCheckBox("J'accepte les conditions d'utilisation ci-dessus")
        self.accept_checkbox.setObjectName("acceptCheckbox")
        self.accept_checkbox.setCursor(Qt.PointingHandCursor)
        
        # Boutons avec disposition moderne et effets hover
        button_container = QFrame()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 10, 0, 0)
        button_layout.setSpacing(15)
        
        self.continue_btn = QPushButton("Continuer vers l'Application")
        self.continue_btn.setObjectName("primaryButton")
        self.continue_btn.setEnabled(False)
        self.continue_btn.setCursor(Qt.PointingHandCursor)
        self.continue_btn.setMinimumSize(180, 40)
        
        cancel_btn = QPushButton("Quitter l'Application")
        cancel_btn.setObjectName("secondaryButton")
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setMinimumSize(150, 40)
        
        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(self.continue_btn)
        
        # Ajout des widgets au layout principal
        layout.addWidget(header_frame)
        layout.addWidget(scroll_area)
        layout.addWidget(self.accept_checkbox)
        layout.addWidget(button_container)
        
        # Connexions des signaux
        self.accept_checkbox.stateChanged.connect(self.toggle_continue_button)
        self.continue_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        # Appliquer le style moderne avec effets et transitions
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f7fa;
            }
            
            #headerFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border-radius: 12px;
                padding: 25px 20px 15px 20px;
                border: 1px solid #e0e6ed;
            }
            
            #titleLabel {
                font-size: 22px;
                font-weight: 600;
                color: #2d3748;
                font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
            }
            
            #versionLabel {
                font-size: 13px;
                color: #718096;
                font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
            }
            
            #separator {
                border: none;
                height: 1px;
                background: linear-gradient(to right, 
                    rgba(200, 200, 200, 0), 
                    rgba(66, 153, 225, 0.5), 
                    rgba(200, 200, 200, 0));
                margin: 10px 30px;
            }
            
            #scrollArea {
                border: none;
                background: transparent;
            }
            
            #termsText {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 25px;
                font-size: 14px;
                color: #4a5568;
                font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            }
            
            #termsText a {
                color: #4299e1;
                text-decoration: none;
            }
            
            #termsText a:hover {
                text-decoration: underline;
            }
            
            #acceptCheckbox {
                font-size: 14px;
                color: #4a5568;
                spacing: 12px;
                padding: 8px 0;
                font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
            }
            
            #acceptCheckbox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #cbd5e0;
                border-radius: 5px;
            }
            
            #acceptCheckbox::indicator:checked {
                background-color: #4299e1;
                border-color: #4299e1;
                image: url(:/icons/checkmark.svg);
            }
            
            #acceptCheckbox::indicator:hover {
                border-color: #a0aec0;
            }
            
            #primaryButton {
                background-color: #4299e1;
                color: white;
                border-radius: 8px;
                padding: 10px 24px;
                font-weight: 500;
                font-size: 14px;
                border: none;
                font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
                transition: all 0.2s ease;
            }
            
            #primaryButton:hover {
                background-color: #3182ce;
                transform: translateY(-1px);
                box-shadow: 0 2px 5px rgba(49, 130, 206, 0.3);
            }
            
            #primaryButton:pressed {
                transform: translateY(0);
                box-shadow: none;
            }
            
            #primaryButton:disabled {
                background-color: #bee3f8;
                transform: none;
                box-shadow: none;
            }
            
            #secondaryButton {
                background-color: white;
                color: #4a5568;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: 500;
                font-size: 14px;
                font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
                transition: all 0.2s ease;
            }
            
            #secondaryButton:hover {
                background-color: #f7fafc;
                border-color: #cbd5e0;
                transform: translateY(-1px);
                box-shadow: 0 2px 5px rgba(203, 213, 224, 0.3);
            }
            
            #secondaryButton:pressed {
                transform: translateY(0);
                box-shadow: none;
            }
        """)
        
        self.setLayout(layout)
    
    def load_terms_content(self):
        """Charge un contenu HTML stylisé avec des sections interactives"""
        terms_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    font-family: 'Segoe UI', system-ui, sans-serif;
                    line-height: 1.7;
                    color: #2d3748;
                    margin: 0;
                    padding: 0;
                }
                h1 {
                    color: #2c5282;
                    font-size: 1.5em;
                    margin-bottom: 1em;
                    padding-bottom: 0.5em;
                    border-bottom: 1px solid #e2e8f0;
                }
                h2 {
                    color: #2b6cb0;
                    margin-top: 1.8em;
                    margin-bottom: 0.8em;
                    font-size: 1.3em;
                }
                h3 {
                    color: #4a5568;
                    margin-top: 1.5em;
                    margin-bottom: 0.5em;
                    font-size: 1.1em;
                }
                p {
                    margin-bottom: 1.2em;
                    text-align: justify;
                }
                ul, ol {
                    margin-bottom: 1.5em;
                    padding-left: 1.8em;
                }
                li {
                    margin-bottom: 0.6em;
                    position: relative;
                }
                li:before {
                    content: "•";
                    color: #4299e1;
                    font-weight: bold;
                    display: inline-block;
                    width: 1em;
                    margin-left: -1em;
                }
                strong {
                    color: #2d3748;
                }
                .highlight {
                    background-color: #ebf8ff;
                    padding: 0.2em 0.4em;
                    border-radius: 0.3em;
                    font-weight: 500;
                }
                .section {
                    margin-bottom: 2em;
                    background: #f8fafc;
                    padding: 1.5em;
                    border-radius: 0.5em;
                    border-left: 4px solid #4299e1;
                }
                .warning {
                    background-color: #fffaf0;
                    border-left-color: #dd6b20;
                }
                .warning-title {
                    color: #dd6b20;
                }
                .info {
                    background-color: #f0fff4;
                    border-left-color: #38a169;
                }
                .info-title {
                    color: #38a169;
                }
                a {
                    color: #3182ce;
                    text-decoration: none;
                    transition: color 0.2s;
                }
                a:hover {
                    color: #2c5282;
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <h1>Conditions Générales d'Utilisation</h1>
            
            <div class="section">
                <h2>1. Acceptation des Conditions</h2>
                <p>En utilisant cette application, vous acceptez sans réserve les présentes conditions générales d'utilisation. Si vous n'acceptez pas ces conditions, veuillez ne pas utiliser l'application.</p>
                
                <h3>Modifications des Conditions</h3>
                <p>Nous nous réservons le droit de modifier ces conditions à tout moment. Les modifications prendront effet immédiatement après leur publication dans l'application.</p>
            </div>
            
            <div class="section">
                <h2>2. Utilisation du Service</h2>
                <p>Cette application vous permet de :</p>
                <ul>
                    <li><strong>Planifier et publier</strong> du contenu sur plusieurs réseaux sociaux</li>
                    <li><strong>Analyser les performances</strong> de vos publications</li>
                    <li><strong>Collaborer</strong> avec votre équipe marketing</li>
                    <li><strong>Gérer</strong> plusieurs comptes sociaux simultanément</li>
                </ul>
                
                <h3>Restrictions d'Usage</h3>
                <p>Vous vous engagez à ne pas :</p>
                <ul>
                    <li>Utiliser l'application à des fins illégales</li>
                    <li>Tenter de contourner les mesures de sécurité</li>
                    <li>Utiliser des robots ou scripts automatisés</li>
                </ul>
            </div>
            
            <div class="section info">
                <h2 class="info-title">3. Protection des Données</h2>
                <p>Nous accordons une importance primordiale à la protection de vos données :</p>
                <ul>
                    <li>Stockage <span class="highlight">local</span> sur votre appareil</li>
                    <li>Chiffrement AES-256 des informations sensibles</li>
                    <li>Conformité RGPD pour les utilisateurs européens</li>
                    <li>Transparence totale sur l'utilisation des données</li>
                </ul>
                
                <h3>Données Collectées</h3>
                <p>Nous collectons uniquement les données nécessaires au fonctionnement de l'application :</p>
                <ul>
                    <li>Identifiants de connexion aux réseaux sociaux (optionnel)</li>
                    <li>Préférences de l'application</li>
                    <li>Statistiques d'utilisation anonymisées</li>
                </ul>
            </div>
            
            <div class="section warning">
                <h2 class="warning-title">4. Responsabilités</h2>
                <p>En tant qu'utilisateur, vous vous engagez à :</p>
                <ul>
                    <li>Maintenir la confidentialité de vos identifiants</li>
                    <li>Respecter les conditions d'utilisation des réseaux sociaux</li>
                    <li>Ne pas publier de contenu illégal ou inapproprié</li>
                </ul>
                
                <h3>Limitation de Responsabilité</h3>
                <p>Nous déclinons toute responsabilité pour :</p>
                <ul>
                    <li>Les interruptions de service non planifiées</li>
                    <li>Les modifications des API des réseaux sociaux</li>
                    <li>L'utilisation inappropriée de l'application</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>5. Propriété Intellectuelle</h2>
                <p>Tous les droits de propriété intellectuelle relatifs à l'application restent notre propriété exclusive.</p>
                
                <h3>Licence d'Utilisation</h3>
                <p>Nous vous accordons une licence personnelle, non exclusive et non transférable pour utiliser l'application.</p>
            </div>
            
            <div class="section">
                <h2>6. Résiliation</h2>
                <p>Nous pouvons résilier votre accès à l'application sans préavis en cas de violation des présentes conditions.</p>
                
                <h3>Conséquences de la Résiliation</h3>
                <p>En cas de résiliation :</p>
                <ul>
                    <li>Votre accès à l'application sera immédiatement désactivé</li>
                    <li>Vos données locales resteront sur votre appareil</li>
                </ul>
            </div>
            
            <p style="text-align: center; margin-top: 2em; font-size: 0.9em; color: #718096;">
                Dernière mise à jour: %s
            </p>
        </body>
        </html>
        """ % QDate.currentDate().toString('dd/MM/yyyy')
        
        self.terms_text.setHtml(terms_html)
    
    def toggle_continue_button(self, state):
        """Active/désactive le bouton Continuer avec animation sophistiquée"""
        was_enabled = self.continue_btn.isEnabled()
        self.continue_btn.setEnabled(state == Qt.Checked)
        
        # Animation seulement lors de l'activation (pas lors de la désactivation)
        if state == Qt.Checked and not was_enabled:
            animation = QPropertyAnimation(self.continue_btn, b"geometry", self)
            animation.setDuration(300)
            animation.setEasingCurve(QEasingCurve.OutBack)
            
            start_geo = self.continue_btn.geometry()
            end_geo = start_geo
            
            # Effet de rebond
            animation.setKeyValueAt(0.3, QRect(
                start_geo.x() - 5, 
                start_geo.y(), 
                start_geo.width() + 10, 
                start_geo.height()
            ))
            
            animation.setEndValue(end_geo)
            animation.start()
    
    def get_results(self) -> Dict:
        return {'accepted_terms': self.accept_checkbox.isChecked()}