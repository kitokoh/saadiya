import sqlite3
import psycopg2
import os

# Chemin vers le fichier SQL
SQL_FILE = "database_schema.sql"

def create_sqlite_database():
    """Crée la base de données SQLite et toutes les tables."""
    conn = None
    try:
        # Chemin vers le fichier de base de données SQLite
        db_path = "database/comptabilite.db"
        
        # Vérifie si le répertoire existe, sinon le crée
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # Connexion à SQLite (crée le fichier s'il n'existe pas)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Lecture du fichier SQL
        with open(SQL_FILE, "r") as file:
            sql_script = file.read()

        # Exécution du script SQL
        cursor.executescript(sql_script)
        print("Base de données SQLite créée avec succès !")

    except sqlite3.Error as e:
        print(f"Erreur SQLite : {e}")
    except Exception as e:
        print(f"Erreur inattendue : {e}")
    finally:
        if conn:
            conn.close()

def create_postgresql_database():
    """Crée la base de données PostgreSQL et toutes les tables."""
    conn = None
    try:
        # Connexion à PostgreSQL
        conn = psycopg2.connect(
            dbname="comptabilite",
            user="votre_utilisateur",
            password="votre_mot_de_passe",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # Lecture du fichier SQL
        with open(SQL_FILE, "r") as file:
            sql_script = file.read()

        # Exécution du script SQL
        cursor.execute(sql_script)
        conn.commit()
        print("Base de données PostgreSQL créée avec succès !")

    except psycopg2.Error as e:
        print(f"Erreur PostgreSQL : {e}")
    except Exception as e:
        print(f"Erreur inattendue : {e}")
    finally:
        if conn:
            conn.close()

def main():
    print("Choisissez le type de base de données :")
    print("1. SQLite")
    print("2. PostgreSQL")
    choix = input("Entrez votre choix (1 ou 2) : ")

    if choix == "1":
        create_sqlite_database()
    elif choix == "2":
        create_postgresql_database()
    else:
        print("Choix invalide. Veuillez choisir 1 ou 2.")

if __name__ == "__main__":
    main()