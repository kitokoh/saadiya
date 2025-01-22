ici nous allons definir les relation entre les table et les futurs api necssaire 
les tables aurront ce qui leur faut 

les tables 

dans groupes on a 3 

def init_db():
    """Initialise la base de données SQLite."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            link TEXT NOT NULL,
            remarks TEXT,
            category TEXT,
            description TEXT,
            keywords TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS robots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            creation_date TEXT,
            category TEXT,
            status TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS group_robot (
            group_id INTEGER,
            robot_id INTEGER,
            FOREIGN KEY(group_id) REFERENCES groups(id),
            FOREIGN KEY(robot_id) REFERENCES robots(id)
        )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_name ON groups (name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON groups (category)')
    conn.commit()
    conn.close()
