-- Table Utilisateurs
CREATE TABLE IF NOT EXISTS Utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    mot_de_passe_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin', 'comptable', 'gestionnaire')),
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table Entreprises
CREATE TABLE IF NOT EXISTS Entreprises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    adresse TEXT,
    ville TEXT,
    code_postal TEXT,
    pays TEXT,
    telephone TEXT,
    email TEXT UNIQUE NOT NULL,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table Clients
CREATE TABLE IF NOT EXISTS Clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entreprise_id INTEGER NOT NULL,
    nom TEXT NOT NULL,
    adresse TEXT,
    ville TEXT,
    code_postal TEXT,
    pays TEXT,
    telephone TEXT,
    email TEXT,
    FOREIGN KEY (entreprise_id) REFERENCES Entreprises(id) ON DELETE CASCADE
);

-- Table Fournisseurs
CREATE TABLE IF NOT EXISTS Fournisseurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entreprise_id INTEGER NOT NULL,
    nom TEXT NOT NULL,
    adresse TEXT,
    ville TEXT,
    code_postal TEXT,
    pays TEXT,
    telephone TEXT,
    email TEXT,
    FOREIGN KEY (entreprise_id) REFERENCES Entreprises(id) ON DELETE CASCADE
);

-- Table Comptes (Plan Comptable)
CREATE TABLE IF NOT EXISTS Comptes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entreprise_id INTEGER NOT NULL,
    code TEXT NOT NULL,
    libelle TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('actif', 'passif', 'produit', 'charge')),
    FOREIGN KEY (entreprise_id) REFERENCES Entreprises(id) ON DELETE CASCADE
);

-- Table EcrituresComptables
CREATE TABLE IF NOT EXISTS EcrituresComptables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entreprise_id INTEGER NOT NULL,
    compte_debit_id INTEGER NOT NULL,
    compte_credit_id INTEGER NOT NULL,
    montant REAL NOT NULL CHECK(montant > 0),
    date_ecriture DATETIME DEFAULT CURRENT_TIMESTAMP,
    libelle TEXT NOT NULL,
    piece_jointe TEXT,
    FOREIGN KEY (entreprise_id) REFERENCES Entreprises(id) ON DELETE CASCADE,
    FOREIGN KEY (compte_debit_id) REFERENCES Comptes(id),
    FOREIGN KEY (compte_credit_id) REFERENCES Comptes(id)
);

-- Table Factures
CREATE TABLE IF NOT EXISTS Factures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entreprise_id INTEGER NOT NULL,
    client_id INTEGER,
    fournisseur_id INTEGER,
    numero_facture TEXT NOT NULL,
    date_facture DATETIME DEFAULT CURRENT_TIMESTAMP,
    montant_ht REAL NOT NULL,
    montant_ttc REAL NOT NULL,
    statut TEXT NOT NULL CHECK(statut IN ('payée', 'impayée', 'en_attente')),
    FOREIGN KEY (entreprise_id) REFERENCES Entreprises(id) ON DELETE CASCADE,
    FOREIGN KEY (client_id) REFERENCES Clients(id),
    FOREIGN KEY (fournisseur_id) REFERENCES Fournisseurs(id)
);

-- Table Paiements
CREATE TABLE IF NOT EXISTS Paiements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    facture_id INTEGER NOT NULL,
    montant REAL NOT NULL,
    date_paiement DATETIME DEFAULT CURRENT_TIMESTAMP,
    mode_paiement TEXT NOT NULL CHECK(mode_paiement IN ('carte', 'virement', 'espèces')),
    FOREIGN KEY (facture_id) REFERENCES Factures(id) ON DELETE CASCADE
);

-- Table Employes
CREATE TABLE IF NOT EXISTS Employes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entreprise_id INTEGER NOT NULL,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    salaire_brut REAL NOT NULL,
    date_embauche DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entreprise_id) REFERENCES Entreprises(id) ON DELETE CASCADE
);

-- Table BulletinsPaie
CREATE TABLE IF NOT EXISTS BulletinsPaie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employe_id INTEGER NOT NULL,
    mois INTEGER NOT NULL CHECK(mois BETWEEN 1 AND 12),
    annee INTEGER NOT NULL,
    salaire_net REAL NOT NULL,
    cotisations REAL NOT NULL,
    FOREIGN KEY (employe_id) REFERENCES Employes(id) ON DELETE CASCADE
);

