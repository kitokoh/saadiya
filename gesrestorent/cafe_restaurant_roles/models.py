from database import get_db_connection

# Modèle pour les utilisateurs
class Utilisateur:
    @staticmethod
    def get_by_email(email):
        conn = get_db_connection()
        utilisateur = conn.execute('SELECT * FROM utilisateurs WHERE email = ?', (email,)).fetchone()
        conn.close()
        return utilisateur

    @staticmethod
    def verifier_permission(email, permission):
        utilisateur = Utilisateur.get_by_email(email)
        if utilisateur is None:
            return False
        conn = get_db_connection()
        permission_valide = conn.execute('''
        SELECT COUNT(*) FROM permissions
        WHERE role = ? AND permission = ?
        ''', (utilisateur['role'], permission)).fetchone()[0]
        conn.close()
        return permission_valide > 0

# Modèle pour le journal d'activité
class JournalActivite:
    @staticmethod
    def enregistrer_action(utilisateur_id, action):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO journal_activite (utilisateur_id, action)
        VALUES (?, ?)
        ''', (utilisateur_id, action))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        activites = conn.execute('''
        SELECT utilisateurs.nom, journal_activite.action, journal_activite.date
        FROM journal_activite
        JOIN utilisateurs ON journal_activite.utilisateur_id = utilisateurs.id
        ORDER BY journal_activite.date DESC
        ''').fetchall()
        conn.close()
        return activites