from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QVBoxLayout, QWidget, QDialog, QLabel, QPushButton, QMessageBox, QMenu, QComboBox, QStatusBar
class Common() :
        def __init__(self, parent=None):

            label = QLabel(self.tr(
                "<div style='background-color:#F5F7FA; padding:15px; border-radius:10px;'>"
                "<h1 style='color:#1A5276; font-size:24px; font-weight:bold; text-align:center;'>Welcome to Nova360.ai</h1>"
                
                "<p style='font-size:16px; color:#333333; text-align:center;'>"
                "<strong>Your All-in-One AI-Powered Social Media Automation Solution</strong>"
                "</p><br>"
                
                "<div style='padding: 10px; border-left: 4px solid #1A5276;'>"
                "<p style='font-size:14px; color:#5D6D7E; line-height:1.6; margin:0 20px;'>"
                "Nova360.ai is the essential tool for entrepreneurs, brands, and influencers looking to simplify and scale their social media presence.<br>"
                "With advanced AI, Nova360.ai automates every aspect of your social media strategy, allowing you to engage effortlessly,<br>"
                "grow your influence, and remain at the forefront of your audience’s minds."
                "</p>"
                "</div><br>"
                
                "<h3 style='color:#1A5276; font-size:18px; margin-top:20px; text-align:center;'>Core Features</h3><br>"
                
                "<ul style='font-size:14px; color:#4A4A4A; padding-left: 40px;'>"
                "<li style='margin-bottom:10px;'><strong>🌐 Smart Scheduling:</strong> Plan and post content across platforms with precision timing for maximum reach.</li><br>"
                "<li style='margin-bottom:10px;'><strong>🤖 Automated Audience Engagement:</strong> Engage your audience with intelligent replies and dynamic comments.</li><br>"
                "<li><strong>📂 Comprehensive Media & Group Management:</strong> Manage media assets, groups, and instances seamlessly to optimize your workflow.</li>"
                "</ul><br>"
                
                "<p style='font-size:14px; color:#5D6D7E; line-height:1.6; text-align:center;'>"
                "Join a thriving community of brands and individuals who trust Nova360.ai to elevate their social media automation.<br>"
                "Save time, boost engagement, and focus on building your brand."
                "</p><br>"
                
                "<p style='font-size:11px; color:#888888; text-align:center; margin-top:20px;'>"
                "© 2024 Nova360 Pro | "
                "<a href='https://www.nova360pro.com' style='color:#1A5276; text-decoration:none;'>www.nova360pro.com</a>"
                "</p>"
                "</div>"
            ))
            label = QLabel(self.tr(
                "<div style='background-color:#FAF3E0; padding:15px; border-radius:8px;'>"
                "<h2 style='color:#D35400; font-size:20px; text-align:center;'>Expiration de Votre Licence</h2>"
                
                "<p style='font-size:14px; color:#4A4A4A; line-height:1.6;'>"
                "Votre licence est actuellement valide jusqu'au <strong style='color:#D35400;'>31 décembre 202x</strong>.<br>"
                "Pour continuer à profiter de toutes les fonctionnalités premium de <strong>Nova360.ai</strong>, veuillez penser à renouveler votre licence avant cette date.<br>"
                "</p><br>"
                
                "<div style='padding: 10px; border-left: 4px solid #D35400; margin: 10px 0;'>"
                "<p style='font-size:13px; color:#7F8C8D; margin:0 20px;'>"
                "Après cette date, votre accès aux fonctionnalités premium sera restreint. Vous pourrez toujours accéder à votre compte mais avec des fonctionnalités limitées jusqu'au renouvellement de votre licence."
                "</p>"
                "</div><br>"
                
                "<h3 style='color:#D35400; font-size:16px;'>En Cas de Problème</h3>"
                
                "<ul style='font-size:13px; color:#4A4A4A; padding-left: 40px;'>"
                "<li style='margin-bottom:10px;'>Si votre instance ne fonctionne plus, vérifiez la connexion Internet et assurez-vous que la licence est active.</li><br>"
                "<li>Contactez notre support technique si vous rencontrez des difficultés supplémentaires.</li>"
                "</ul><br>"
                
                "<p style='font-size:12px; color:gray; text-align:center;'>"
                "Pour toute assistance, veuillez visiter <a href='https://support.nova360pro.com' style='color:#D35400; text-decoration:none;'>notre centre de support</a>."
                "</p>"
                "</div>"
            ))


            #dynamyserla requette pour voir la validiter 