-- Table Taxes
CREATE TABLE IF NOT EXISTS Taxes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entreprise_id INTEGER NOT NULL,
    type_taxe TEXT NOT NULL CHECK(type_taxe IN ('TVA', 'impôt_sociétés')),
    montant REAL NOT NULL,
    date_declaration DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entreprise_id) REFERENCES Entreprises(id) ON DELETE CASCADE
);

-- Table Produits
CREATE TABLE IF NOT EXISTS Produits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entreprise_id INTEGER NOT NULL,
    nom TEXT NOT NULL,
    description TEXT,
    prix_unitaire REAL NOT NULL,
    quantite_stock INTEGER NOT NULL,
    FOREIGN KEY (entreprise_id) REFERENCES Entreprises(id) ON DELETE CASCADE
);

-- Table MouvementsStocks
CREATE TABLE IF NOT EXISTS MouvementsStocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produit_id INTEGER NOT NULL,
    type_mouvement TEXT NOT NULL CHECK(type_mouvement IN ('entree', 'sortie')),
    quantite INTEGER NOT NULL,
    date_mouvement DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (produit_id) REFERENCES Produits(id) ON DELETE CASCADE
);

-- Table JournalAudit
CREATE TABLE IF NOT EXISTS JournalAudit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    utilisateur_id INTEGER NOT NULL,
    action TEXT NOT NULL,
    date_action DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateurs(id) ON DELETE CASCADE
);

-- Table Parametres
CREATE TABLE IF NOT EXISTS Parametres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entreprise_id INTEGER NOT NULL,
    cle TEXT NOT NULL,
    valeur TEXT NOT NULL,
    FOREIGN KEY (entreprise_id) REFERENCES Entreprises(id) ON DELETE CASCADE
);

-- Table Devises
CREATE TABLE IF NOT EXISTS Devises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    libelle TEXT NOT NULL,
    taux_conversion REAL NOT NULL
);

-- Table TransactionsMultiDevises
CREATE TABLE IF NOT EXISTS TransactionsMultiDevises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entreprise_id INTEGER NOT NULL,
    montant REAL NOT NULL,
    devise_id INTEGER NOT NULL,
    date_transaction DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entreprise_id) REFERENCES Entreprises(id) ON DELETE CASCADE,
    FOREIGN KEY (devise_id) REFERENCES Devises(id)
);

-- Table Relances
CREATE TABLE IF NOT EXISTS Relances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    facture_id INTEGER NOT NULL,
    date_relance DATETIME DEFAULT CURRENT_TIMESTAMP,
    statut TEXT NOT NULL CHECK(statut IN ('envoyée', 'en_attente', 'payée')),
    FOREIGN KEY (client_id) REFERENCES Clients(id) ON DELETE CASCADE,
    FOREIGN KEY (facture_id) REFERENCES Factures(id)
);

-- Table CreancesDouteuses
CREATE TABLE IF NOT EXISTS CreancesDouteuses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    montant REAL NOT NULL,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES Clients(id) ON DELETE CASCADE
);

-- Table PrevisionsFluxTresorerie
CREATE TABLE IF NOT EXISTS PrevisionsFluxTresorerie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entreprise_id INTEGER NOT NULL,
    date_prevision DATE NOT NULL,
    montant_prevu REAL NOT NULL,
    confiance REAL NOT NULL CHECK(confiance BETWEEN 0 AND 1),
    FOREIGN KEY (entreprise_id) REFERENCES Entreprises(id) ON DELETE CASCADE
);

-- Table TransactionsBlockchain
CREATE TABLE IF NOT EXISTS TransactionsBlockchain (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hash_transaction TEXT NOT NULL UNIQUE,
    type_transaction TEXT NOT NULL CHECK(type_transaction IN ('facture', 'paiement', 'ajustement')),
    donnees_transaction TEXT NOT NULL,
    date_transaction DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entreprise_id) REFERENCES Entreprises(id) ON DELETE CASCADE
);

-- Table Projets
CREATE TABLE IF NOT EXISTS Projets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entreprise_id INTEGER NOT NULL,
    nom TEXT NOT NULL,
    description TEXT,
    date_debut DATE NOT NULL,
    date_fin DATE,
    budget REAL NOT NULL,
    FOREIGN KEY (entreprise_id) REFERENCES Entreprises(id) ON DELETE CASCADE
);

