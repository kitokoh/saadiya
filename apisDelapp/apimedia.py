from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_PATH = 'media.db'

# Helper functions
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def close_db_connection(conn):
    conn.close()

# Media Type Endpoints
@app.route('/api/media_types', methods=['GET'])
def get_media_types():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM media_type WHERE date_suppression IS NULL')
    media_types = cursor.fetchall()
    close_db_connection(conn)
    return jsonify([dict(media_type) for media_type in media_types])

@app.route('/api/media_types/<int:type_id>', methods=['GET'])
def get_media_type(type_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM media_type WHERE id = ? AND date_suppression IS NULL', (type_id,))
    media_type = cursor.fetchone()
    close_db_connection(conn)
    if media_type:
        return jsonify(dict(media_type))
    return jsonify({'error': 'Media type not found'}), 404

# Category Endpoints
@app.route('/api/categories', methods=['GET'])
def get_categories():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM category WHERE date_suppression IS NULL')
    categories = cursor.fetchall()
    close_db_connection(conn)
    return jsonify([dict(category) for category in categories])

@app.route('/api/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM category WHERE id = ? AND date_suppression IS NULL', (category_id,))
    category = cursor.fetchone()
    close_db_connection(conn)
    if category:
        return jsonify(dict(category))
    return jsonify({'error': 'Category not found'}), 404

# Media Endpoints
@app.route('/api/media', methods=['GET'])
def get_all_media():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT m.*, mt.type as media_type, c.name as category_name 
        FROM media m
        JOIN media_type mt ON m.type_id = mt.id
        LEFT JOIN category c ON m.category_id = c.id
        WHERE m.date_suppression IS NULL
    ''')
    media_items = cursor.fetchall()
    close_db_connection(conn)
    return jsonify([dict(media) for media in media_items])

@app.route('/api/media/<int:media_id>', methods=['GET'])
def get_media(media_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT m.*, mt.type as media_type, c.name as category_name 
        FROM media m
        JOIN media_type mt ON m.type_id = mt.id
        LEFT JOIN category c ON m.category_id = c.id
        WHERE m.id = ? AND m.date_suppression IS NULL
    ''', (media_id,))
    media = cursor.fetchone()
    close_db_connection(conn)
    if media:
        return jsonify(dict(media))
    return jsonify({'error': 'Media not found'}), 404

@app.route('/api/media', methods=['POST'])
def add_media():
    data = request.get_json()
    required_fields = ['nom', 'preview_path', 'type_id']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO media (
                nom, description, preview_path, type_id, category_id, date_modification
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['nom'],
            data.get('description'),
            data['preview_path'],
            data['type_id'],
            data.get('category_id'),
            datetime.now()
        ))
        conn.commit()
        media_id = cursor.lastrowid
        close_db_connection(conn)
        return jsonify({'id': media_id, 'message': 'Media added successfully'}), 201
    except sqlite3.IntegrityError as e:
        close_db_connection(conn)
        return jsonify({'error': str(e)}), 400

@app.route('/api/media/<int:media_id>', methods=['PUT'])
def update_media(media_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if media exists
    cursor.execute('SELECT id FROM media WHERE id = ? AND date_suppression IS NULL', (media_id,))
    if not cursor.fetchone():
        close_db_connection(conn)
        return jsonify({'error': 'Media not found'}), 404
    
    try:
        cursor.execute('''
            UPDATE media SET
                nom = COALESCE(?, nom),
                description = COALESCE(?, description),
                preview_path = COALESCE(?, preview_path),
                type_id = COALESCE(?, type_id),
                category_id = COALESCE(?, category_id),
                date_modification = ?
            WHERE id = ?
        ''', (
            data.get('nom'),
            data.get('description'),
            data.get('preview_path'),
            data.get('type_id'),
            data.get('category_id'),
            datetime.now(),
            media_id
        ))
        conn.commit()
        close_db_connection(conn)
        return jsonify({'message': 'Media updated successfully'})
    except sqlite3.IntegrityError as e:
        close_db_connection(conn)
        return jsonify({'error': str(e)}), 400

@app.route('/api/media/<int:media_id>', methods=['DELETE'])
def delete_media(media_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if media exists
    cursor.execute('SELECT id FROM media WHERE id = ? AND date_suppression IS NULL', (media_id,))
    if not cursor.fetchone():
        close_db_connection(conn)
        return jsonify({'error': 'Media not found'}), 404
    
    try:
        cursor.execute('''
            UPDATE media SET
                date_suppression = ?,
                est_supprime = 1
            WHERE id = ?
        ''', (datetime.now(), media_id))
        conn.commit()
        close_db_connection(conn)
        return jsonify({'message': 'Media deleted successfully'})
    except Exception as e:
        close_db_connection(conn)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)