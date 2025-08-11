import sqlite3
import os

def get_db_path():
    # This should be configured more robustly in a real app
    return "/app/leopardo_v2/app/data/leopardo_v2.db"

def init_data_db():
    """Initialize database with tables for the application data"""
    db_path = get_db_path()
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crm (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            status TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            type TEXT,
            path TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_management (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            status TEXT
        )
    ''')

    conn.commit()
    conn.close()

def init_db():
    """Initialize database with complete dataset"""
    db_path = get_db_path()
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detection_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            platform TEXT NOT NULL,
            response_template TEXT NOT NULL,
            action_type TEXT NOT NULL
        )
    ''')

    # Check existing data
    cursor.execute("SELECT COUNT(*) FROM detection_rules")
    if cursor.fetchone()[0] == 0:
        # Insert complete dataset
        rules = [
            ("whatsapp", "whatsapp", "Complete WhatsApp automation", "whatsapp_auto"),
            ("whatsapp message", "whatsapp", "Send personal WhatsApp message", "whatsapp_personal"),
            ("whatsapp group", "whatsapp", "Send message to WhatsApp group", "whatsapp_group"),
            ("whatsapp campaign", "whatsapp", "Launch WhatsApp campaign", "whatsapp_campaign"),
            ("automate whatsapp", "whatsapp", "Automate WhatsApp replies", "whatsapp_auto_reply"),
            ("instagram", "instagram", "Create Instagram post", "instagram_post"),
            ("instagram story", "instagram", "Create Instagram story", "instagram_story"),
            ("instagram reels", "instagram", "Create Instagram Reel", "instagram_reel"),
            ("instagram campaign", "instagram", "Launch Instagram ad campaign", "instagram_ads"),
            ("instagram hashtag", "instagram", "Generate optimized hashtags", "instagram_hashtags"),
            ("facebook", "facebook", "Create Facebook post", "facebook_post"),
            ("facebook ad", "facebook", "Launch Facebook ad", "facebook_ads"),
            ("facebook page", "facebook", "Optimize your Facebook page", "facebook_page"),
            ("linkedin", "linkedin", "Create LinkedIn post", "linkedin_post"),
            ("tiktok", "tiktok", "Create TikTok video", "tiktok_video"),
            ("youtube", "youtube", "Optimize YouTube video", "youtube_optimize"),
            ("email", "email", "Create email campaign", "email_campaign"),
            ("newsletter", "email", "Create newsletter", "email_newsletter"),
            ("strategy", "general", "Develop marketing strategy", "marketing_strategy"),
            ("analysis", "analytics", "Analyze performance", "performance_analysis"),
            ("seo", "seo", "SEO optimization", "seo_optimization"),
            ("content", "content", "Plan content", "content_planning")
        ]

        cursor.executemany('''
            INSERT INTO detection_rules (keyword, platform, response_template, action_type)
            VALUES (?, ?, ?, ?)
        ''', rules)
        conn.commit()

    conn.close()
    return db_path