-- Table Actifs
CREATE TABLE IF NOT EXISTS Actifs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entreprise_id INTEGER NOT NULL,
    nom TEXT NOT NULL,
    description TEXT,
    date_acquisition DATE NOT NULL,
    valeur_initiale REAL NOT NULL,
    duree_amortissement INTEGER NOT NULL,
    FOREIGN KEY (entreprise_id) REFERENCES Entreprises(id) ON DELETE CASCADE
);

-- Table RisquesFinanciers
CREATE TABLE IF NOT EXISTS RisquesFinanciers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entreprise_id INTEGER NOT NULL,
    type_risque TEXT NOT NULL CHECK(type_risque IN ('credit', 'marche', 'liquidite')),
    description TEXT NOT NULL,
    probabilite REAL NOT NULL CHECK(probabilite BETWEEN 0 AND 1),
    impact REAL NOT NULL CHECK(impact BETWEEN 0 AND 1),
    FOREIGN KEY (entreprise_id) REFERENCES Entreprises(id) ON DELETE CASCADE
);

-- Table ContratsIntelligents
CREATE TABLE IF NOT EXISTS ContratsIntelligents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entreprise_id INTEGER NOT NULL,
    hash_contrat TEXT NOT NULL UNIQUE,
    type_contrat TEXT NOT NULL CHECK(type_contrat IN ('paiement', 'validation_facture')),
    donnees_contrat TEXT NOT NULL,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entreprise_id) REFERENCES Entreprises(id) ON DELETE CASCADE
);

-- Table KPI
CREATE TABLE IF NOT EXISTS KPI (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entreprise_id INTEGER NOT NULL,
    nom TEXT NOT NULL,
    valeur REAL NOT NULL,
    date_mise_a_jour DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entreprise_id) REFERENCES Entreprises(id) ON DELETE CASCADE
);

-- Table Notifications
CREATE TABLE IF NOT EXISTS Notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    utilisateur_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    date_notification DATETIME DEFAULT CURRENT_TIMESTAMP,
    lue BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateurs(id) ON DELETE CASCADE
);

-- Table IntegrationsAPI
CREATE TABLE IF NOT EXISTS IntegrationsAPI (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entreprise_id INTEGER NOT NULL,
    nom_service TEXT NOT NULL,
    endpoint TEXT NOT NULL,
    cle_api TEXT NOT NULL,
    FOREIGN KEY (entreprise_id) REFERENCES Entreprises(id) ON DELETE CASCADE
);

-- Table Roles
CREATE TABLE IF NOT EXISTS Roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL UNIQUE,
    description TEXT
);

-- Table Permissions
CREATE TABLE IF NOT EXISTS Permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL UNIQUE,
    description TEXT
);

-- Table RolePermissions
CREATE TABLE IF NOT EXISTS RolePermissions (
    role_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES Roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES Permissions(id) ON DELETE CASCADE
);

-- Table UtilisateurRoles
CREATE TABLE IF NOT EXISTS UtilisateurRoles (
    utilisateur_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    PRIMARY KEY (utilisateur_id, role_id),
    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateurs(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES Roles(id) ON DELETE CASCADE
);

-- Table VersionsDocuments
CREATE TABLE IF NOT EXISTS VersionsDocuments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    type_document TEXT NOT NULL CHECK(type_document IN ('facture', 'contrat', 'ecriture')),
    version INTEGER NOT NULL,
    donnees TEXT NOT NULL,
    date_version DATETIME DEFAULT CURRENT_TIMESTAMP,
    utilisateur_id INTEGER NOT NULL,
    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateurs(id) ON DELETE CASCADE
);

-- Table Taches
CREATE TABLE IF NOT EXISTS Taches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    description TEXT,
    statut TEXT NOT NULL CHECK(statut IN ('à faire', 'en cours', 'terminée')),
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_echeance DATE,
    utilisateur_assignee_id INTEGER NOT NULL,
    FOREIGN KEY (utilisateur_assignee_id) REFERENCES Utilisateurs(id) ON DELETE CASCADE
);

-- Table Workflows
CREATE TABLE IF NOT EXISTS Workflows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    description TEXT,
    etape_actuelle INTEGER NOT NULL,
    etape_totale INTEGER NOT NULL,
    statut TEXT NOT NULL CHECK(statut IN ('en cours', 'terminé', 'annulé')),
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (etape_actuelle) REFERENCES Taches(id)
);

