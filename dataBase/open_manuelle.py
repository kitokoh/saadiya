    def setup_database(self):
        """Initialize database connection"""
        self.conn = sqlite3.connect(DB_PATH_notes)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_size INTEGER DEFAULT 10,
                last_description TEXT,
                last_robot TEXT,
                last_network TEXT,
                chrome_path TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS autredescription (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                network_name TEXT NOT NULL,
                robot_name TEXT NOT NULL,
                description TEXT,
                UNIQUE(network_name, robot_name)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                network_name TEXT NOT NULL,
                robot_name TEXT NOT NULL,
                script_name TEXT NOT NULL,
                scheduled_time DATETIME NOT NULL,
                status TEXT DEFAULT 'pending'
            )
        ''')
    
        self.cursor.execute('SELECT COUNT(*) FROM settings')
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute('''
                INSERT INTO settings (group_size, chrome_path) 
                VALUES (10, 'C:/Program Files/Google/Chrome/Application/chrome.exe')
            ''')
            self.conn.commit()
