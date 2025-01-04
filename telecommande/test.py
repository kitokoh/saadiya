def initUI(self):
        self.setWindowTitle("Nova360 AI - Remote Control")
        self.setWindowIcon(QIcon('../resources/icons/robot-icons-30504-Windows.ico'))  # Assurez-vous que le chemin de l'icône est correct

        self.setFixedSize(450, 700)  # Set fixed size for the window

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Digital screen with modern styling
        self.screen = QLabel("Ready to Control")
        self.screen.setFixedHeight(self.height() // 5)
        self.screen.setAlignment(Qt.AlignCenter)
        self.apply_shadow_effect(self.screen)
        self.screen.setStyleSheet(self.get_screen_stylesheet())
        main_layout.addWidget(self.screen)

        # Central area: circular buttons and small buttons
        central_layout = QHBoxLayout()

        # Small buttons on the left
        left_buttons = QVBoxLayout()
        # Dictionnaire des actions par nom de bouton
        button_actions = {
            "Fb Robot": self.run_fb_robot,
            "Multi Fb": self.run_fb_robot,  # Vous devez créer ces méthodes si elles n'existent pas encore
            "WA": self.run_fb_robot,
            "Insta": self.run_fb_robot
        }

        # Création des boutons avec des actions spécifiques
        for name, icon in [("Fb Robot", "icons/fb.png"), ("Multi Fb", "icons/multi_fb.png"), 
                        ("WA", "icons/wa.png"), ("Insta", "icons/insta.png")]:
            btn = self.create_small_button(name, icon)
            self.apply_shadow_effect(btn)
            left_buttons.addWidget(btn)

            # Connecter chaque bouton à son action
            if name in button_actions:
                btn.clicked.connect(button_actions[name])





        # Circular buttons in the center
        circle_buttons_layout = QVBoxLayout()
        self.open_panel_btn = self.create_circular_button("Open Panel", "icons/panel.png")
        self.start_robots_btn = self.create_circular_button("Start Robots", "icons/robot.png")
        self.choice_module_btn = self.create_circular_button("Choice Module", "icons/module.png")
        
        for btn in [self.open_panel_btn, self.start_robots_btn, self.choice_module_btn]:
            self.apply_shadow_effect(btn)
            circle_buttons_layout.addWidget(btn)

        # Small buttons on the right
        right_buttons = QVBoxLayout()
        for name, icon in [("Pin", "icons/pin.png"), ("X", "icons/x.png"), 
                           ("In", "icons/linkedin.png"), ("YTB", "icons/ytb.png")]:
            btn = self.create_small_button(name, icon)
            self.apply_shadow_effect(btn)
            right_buttons.addWidget(btn)

        # Add layouts to the central layout
        central_layout.addLayout(left_buttons)
        central_layout.addLayout(circle_buttons_layout)
        central_layout.addLayout(right_buttons)

        main_layout.addLayout(central_layout)
        # Toggle theme button
        self.toggle_theme_btn = QPushButton("Toggle Theme")
        self.toggle_theme_btn.clicked.connect(self.toggle_theme)
        self.apply_shadow_effect(self.toggle_theme_btn)
        self.toggle_theme_btn.setStyleSheet(self.get_toggle_button_stylesheet())
        main_layout.addWidget(self.toggle_theme_btn)


        # Footer with sleek design
        footer = QLabel("© 2024 Nova360 AI - Remote Control")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("""
            QLabel {
                color: #aaa;
                font-size: 12px;
                font-style: italic;
                margin-top: 10px;
            }
        """)
        self.apply_shadow_effect(footer)
        main_layout.addWidget(footer)

        # Apply the main layout
        self.setLayout(main_layout)

        # Create a label to show time remaining
        self.timer_label = QLabel("Temps restant : 00:00:00")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.apply_shadow_effect(self.timer_label)
        main_layout.addWidget(self.timer_label)

        # Connect main buttons for light effect
        self.open_panel_btn.clicked.connect(lambda: self.activate_light("Open Panel Activated"))
        self.start_robots_btn.clicked.connect(lambda: self.activate_light("Robots Started"))
        self.choice_module_btn.clicked.connect(self.start_countdown)
        # Buttons to trigger the execution of external programs
        self.fb_robot_btn = self.create_small_button("Fb Robot", "icons/fb.png")
        self.pin_btn = self.create_small_button("Pin", "icons/pin.png")
        self.fb_robot_btn.clicked.connect(self.run_fb_robot)
        self.pin_btn.clicked.connect(self.run_pin)

        # Initialize the timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.time_remaining = QTime(0, 5, 0)  # Example: Start a 5-minute countdown


        # Splitter principal
        self.splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(self.splitter)


        # Section des boutons
        self.button_tabs = QTabWidget()
        self.splitter.addWidget(self.button_tabs)

 # Section des terminaux
        self.terminal_tabs = QTabWidget()
        self.terminal_tabs.setTabsClosable(True)
        self.terminal_tabs.tabCloseRequested.connect(self.close_terminal_tab)
        self.splitter.addWidget(self.terminal_tabs)