
    
        # from media
    def create_database(self):
            """Crée la base de données SQLite avec les tables media, media_type, et category."""
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()

            # Table pour les types de médias
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS media_type (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL UNIQUE,
                    label TEXT,
                    description TEXT,
                    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    date_modification TIMESTAMP,
                    date_suppression TIMESTAMP
                )
            ''')

            # Table pour les catégories
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS category (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    label TEXT,
                    description TEXT,
                    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    date_modification TIMESTAMP,
                    date_suppression TIMESTAMP
                )
            ''')

            # Table pour les médias
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS media (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    description TEXT,
                    preview_path TEXT NOT NULL,
                    type_id INTEGER NOT NULL,
                    category_id INTEGER,
                    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    date_modification TIMESTAMP,
                    date_suppression TIMESTAMP,
                    est_supprime BOOLEAN DEFAULT 0,
                    FOREIGN KEY (type_id) REFERENCES media_type(id),
                    FOREIGN KEY (category_id) REFERENCES category(id)
                )
            ''')

            # Insérer les types de médias par défaut (media1 à media10)
            for i in range(1, 11):
                cursor.execute('''
                    INSERT OR IGNORE INTO media_type (type, label, description) VALUES (?, ?, ?)
                ''', (f'media{i}', f'Media {i}', f'Description for Media {i}'))

            # Insérer une catégorie par défaut
            cursor.execute('''
                INSERT OR IGNORE INTO category (name, label, description) VALUES (?, ?, ?)
            ''', ('Default', 'Default Category', 'Default category description'))

            conn.commit()
            conn.close()

        # from groups

    def init_db():
        """Initialise la base de données SQLite avec des tables et des données par défaut."""
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Table pour les catégories
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                label TEXT,
                description TEXT,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP,
                date_suppression TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS category_group (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                label TEXT,
                description TEXT,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP,
                date_suppression TIMESTAMP
            )
        ''')
        # Table pour les réseaux sociaux
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reseaux_sociaux (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP,
                date_suppression TIMESTAMP
            )
        ''')

        # Table pour les types de médias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS media_type (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL UNIQUE,
                label TEXT,
                description TEXT,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP,
                date_suppression TIMESTAMP
            )
        ''')

        # Table pour les médias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS media (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                description TEXT,
                preview_path TEXT NOT NULL,
                type_id INTEGER NOT NULL,
                category_id INTEGER,
                date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP,
                date_suppression TIMESTAMP,
                est_supprime BOOLEAN DEFAULT 0,
                FOREIGN KEY (type_id) REFERENCES media_type(id),
                FOREIGN KEY (category_id) REFERENCES category(id)
            )
        ''')

        # Table pour les robots
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS robots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                label TEXT,
                description TEXT,
                creation_date TEXT,
                category TEXT,
                status TEXT,
                reseau_social_id INTEGER,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP,
                date_suppression TIMESTAMP,
                FOREIGN KEY(reseau_social_id) REFERENCES reseaux_sociaux(id)
            )
        ''')

        # Table de liaison entre robots et types de médias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS robot_media_type (
                robot_id INTEGER,
                media_type_id INTEGER,
                FOREIGN KEY(robot_id) REFERENCES robots(id),
                FOREIGN KEY(media_type_id) REFERENCES media_type(id)
            )
        ''')

        # Table pour les groupes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                link TEXT NOT NULL,
                remarks TEXT,
                category_group_id INTEGER,
                description TEXT,
                keywords TEXT,
                FOREIGN KEY(category_group_id) REFERENCES category_group(id)
            )
        ''')

        # Table de liaison entre groupes et robots
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS group_robot (
                group_id INTEGER,
                robot_id INTEGER,
                FOREIGN KEY(group_id) REFERENCES groups(id),
                FOREIGN KEY(robot_id) REFERENCES robots(id)
            )
        ''')

        # Table pour les identifiants
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS identifiant (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                reseau_social_id INTEGER,
                robot_id INTEGER,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP,
                date_suppression TIMESTAMP,
                FOREIGN KEY(reseau_social_id) REFERENCES reseaux_sociaux(id),
                FOREIGN KEY(robot_id) REFERENCES robots(id)
            )
        ''')


        # Table pour les archives
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS archive (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                robot_id INTEGER,
                reseau_social_id INTEGER,
                filename TEXT NOT NULL,
                content TEXT NOT NULL,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP,
                date_suppression TIMESTAMP,
                version INTEGER DEFAULT 1,
                FOREIGN KEY(robot_id) REFERENCES robots(id),
                FOREIGN KEY(reseau_social_id) REFERENCES reseaux_sociaux(id)
            )
        ''')

        # Insertion des données par défaut

        # Catégories par défaut
        cursor.execute('''
            INSERT OR IGNORE INTO category (name, label, description)
            VALUES (?, ?, ?)
        ''', ('Default', 'Default Category', 'Default category description'))

        # Réseaux sociaux par défaut
        reseaux_sociaux = [
            ('Facebook', 'Réseau social Facebook'),
            ('WhatsApp', 'Application de messagerie WhatsApp'),
            ('Twitter', 'Réseau social Twitter')
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO reseaux_sociaux (name, description)
            VALUES (?, ?)
        ''', reseaux_sociaux)

        # Types de médias par défaut
        media_types = [
            ('Image', 'Image', 'Type de média pour les images'),
            ('Video', 'Vidéo', 'Type de média pour les vidéos')
        ] + [(f'media{i}', f'Media {i}', f'Description for Media {i}') for i in range(1, 11)]
        cursor.executemany('''
            INSERT OR IGNORE INTO media_type (type, label, description)
            VALUES (?, ?, ?)
        ''', media_types)

        # Robots par défaut
        robots = [
            ('Robot1', 'Robot 1', 'Description Robot 1', '2023-01-01', 'Category1', 'Active', 1),
            ('Robot2', 'Robot 2', 'Description Robot 2', '2023-01-01', 'Category2', 'Inactive', 2)
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO robots (name, label, description, creation_date, category, status, reseau_social_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', robots)

        # Groupes par défaut
        groups = [
            ('Group1', 'http://example.com/group1', 'Remarks 1', 1, 'Description 1', 'Keywords1'),
            ('Group2', 'http://example.com/group2', 'Remarks 2', 1, 'Description 2', 'Keywords2')
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO groups (name, link, remarks, category_group_id, description, keywords)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', groups)

        conn.commit()
        conn.close()