-- Table Communications
CREATE TABLE IF NOT EXISTS Communications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_communication TEXT NOT NULL CHECK(type_communication IN ('email', 'appel', 'réunion')),
    sujet TEXT NOT NULL,
    message TEXT NOT NULL,
    date_communication DATETIME DEFAULT CURRENT_TIMESTAMP,
    utilisateur_id INTEGER NOT NULL,
    contact_id INTEGER NOT NULL,
    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateurs(id) ON DELETE CASCADE,
    FOREIGN KEY (contact_id) REFERENCES Clients(id) ON DELETE CASCADE
);

-- Table PiecesJointesCommunications
CREATE TABLE IF NOT EXISTS PiecesJointesCommunications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    communication_id INTEGER NOT NULL,
    nom_fichier TEXT NOT NULL,
    chemin_fichier TEXT NOT NULL,
    FOREIGN KEY (communication_id) REFERENCES Communications(id) ON DELETE CASCADE
);

-- Table Abonnements
CREATE TABLE IF NOT EXISTS Abonnements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entreprise_id INTEGER NOT NULL,
    plan TEXT NOT NULL CHECK(plan IN ('basique', 'standard', 'premium')),
    date_debut DATE NOT NULL,
    date_fin DATE,
    statut TEXT NOT NULL CHECK(statut IN ('actif', 'inactif', 'suspendu')),
    FOREIGN KEY (entreprise_id) REFERENCES Entreprises(id) ON DELETE CASCADE
);

-- Table PaiementsRecurrents
CREATE TABLE IF NOT EXISTS PaiementsRecurrents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    abonnement_id INTEGER NOT NULL,
    montant REAL NOT NULL,
    date_paiement DATE NOT NULL,
    statut TEXT NOT NULL CHECK(statut IN ('payé', 'impayé', 'en attente')),
    FOREIGN KEY (abonnement_id) REFERENCES Abonnements(id) ON DELETE CASCADE
);

-- Table Langues
CREATE TABLE IF NOT EXISTS Langues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    libelle TEXT NOT NULL
);

-- Table Traductions
CREATE TABLE IF NOT EXISTS Traductions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cle TEXT NOT NULL,
    langue_id INTEGER NOT NULL,
    valeur TEXT NOT NULL,
    FOREIGN KEY (langue_id) REFERENCES Langues(id) ON DELETE CASCADE
);

-- Table Archives
CREATE TABLE IF NOT EXISTS Archives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_source TEXT NOT NULL,
    id_source INTEGER NOT NULL,
    donnees TEXT NOT NULL,
    date_archivage DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Index pour améliorer les performances
CREATE INDEX IF NOT EXISTS idx_utilisateurs_email ON Utilisateurs(email);
CREATE INDEX IF NOT EXISTS idx_factures_statut ON Factures(statut);
CREATE INDEX IF NOT EXISTS idx_mouvementsstocks_produit_id ON MouvementsStocks(produit_id);
CREATE INDEX IF NOT EXISTS idx_ecriturescomptables_date_ecriture ON EcrituresComptables(date_ecriture);
CREATE INDEX IF NOT EXISTS idx_transactionsmultidevises_devise_id ON TransactionsMultiDevises(devise_id);

-- Trigger pour Mettre à Jour le Stock
CREATE TRIGGER IF NOT EXISTS update_stock
AFTER INSERT ON MouvementsStocks
FOR EACH ROW
BEGIN
    UPDATE Produits
    SET quantite_stock = quantite_stock + 
        CASE 
            WHEN NEW.type_mouvement = 'entree' THEN NEW.quantite
            WHEN NEW.type_mouvement = 'sortie' THEN -NEW.quantite
        END
    WHERE id = NEW.produit_id;
END;

-- Trigger pour Calculer le Montant TTC d'une Facture
CREATE TRIGGER IF NOT EXISTS calculate_ttc
AFTER INSERT ON Factures
FOR EACH ROW
BEGIN
    UPDATE Factures
    SET montant_ttc = NEW.montant_ht * 1.20 -- Exemple de TVA à 20%
    WHERE id = NEW.id;
END;

-- Trigger pour Journalisation des Actions Utilisateurs
CREATE TRIGGER IF NOT EXISTS log_user_action
AFTER INSERT ON Utilisateurs
FOR EACH ROW
BEGIN
    INSERT INTO JournalAudit (utilisateur_id, action)
    VALUES (NEW.id, 'Nouvel utilisateur créé');
END;