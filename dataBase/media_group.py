import os
import sqlite3
import os
import sqlite3
from datetime import datetime, timedelta
import random
class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialise la base de données avec les tables et données par défaut"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            self._create_tables(cursor)
            self._insert_default_data(cursor)
            conn.commit()
    
    def _create_tables(self, cursor):
        """Crée toutes les tables nécessaires"""
        # Table des catégories
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
        
        # Table des réseaux sociaux
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
        
        # Table des types de médias
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
        
        # Table des médias
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
        
        # Table des robots
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
        
        # Tables de liaison
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS robot_media_type (
                robot_id INTEGER,
                media_type_id INTEGER,
                PRIMARY KEY (robot_id, media_type_id),
                FOREIGN KEY(robot_id) REFERENCES robots(id),
                FOREIGN KEY(media_type_id) REFERENCES media_type(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                link TEXT NOT NULL UNIQUE,
                remarks TEXT,
                category_group_id INTEGER,
                description TEXT,
                keywords TEXT,
                FOREIGN KEY(category_group_id) REFERENCES category_group(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS group_robot (
                group_id INTEGER,
                robot_id INTEGER,
                PRIMARY KEY (group_id, robot_id),
                FOREIGN KEY(group_id) REFERENCES groups(id),
                FOREIGN KEY(robot_id) REFERENCES robots(id)
            )
        ''')
        
        # Table des identifiants
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
        
        # Table des archives
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
    
    # def _insert_default_data(self, cursor):
    #     """Insère les données par défaut dans les tables"""
    #     # Catégorie par défaut
    #     cursor.execute('''
    #         INSERT OR IGNORE INTO category (name, label, description)
    #         VALUES (?, ?, ?)
    #     ''', ('Default', 'Default Category', 'Default category description'))
        
    #     # Réseaux sociaux par défaut
    #     reseaux_sociaux = [
    #         ('Facebook', 'Réseau social Facebook'),
    #         ('WhatsApp', 'Application de messagerie WhatsApp'),
    #         ('Twitter', 'Réseau social Twitter')
    #     ]
    #     cursor.executemany('''
    #         INSERT OR IGNORE INTO reseaux_sociaux (name, description)
    #         VALUES (?, ?)
    #     ''', reseaux_sociaux)
        
    #     # Types de médias par défaut
    #     media_types = [
    #         ('Image', 'Image', 'Type de média pour les images'),
    #         ('Video', 'Vidéo', 'Type de média pour les vidéos')
    #     ] + [(f'media{i}', f'Media {i}', f'Description for Media {i}') for i in range(1, 11)]
    #     cursor.executemany('''
    #         INSERT OR IGNORE INTO media_type (type, label, description)
    #         VALUES (?, ?, ?)
    #     ''', media_types)
        
    #     # Robots par défaut
    #     robots = [
    #         ('Robot1', 'Robot 1', 'Description Robot 1', '2023-01-01', 'Category1', 'Active', 1),
    #         ('Robot2', 'Robot 2', 'Description Robot 2', '2023-01-01', 'Category2', 'Inactive', 2)
    #     ]
    #     cursor.executemany('''
    #         INSERT OR IGNORE INTO robots (name, label, description, creation_date, category, status, reseau_social_id)
    #         VALUES (?, ?, ?, ?, ?, ?, ?)
    #     ''', robots)
        
    #     # Groupes par défaut
    #     groups = [
    #         ('Group1', 'https://www.facebook.com/groups/865531597256624', '', 1, '', ''),
    #         ('Group2', 'https://www.facebook.com/groups/865531597256624', '', 1, '', ''),
    #         ('Group3', 'https://www.facebook.com/groups/865531597256624', '', 1, '', ''),
    #         ('Group4', 'https://www.facebook.com/groups/865531597256624', '', 1, '', ''),
    #         ('Group5', 'https://www.facebook.com/groups/865531597256624', '', 1, '', ''),
    #         ('Group6', 'https://www.facebook.com/groups/865531597256624', '', 1, '', ''),
    #         ('Group7', 'https://www.facebook.com/groups/865531597256624', '', 1, '', ''),
    #         ('Group8', 'https://www.facebook.com/groups/865531597256624', '', 1, '', ''),
    #         ('Group9', 'https://www.facebook.com/groups/865531597256624', '', 1, '', ''),
    #         ('Group10', 'https://www.facebook.com/groups/1533868653533875/', '', 1, '', ''),
    #         ('Group11', 'https://www.facebook.com/groups/2309210009291237/', '', 1, '', ''),
    #         ('Group12', 'https://www.facebook.com/groups/119929018423623/', '', 1, '', ''),
    #         ('Group13', 'https://www.facebook.com/groups/1914166852277174/', '', 1, '', ''),
    #         ('Group14', 'https://www.facebook.com/groups/249218873426277/', '', 1, '', ''),
    #         ('Group15', 'https://www.facebook.com/groups/382896815533960/', '', 1, '', ''),
    #         ('Group16', 'https://www.facebook.com/groups/501089116661238/', '', 1, '', ''),
    #         ('Group17', 'https://www.facebook.com/groups/313539295727010/', '', 1, '', ''),
    #         ('Group18', 'https://www.facebook.com/groups/2939025449709547/', '', 1, '', ''),
    #         ('Group19', 'https://www.facebook.com/groups/753693605432949/', '', 1, '', ''),
    #         ('Group20', 'https://www.facebook.com/groups/785886162129417/', '', 1, '', ''),
    #         ('Group21', 'https://www.facebook.com/groups/887867051269561/', '', 1, '', ''),
    #         ('Group22', 'https://www.facebook.com/groups/pressegypt/', '', 1, '', ''),
    #         ('Group23', 'https://www.facebook.com/groups/208073056046127/', '', 1, '', ''),
    #         ('Group24', 'https://www.facebook.com/groups/1335838006878557/', '', 1, '', ''),
    #         ('Group25', 'https://www.facebook.com/groups/1980706472159891/', '', 1, '', ''),
    #         ('Group26', 'https://www.facebook.com/groups/2245742298849513/', '', 1, '', ''),
    #         ('Group27', 'https://www.facebook.com/groups/266563507144846/', '', 1, '', ''),
    #         ('Group28', 'https://www.facebook.com/groups/1713003238853136/', '', 1, '', ''),
    #         ('Group29', 'https://www.facebook.com/groups/668946039826955', '', 1, '', ''),
    #         ('Group30', 'https://www.facebook.com/groups/1090039738545144/', '', 1, '', ''),
    #     ]
    #     cursor.executemany('''
    #         INSERT OR IGNORE INTO groups (name, link, remarks, category_group_id, description, keywords)
    #         VALUES (?, ?, ?, ?, ?, ?)
    #     ''', groups)
    
    # def get_connection(self):
    #     """Retourne une nouvelle connexion à la base de données"""
    #     return sqlite3.connect(self.db_path)








    def _insert_default_data(self, cursor):
        """Insère des données fictives complètes dans toutes les tables"""
        self._insert_categories(cursor)
        self._insert_category_groups(cursor)
        self._insert_social_networks(cursor)
        self._insert_media_types(cursor)
        self._insert_robots(cursor)
        self._insert_groups(cursor)
        self._insert_media(cursor)
        self._insert_robot_media_types(cursor)
        self._insert_group_robots(cursor)
        self._insert_credentials(cursor)
        self._insert_archives(cursor)
    
    def _insert_categories(self, cursor):
        categories = [
            ('Actualités', 'Actualités', 'Catégorie pour les actualités'),
            ('Technologie', 'Tech', 'Tout sur la technologie'),
            ('Sport', 'Sport', 'Actualités sportives'),
            ('Divertissement', 'Divertissement', 'Films, séries, célébrités'),
            ('Politique', 'Politique', 'Actualités politiques')
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO category (name, label, description)
            VALUES (?, ?, ?)
        ''', categories)
    
    def _insert_category_groups(self, cursor):
        category_groups = [
            ('Public', 'Groupes publics', 'Groupes accessibles à tous'),
            ('Privé', 'Groupes privés', 'Groupes sur invitation seulement'),
            ('Professionnel', 'Groupes pro', 'Groupes professionnels'),
            ('Local', 'Groupes locaux', 'Groupes régionaux')
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO category_group (name, label, description)
            VALUES (?, ?, ?)
        ''', category_groups)
    
    def _insert_social_networks(self, cursor):
        networks = [
            ('Facebook', 'Réseau social le plus populaire'),
            ('Twitter', 'Micro-blogging'),
            ('WhatsApp', 'Messagerie instantanée'),
            ('LinkedIn', 'Réseau professionnel'),
            ('Instagram', 'Partage de photos et vidéos'),
            ('Telegram', 'Messagerie sécurisée')
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO reseaux_sociaux (name, description)
            VALUES (?, ?)
        ''', networks)
    
    def _insert_media_types(self, cursor):
        types = [
            ('Image', 'Image', 'Média de type image'),
            ('Video', 'Vidéo', 'Média de type vidéo'),
            ('GIF', 'GIF animé', 'Animation courte'),
            ('PDF', 'Document PDF', 'Document portable'),
            ('Audio', 'Fichier audio', 'Podcast ou musique')
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO media_type (type, label, description)
            VALUES (?, ?, ?)
        ''', types)
    
    def _insert_robots(self, cursor):
        robots = [
            ('BotActualites', 'Bot Actualités', 'Collecte les dernières actualités', '2023-01-15', 'Actualités', 'Actif', 1),
            ('BotTech', 'Bot Technologie', 'Surveille les tendances tech', '2023-02-20', 'Technologie', 'Actif', 2),
            ('BotSports', 'Bot Sports', 'Agrégateur de nouvelles sportives', '2023-03-10', 'Sport', 'Inactif', 1),
            ('BotPolitique', 'Bot Politique', 'Analyse les discours politiques', '2023-04-05', 'Politique', 'Actif', 3),
            ('BotDivertissement', 'Bot Divertissement', 'Surveille les célébrités', '2023-05-12', 'Divertissement', 'Actif', 4)
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO robots (name, label, description, creation_date, category, status, reseau_social_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', robots)
    
    def _insert_groups(self, cursor):
        groups = [
            ('Tech Innovators', 'https://facebook.com/groups/techinnovators', 'Groupe pour innovateurs', 3, 'Partagez vos inventions', 'tech,innovation'),
            ('Sports Fans', 'https://facebook.com/groups/sportsfans', 'Communauté sportive', 1, 'Pour les passionnés de sport', 'sport,football'),
            ('News Analyzers', 'https://facebook.com/groups/newsanalyzers', 'Analyse critique', 2, 'Débats sur l\'actualité', 'news,politique'),
            ('Cinéma Club', 'https://facebook.com/groups/cinemaclub', 'Amateurs de films', 1, 'Critiques de films', 'cinema,films'),
            ('Local Community', 'https://facebook.com/groups/localcommunity', 'Vie locale', 4, 'Événements locaux', 'local,ville')
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO groups (name, link, remarks, category_group_id, description, keywords)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', groups)
    
    def _insert_media(self, cursor):
        media = [
            ('Logo Tech', 'Logo du groupe Tech', '/media/tech_logo.jpg', 1, 2, datetime.now().strftime('%Y-%m-%d'), None, None, 0),
            ('Vidéo présentation', 'Vidéo de présentation', '/media/presentation.mp4', 2, 1, datetime.now().strftime('%Y-%m-%d'), None, None, 0),
            ('Infographie', 'Infographie statistique', '/media/infographic.png', 1, 3, (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'), None, None, 0),
            ('Podcast', 'Épisode podcast', '/media/podcast.mp3', 5, 4, (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d'), None, None, 0),
            ('Documentation', 'Guide utilisateur', '/media/guide.pdf', 4, 5, (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'), None, None, 0)
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO media (nom, description, preview_path, type_id, category_id, date_ajout, date_modification, date_suppression, est_supprime)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', media)
    
    def _insert_robot_media_types(self, cursor):
        associations = [
            (1, 1), (1, 2),  # BotActualites peut utiliser Images et Vidéos
            (2, 1), (2, 4),   # BotTech peut utiliser Images et PDFs
            (3, 1), (3, 2),   # BotSports peut utiliser Images et Vidéos
            (4, 1), (4, 4),   # BotPolitique peut utiliser Images et PDFs
            (5, 1), (5, 2), (5, 3)  # BotDivertissement peut utiliser Images, Vidéos et GIFs
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO robot_media_type (robot_id, media_type_id)
            VALUES (?, ?)
        ''', associations)
    
    def _insert_group_robots(self, cursor):
        associations = [
            (1, 2),  # Tech Innovators -> BotTech
            (2, 3),  # Sports Fans -> BotSports
            (3, 1), (3, 4),  # News Analyzers -> BotActualites et BotPolitique
            (4, 5),  # Cinéma Club -> BotDivertissement
            (5, 1)   # Local Community -> BotActualites
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO group_robot (group_id, robot_id)
            VALUES (?, ?)
        ''', associations)
    
    def _insert_credentials(self, cursor):
        credentials = [
            ('fb_bot1', 'securepass123', 1, 1),
            ('tw_bot2', 'twitterpass456', 2, 2),
            ('wa_bot3', 'whatsapp789', 3, 3),
            ('ig_bot5', 'instapass101', 5, 5),
            ('tg_bot4', 'telegram202', 6, 4)
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO identifiant (username, password, reseau_social_id, robot_id)
            VALUES (?, ?, ?, ?)
        ''', credentials)
    
    def _insert_archives(self, cursor):
        archives = []
        for i in range(1, 6):  # Pour chaque robot
            for j in range(3):   # 3 archives par robot
                archives.append((
                    i,
                    random.randint(1, 6),  # réseau social aléatoire
                    f'report_{i}_{j}.json',
                    f'{{"data": "archive content for robot {i}", "version": {j+1}}}',
                    (datetime.now() - timedelta(days=j*2)).strftime('%Y-%m-%d'),
                    None,
                    None,
                    j+1
                ))
        
        cursor.executemany('''
            INSERT OR IGNORE INTO archive (robot_id, reseau_social_id, filename, content, date_creation, date_modification, date_suppression, version)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', archives)
    
    def get_connection(self):
        """Retourne une nouvelle connexion à la base de données"""
        return sqlite3.connect(self.db_path)

if __name__ == "__main__":
    print("Création de la base de données et insertion des données fictives...")
    
    # Initialisation de la base de données
    from imports import DB_PATH
    db_manager = DatabaseManager(DB_PATH)
    
    # Vérification que les données ont bien été insérées
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        
        # Comptage des entrées dans chaque table
        tables = [
            'category', 'category_group', 'reseaux_sociaux', 
            'media_type', 'robots', 'groups', 'media',
            'robot_media_type', 'group_robot', 'identifiant', 'archive'
        ]
        
        print("\nVérification des données insérées:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"- {table}: {count} enregistrements")
    
    print(f"\nBase de données créée avec succès: {DB_PATH}")
