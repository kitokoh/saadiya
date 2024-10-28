-- Table users
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    status TEXT DEFAULT 'active',
    FOREIGN KEY (role_id) REFERENCES user_roles(id)
);

-- Table user_roles
CREATE TABLE IF NOT EXISTS user_roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT NOT NULL,
    description TEXT
);

-- Table instances
CREATE TABLE IF NOT EXISTS instances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('active', 'inactive', 'deleted')),
    type TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    quota INTEGER DEFAULT 100,
    path TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Table licences
CREATE TABLE IF NOT EXISTS licences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT NOT NULL,
    description TEXT,
    duration INTEGER NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('valid', 'expired', 'pending')),
    instance_id INTEGER NOT NULL,
    request_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    license_type TEXT NOT NULL,
    type TEXT,
    FOREIGN KEY (instance_id) REFERENCES instances(id)
);

-- Table media
CREATE TABLE IF NOT EXISTS media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path TEXT NOT NULL,
    tag TEXT NOT NULL,
    label TEXT NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    instance_id INTEGER NOT NULL,
    name TEXT,
    FOREIGN KEY (instance_id) REFERENCES instances(id)
);

-- Table groups
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT NOT NULL,
    description TEXT,
    link TEXT NOT NULL UNIQUE,
    category TEXT,
    tag TEXT NOT NULL,
    instance_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    name TEXT,
    FOREIGN KEY (instance_id) REFERENCES instances(id)
);

-- Table facebook_users
CREATE TABLE IF NOT EXISTS facebook_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    instance_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    facebook_name TEXT UNIQUE,
    FOREIGN KEY (instance_id) REFERENCES instances(id)
);

-- Table alerts
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('info', 'warning', 'error')),
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    alert_type TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Table audit_log
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    table_name TEXT NOT NULL,
    record_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    performed_by TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Table quotas
CREATE TABLE IF NOT EXISTS quotas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    quota_limit INTEGER NOT NULL,
    current_usage INTEGER DEFAULT 0,
    instance_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    media_quota INTEGER,
    FOREIGN KEY (instance_id) REFERENCES instances(id)
);

-- Table backup_logs
CREATE TABLE IF NOT EXISTS backup_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    instance_id INTEGER NOT NULL,
    backup_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL CHECK(status IN ('success', 'failure')),
    backup_file TEXT,
    FOREIGN KEY (instance_id) REFERENCES instances(id)
);

-- Table contacts
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    email TEXT UNIQUE,
    category TEXT,
    tag TEXT,
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Table instance_user association
CREATE TABLE IF NOT EXISTS instance_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    instance_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (instance_id) REFERENCES instances(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Table group_user association
CREATE TABLE IF NOT EXISTS group_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Sélectionner tous les utilisateurs avec leurs rôles
SELECT users.id, users.name, users.email, user_roles.role_name
FROM users
INNER JOIN user_roles ON users.role_id = user_roles.id;

-- Sélectionner toutes les instances avec leurs utilisateurs associés
SELECT instances.id, instances.name, instances.status, users.name AS user_name
FROM instances
INNER JOIN users ON instances.user_id = users.id;

-- Sélectionner toutes les licences avec les informations des instances associées
SELECT licences.id, licences.label, licences.status, instances.name AS instance_name
FROM licences
INNER JOIN instances ON licences.instance_id = instances.id;

-- Sélectionner tous les médias avec les instances associées
SELECT media.id, media.file_path, media.label, instances.name AS instance_name
FROM media
INNER JOIN instances ON media.instance_id = instances.id;

-- Sélectionner tous les groupes avec les instances associées
SELECT groups.id, groups.label, groups.link, instances.name AS instance_name
FROM groups
INNER JOIN instances ON groups.instance_id = instances.id;

-- Sélectionner tous les utilisateurs Facebook avec les instances associées
SELECT facebook_users.id, facebook_users.name, facebook_users.facebook_name, instances.name AS instance_name
FROM facebook_users
INNER JOIN instances ON facebook_users.instance_id = instances.id;

-- Sélectionner toutes les alertes avec les utilisateurs associés
SELECT alerts.id, alerts.message, alerts.type, users.name AS user_name
FROM alerts
INNER JOIN users ON alerts.user_id = users.id;

-- Sélectionner les logs d'audit avec les utilisateurs ayant effectué les actions
SELECT audit_log.id, audit_log.action, audit_log.table_name, audit_log.record_id, users.name AS user_name
FROM audit_log
INNER JOIN users ON audit_log.user_id = users.id;

-- Sélectionner toutes les quotas avec les instances associées
SELECT quotas.id, quotas.type, quotas.quota_limit, quotas.current_usage, instances.name AS instance_name
FROM quotas
INNER JOIN instances ON quotas.instance_id = instances.id;

-- Sélectionner tous les logs de sauvegarde avec les instances associées
SELECT backup_logs.id, backup_logs.backup_date, backup_logs.status, instances.name AS instance_name
FROM backup_logs
INNER JOIN instances ON backup_logs.instance_id = instances.id;

-- Sélectionner tous les contacts avec les utilisateurs associés
SELECT contacts.id, contacts.first_name, contacts.last_name, contacts.phone_number, users.name AS user_name
FROM contacts
INNER JOIN users ON contacts.user_id = users.id;

-- Sélectionner les instances avec leurs utilisateurs (jointure sur la table d'association instance_user)
SELECT instances.name AS instance_name, users.name AS user_name
FROM instance_user
INNER JOIN instances ON instance_user.instance_id = instances.id
INNER JOIN users ON instance_user.user_id = users.id;

-- Sélectionner les groupes avec leurs utilisateurs (jointure sur la table d'association group_user)
SELECT groups.label AS group_label, users.name AS user_name
FROM group_user
INNER JOIN groups ON group_user.group_id = groups.id
INNER JOIN users ON group_user.user_id = users.id;

-- Ajouter un nouvel utilisateur
INSERT INTO users (name, email, password, role_id)
VALUES ('John Doe', 'john.doe@example.com', 'password123', 1);

-- Mettre à jour le quota d'une instance
UPDATE quotas
SET quota_limit = 500
WHERE instance_id = 1;

-- Supprimer un utilisateur
DELETE FROM users WHERE id = 5;

-- Ajouter un index pour optimiser la recherche d'utilisateurs par e-mail
CREATE INDEX idx_users_email ON users(email);

-- Créer une vue pour afficher les utilisateurs actifs
CREATE VIEW active_users AS
SELECT id, name, email
FROM users
WHERE status = 'active';

-- Créer une procédure stockée pour changer le statut d'un utilisateur
CREATE PROCEDURE deactivate_user(IN user_id INT)
BEGIN
    UPDATE users
    SET status = 'inactive'
    WHERE id = user_id;
END;

-- Créer un trigger pour mettre à jour la date de mise à jour d'un utilisateur à chaque modification
CREATE TRIGGER update_user_timestamp
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id = OLD.id;
END;

-- Créer un backup automatique après chaque insertion dans les logs de sauvegarde
CREATE TRIGGER auto_backup_log
AFTER INSERT ON backup_logs
FOR EACH ROW
BEGIN
    -- Simuler une procédure de sauvegarde (par exemple, copier un fichier)
    INSERT INTO backup_logs (instance_id, status, backup_file) VALUES (NEW.instance_id, 'success', 'backup_file_path');
END;
