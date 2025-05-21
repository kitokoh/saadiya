    def create_top_menu(self):
        """
        Crée une barre de menu supérieure réorganisée avec une nouvelle structure radicale.
        """
        # Initialisation de l'état utilisateur
        self.is_user_logged_in = False
        self.is_enterprise_mode = False
        self.current_username = "Guest"
        
        # Charger l'état de connexion
        self.load_session_state()

        # Configuration du menu
        self.menu_config = {
            'visible_buttons': {
                'Tools': False,
                'Data': False,
                'Support': False
            }
        }
        self.load_menu_config()

        # Création du conteneur principal
        self.top_menu = QFrame()
        self.top_menu.setFixedHeight(50)
        self.top_menu.setStyleSheet("""
            QFrame {
                background-color: #f8fafc;
                border-bottom: 1px solid #e2e8f0;
            }
        """)

        # Layout principal
        self.top_menu_layout = QHBoxLayout(self.top_menu)
        self.top_menu_layout.setContentsMargins(5, 5, 5, 5)
        self.top_menu_layout.setSpacing(10)

        # --- Logo / Titre de l'application ---
        self.app_title = QLabel("Leopardo AI")
        self.app_title.setStyleSheet("""
            QLabel {
                color: #2563eb;
                font-size: 18px;
                font-weight: bold;
                padding: 0 15px;
            }
        """)
        self.top_menu_layout.addWidget(self.app_title)

        # --- Barre de menu ---
        self.menu_bar = QHBoxLayout()
        self.menu_bar.setSpacing(5)
        
        # Nouvelle structure des éléments de menu principal
        menu_items = [
            # 1. Home (inchangé)
            ("🏠", self.tr("Home"), "home", self.open_home, self.tr("Main dashboard"), []),
            
            # 2. Marketing
            ("📢", self.tr("Marketing"), "marketing", None, self.tr("Marketing tools"), [
                ("🎬", self.tr("My Media"), "media", self.add_media_page, self.tr("Media Management"), []),
                ("🌐", self.tr("My Groups"), "grups", self.open_grups_window, self.tr("Group list"), []),
                ("🤖", self.tr("Marketing Robots"), "marketing_robots", self.open_marketing, self.tr("Marketing automation tools"), []),
                ("📰", self.tr("Ads Manager"), "ads_manager", self.open_ads_manager, self.tr("Manage advertising campaigns"), []),
                ("⏳", self.tr("Campaign Scheduler"), "campaign_scheduler", self.open_sheduling_window, self.tr("Schedule marketing campaigns"), []),
                ("✉️", self.tr("Email & SMS"), "email_sms", self.open_email_sms, self.tr("Email and SMS marketing tools"), []),
                ("🖋️", self.tr("Content Generator"), "content_generator", self.open_content_generator, self.tr("Generate marketing content"), []),
            ]),
            
            # 3. Sales
            ("💰", self.tr("Sales"), "sales", None, self.tr("Sales tools"), [
                ("📂", self.tr("Project Management"), "project_management", self.open_project_management, self.tr("Manage sales projects"), []),
                ("🛠️", self.tr("SAV"), "sav", self.open_sav, self.tr("After-sales service management"), []),
                ("🔗", self.tr("Short Links & Trackers"), "links", self.open_links_window, self.tr("Manage and track links"), []),
                ("👥", self.tr("Prospection & Relances"), "contact", self.open_contacts_window, self.tr("Contact list and follow-ups"), []),
                ("📑", self.tr("DMS & Quotes"), "dms_quotes", self.open_dms_quotes, self.tr("Document management and quotes"), []),
                ("📊", self.tr("CRM"), "crm", self.open_crm, self.tr("Customer relationship management"), []),
                ("📝", self.tr("Sales Prompts/Templates"), "prompts", self.open_prompts_window, self.tr("Sales templates and prompts"), []),
            ]),
            
            # 4. Run (inchangé)
            ("⏯️", self.tr("Run"), "Run", self.open_manuelle_window, self.tr("Run Now"), []),
            
            # 5. AI Agent
            ("🧠", self.tr("AI Agent"), "ai_agent", None, self.tr("AI Assistant tools"), [
                ("🤖", self.tr("Auto-Responder"), "auto_responder", self.open_auto_responder, self.tr("Automatic response system"), []),
                ("👔", self.tr("Sales Assistant"), "sales_assistant", self.open_sales_assistant, self.tr("AI sales assistant"), []),
                ("🛠️", self.tr("Prompts & Tools"), "prompts_tools", self.open_prompts_tools, self.tr("AI prompts and tools"), []),
                ("🔍", self.tr("Competitor Analysis"), "competitor_analysis", self.open_competitor_analysis, self.tr("Analyze competitors"), []),
                ("👩‍💼", self.tr("Sales Assistant"), "sales_assistant_v2", self.open_sales_assistant_v2, self.tr("Enhanced sales assistant"), []),
                ("⚙️", self.tr("AI Workflows"), "ai_workflows", self.open_ai_workflows, self.tr("AI workflow automation"), []),
            ]),
            
            # 6. Finance
            ("💸", self.tr("Finance"), "finance", None, self.tr("Financial tools"), [
                ("🧾", self.tr("Invoices & Billing"), "invoices", self.open_invoices, self.tr("Invoice management"), []),
                ("📈", self.tr("Trader"), "trader", self.open_trader, self.tr("Trading tools"), []),
            ]),
            
            # 7. Upgrade
            ("🚀", self.tr("Upgrade"), "upgrade", self.open_upgrade_window, self.tr("Upgrade options"), []),
            
            # Anciens menus (regroupés)
            ("🗃️", self.tr("Legacy"), "legacy", None, self.tr("Old menu items"), [
                ("🧰", self.tr("Old Tools"), "old_tools", self.open_management, self.tr("Deprecated tools"), []),
                ("📜", self.tr("Old Protocols"), "protocoles", self.open_management, self.tr("Deprecated protocols"), []),
                ("📥", self.tr("Old Import Data"), "import", self.open_imports_window, self.tr("Deprecated import tools"), []),
                ("🗂️", self.tr("Old ADN Backup"), "backup", self.open_imports_window, self.tr("Deprecated backup"), []),
            ]),
        ]

        # Création des boutons de menu principal
        self.menu_buttons = []
        self.sub_menus = {}
        self.current_open_menu = None
        self.menu_button_refs = {}

        for icon, text, identifier, action, tooltip, sub_items in menu_items:
            button = QPushButton(f"{icon} {text}")
            button.setFixedHeight(36)
            button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #4b5563;
                    border: none;
                    font-size: 14px;
                    padding: 5px 10px;
                    border-radius: 4px;
                    transition: all 0.2s ease;
                }
                QPushButton:hover {
                    background-color: #e5e7eb;
                    color: #1f2937;
                    transform: translateY(-1px);
                }
            """)
            button.setToolTip(f"<b>{text}</b><br>{tooltip}")
            
            # Connecter l'action avec vérification du mode pro si nécessaire
            if action:
                if identifier in ['upgrade', 'home']:  # Toujours accessibles
                    button.clicked.connect(action)
                else:
                    button.clicked.connect(lambda _, f=action: self.check_pro_mode(f))
            
            if identifier not in ["home", "tools", "data", "support", "upgrade", "settings", "beta"]:
                self.menu_button_refs[text] = button
            
            if sub_items:
                menu = QMenu()
                menu.setStyleSheet("""
                    QMenu {
                        background-color: #ffffff;
                        border: 1px solid #d1d5db;
                        padding: 5px;
                        border-radius: 8px;
                        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
                    }
                    QMenu::item {
                        color: #4b5563;
                        padding: 8px 25px;
                        margin: 2px;
                        border-radius: 4px;
                        font-size: 13px;
                        min-width: 150px;
                    }
                    QMenu::item:selected {
                        background-color: #f3f4f6;
                        color: #111827;
                    }
                    QMenu::item:disabled {
                        color: #9ca3af;
                    }
                    QMenu::icon {
                        padding-left: 10px;
                    }
                """)

                for sub_icon, sub_text, sub_id, sub_action, sub_tooltip, nested_sub_items in sub_items:
                    if nested_sub_items:
                        submenu = QMenu(sub_text)
                        submenu.setStyleSheet(menu.styleSheet())
                        
                        for nest_icon, nest_text, nest_id, nest_action, nest_tooltip, _ in nested_sub_items:
                            action = submenu.addAction(f"{nest_icon} {nest_text}")
                            action.setToolTip(nest_tooltip)
                            if nest_action:
                                action.triggered.connect(lambda _, f=nest_action: self.check_pro_mode(f))
                        
                        menu.addMenu(submenu)
                    else:
                        action = menu.addAction(f"{sub_icon} {sub_text}")
                        action.setToolTip(sub_tooltip)
                        if sub_action:
                            action.triggered.connect(lambda _, f=sub_action: self.check_pro_mode(f))
                
                button.setMenu(menu)
            
            self.menu_bar.addWidget(button)
            self.menu_buttons.append(button)

        self.top_menu_layout.addLayout(self.menu_bar)
        self.top_menu_layout.addStretch()

        # --- Section de notification ---
        self.create_notif()
        self.top_menu_layout.addStretch()

        # --- Contrôles de fenêtre ---
        self.control_buttons_layout = QHBoxLayout()
        self.control_buttons_layout.setSpacing(5)

        minimize_button = QPushButton("—")
        minimize_button.setFixedSize(26, 26)
        minimize_button.setStyleSheet(self.get_control_button_style("minimize"))
        minimize_button.clicked.connect(self.minimize_window)

        maximize_button = QPushButton("□")
        maximize_button.setFixedSize(26, 26)
        maximize_button.setStyleSheet(self.get_control_button_style("maximize"))
        maximize_button.clicked.connect(self.maximize_window)

        close_button = QPushButton("✕")
        close_button.setFixedSize(26, 26)
        close_button.setStyleSheet(self.get_control_button_style("close"))
        close_button.clicked.connect(self.close_window)

        self.control_buttons_layout.addWidget(minimize_button)
        self.control_buttons_layout.addWidget(maximize_button)
        self.control_buttons_layout.addWidget(close_button)

        # --- Section utilisateur ---
        self.user_button = QPushButton(f"👤 {self.current_username}")
        self.user_button.setFixedHeight(36)
        self.user_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #4b5563;
                border: 1px solid #d1d5db;
                font-size: 14px;
                padding: 5px 15px 5px 10px;
                border-radius: 18px;
                min-width: 100px;
                transition: all 0.2s ease;
            }
            QPushButton:hover {
                background-color: #f3f4f6;
                transform: translateY(-1px);
            }
        """)

        # Menu utilisateur
        self.user_menu = QMenu()
        self.user_menu.setStyleSheet("""
            QMenu {
                background-color: #ffffff;
                border: 1px solid #d1d5db;
                padding: 8px;
                border-radius: 12px;
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
                margin-top: 5px;
            }
            QMenu::item {
                color: #4b5563;
                padding: 10px 25px;
                margin: 2px;
                border-radius: 6px;
                font-size: 13px;
                min-width: 180px;
            }
            QMenu::item:selected {
                background-color: #f3f4f6;
                color: #111827;
            }
            QMenu::separator {
                height: 1px;
                background: #e5e7eb;
                margin: 8px 2px;
            }
            QMenu::icon {
                padding-left: 10px;
            }
        """)
        
        # Actions principales du menu utilisateur
        self.login_action = self.user_menu.addAction("🔑 " + self.tr("Login"))
        self.logout_action = self.user_menu.addAction("🚪 " + self.tr("Logout"))
        self.user_menu.addSeparator()
        
        # Nouvelle section Plans (remplace Account Mode)
        plan_section = self.user_menu.addAction("📋 " + self.tr("Plans"))
        plan_section.setEnabled(False)
        self.marketing_plan_action = self.user_menu.addAction("   📢 " + self.tr("Marketing Plan"))
        self.sales_plan_action = self.user_menu.addAction("   💰 " + self.tr("Sales Plan"))
        self.user_menu.addSeparator()
        
        # Section mise à jour
        self.settings_action = self.user_menu.addAction("♻️ " + self.tr("Update"))
        
        # Sous-menu Settings
        settings_menu = self.user_menu.addMenu("⚙️ " + self.tr("Settings"))
        settings_menu.setStyleSheet(self.user_menu.styleSheet())
        
        settings_items = [
            ("🔌", self.tr("Add-On"), "add-on", self.add_on_page, self.tr("Add app")),
            ("📡", self.tr("Remote"), "remote", self.open_telecommande_window, self.tr("Remote control")),
            ("📦", self.tr("Installer"), "Installer", self.open_installer_window, self.tr("Add app")),
            ("🌐", self.tr("Connection"), "online_connect", self.connect_via_ssh, self.tr("Remote connection settings")),
            ("🗂️", self.tr("Instances"), "instances", self.open_instance, self.tr("Manage instances")),
            ("💎", self.tr("Upgrade"), "upgrade", self.open_upgrade_window, self.tr("Upgrade options")),
            ("📞", self.tr("Contact"), "contact", self.open_contact_window, self.tr("Contact us")),
            ("♟️", self.tr("Strategies"), "strategies", self.open_strategies_window, self.tr("Possible strategies")),
        ]
        
        for icon, text, identifier, action, tooltip in settings_items:
            act = settings_menu.addAction(f"{icon} {text}")
            act.setToolTip(tooltip)
            if action:
                act.triggered.connect(lambda _, f=action: self.check_pro_mode(f))
        
        self.user_menu.addSeparator()
        
        # Section compte
        account_section = self.user_menu.addAction("👤 " + self.tr("Account"))
        account_section.setEnabled(False)
        self.switch_action = self.user_menu.addAction("   👥 " + self.tr("Switch Account"))
        self.subscription_action = self.user_menu.addAction("   🛒 " + self.tr("Subscription"))
        self.my_persona_action = self.user_menu.addAction("   🎭 " + self.tr("My Persona"))
        
        # Menu Langue
        language_menu = self.user_menu.addMenu("   🌍 " + self.tr("Language"))
        language_menu.setStyleSheet(self.user_menu.styleSheet())
        
        language_items = [
            ("🗼", self.tr("French"), "french", lambda: self.switch_language("fr"), self.tr("French language")),
            ("🏰", self.tr("English"), "english", lambda: self.switch_language("en"), self.tr("English language")),
            ("🕋", self.tr("Arabic"), "arabic", lambda: self.switch_language("ar"), self.tr("Arabic language")),
            ("🕌", self.tr("Turkish"), "turkish", lambda: self.switch_language("tr"), self.tr("Turkish language")),
            ("🏖️", self.tr("Portuguese"), "portuguese", lambda: self.switch_language("pt"), self.tr("Portuguese language")),
        ]
        
        for icon, text, identifier, action, tooltip in language_items:
            act = language_menu.addAction(f"{icon} {text}")
            act.setToolTip(tooltip)
            if action:
                act.triggered.connect(action)
        
        # Connexions des signaux
        self.login_action.triggered.connect(self.user_login)
        self.logout_action.triggered.connect(self.user_logout)
        self.marketing_plan_action.triggered.connect(lambda: self.open_plan("marketing"))
        self.sales_plan_action.triggered.connect(lambda: self.open_plan("sales"))
        self.settings_action.triggered.connect(self.open_user_settings)
        self.switch_action.triggered.connect(self.switch_account)
        self.subscription_action.triggered.connect(self.open_subscription)
        self.my_persona_action.triggered.connect(self.open_my_persona)
        
        self.user_button.setMenu(self.user_menu)
        self.top_menu_layout.addWidget(self.user_button)

        # Ajouter les contrôles de fenêtre
        self.top_menu_layout.addLayout(self.control_buttons_layout)

        # Mettre à jour l'interface en fonction de l'état de connexion
        self.update_user_profile_section()
        self.update_menu_visibility()

        # Ajouter le menu top au layout principal
        self.main_layout.insertWidget(0, self.top_menu)

        # Mettre à jour les badges de notification
        self.update_notification_count()
        self.update_message_count()

    def check_pro_mode(self, action_function):
        """
        Vérifie si l'utilisateur est en mode pro avant d'exécuter une action.
        Affiche un message d'upgrade si nécessaire.
        """
        if self.is_enterprise_mode:
            action_function()
        else:
            QMessageBox.information(self, 
                                self.tr("Pro Feature"),
                                self.tr("This feature is only available in Pro mode. Please upgrade to access all professional features."),
                                QMessageBox.Ok)
            self.open_upgrade_window()

    def open_plan(self, plan_type):
        """
        Ouvre la fenêtre du plan spécifié (marketing ou sales)
        """
        if plan_type == "marketing":
            # Implémentation de la fenêtre du plan marketing
            print("Opening Marketing Plan")
        elif plan_type == "sales":
            # Implémentation de la fenêtre du plan sales
            print("Opening Sales Plan")

    # Nouvelles fonctions pour les nouveaux menus
    def open_ads_manager(self):
        """Ouvre le gestionnaire d'annonces"""
        if self.is_enterprise_mode:
            print("Opening Ads Manager")
        else:
            self.check_pro_mode(lambda: None)

    def open_email_sms(self):
        """Ouvre le gestionnaire d'emails et SMS"""
        if self.is_enterprise_mode:
            print("Opening Email & SMS Manager")
        else:
            self.check_pro_mode(lambda: None)

    def open_content_generator(self):
        """Ouvre le générateur de contenu"""
        if self.is_enterprise_mode:
            print("Opening Content Generator")
        else:
            self.check_pro_mode(lambda: None)

    def open_project_management(self):
        """Ouvre la gestion de projets"""
        if self.is_enterprise_mode:
            print("Opening Project Management")
        else:
            self.check_pro_mode(lambda: None)

    def open_sav(self):
        """Ouvre le module SAV"""
        if self.is_enterprise_mode:
            print("Opening SAV Module")
        else:
            self.check_pro_mode(lambda: None)

    def open_dms_quotes(self):
        """Ouvre la gestion de documents et devis"""
        if self.is_enterprise_mode:
            print("Opening DMS & Quotes")
        else:
            self.check_pro_mode(lambda: None)

    def open_crm(self):
        """Ouvre le CRM"""
        if self.is_enterprise_mode:
            print("Opening CRM")
        else:
            self.check_pro_mode(lambda: None)

    def open_auto_responder(self):
        """Ouvre l'auto-répondeur"""
        if self.is_enterprise_mode:
            print("Opening Auto-Responder")
        else:
            self.check_pro_mode(lambda: None)

    def open_sales_assistant(self):
        """Ouvre l'assistant commercial"""
        if self.is_enterprise_mode:
            print("Opening Sales Assistant")
        else:
            self.check_pro_mode(lambda: None)

    def open_prompts_tools(self):
        """Ouvre les prompts et outils"""
        if self.is_enterprise_mode:
            print("Opening Prompts & Tools")
        else:
            self.check_pro_mode(lambda: None)

    def open_competitor_analysis(self):
        """Ouvre l'analyse des concurrents"""
        if self.is_enterprise_mode:
            print("Opening Competitor Analysis")
        else:
            self.check_pro_mode(lambda: None)

    def open_sales_assistant_v2(self):
        """Ouvre la nouvelle version de l'assistant commercial"""
        if self.is_enterprise_mode:
            print("Opening Sales Assistant V2")
        else:
            self.check_pro_mode(lambda: None)

    def open_ai_workflows(self):
        """Ouvre les workflows AI"""
        if self.is_enterprise_mode:
            print("Opening AI Workflows")
        else:
            self.check_pro_mode(lambda: None)

    def open_invoices(self):
        """Ouvre la gestion des factures"""
        if self.is_enterprise_mode:
            print("Opening Invoices & Billing")
        else:
            self.check_pro_mode(lambda: None)

    def open_trader(self):
        """Ouvre les outils de trading"""
        if self.is_enterprise_mode:
            print("Opening Trader Tools")
        else:
            self.check_pro_mode(lambda: None)