# Diagrammes Conceptuels - Leopardo AI

Ce document utilise la syntaxe Mermaid pour représenter graphiquement l'architecture du système.

## 1. Diagramme de Classe Simplifié (Architecture MVC)

```mermaid
classDiagram
    class MainWindow {
        +ServiceContainer container
        +QStackedWidget content_stack
        +init_features()
    }
    class ServiceContainer {
        -dict services
        +register(name, service)
        +get(name)
    }
    class AuthService {
        +bool is_logged_in
        +login(u, p)
        +has_access(level)
    }
    class FeatureModule {
        <<Interface>>
        +create_feature()
    }
    class Model {
        +getData()
        +saveData()
    }
    class View {
        +updateUI()
    }
    class Controller {
        +handleAction()
    }

    MainWindow *-- ServiceContainer
    ServiceContainer o-- AuthService
    MainWindow *-- FeatureModule
    FeatureModule *-- Model
    FeatureModule *-- View
    FeatureModule *-- Controller
```

## 2. Diagramme de Séquence : Authentification et Chargement

```mermaid
sequenceDiagram
    participant App as Main Application
    participant Auth as AuthService
    participant UI as LoginDialog
    participant MW as MainWindow

    App->>Auth: load_session()
    alt Session Valide
        Auth-->>App: is_logged_in = True
    else Session Invalide
        App->>UI: show()
        UI->>Auth: login(user, pass)
        Auth-->>UI: Success / Fail
        UI-->>App: Accepted
    end
    App->>MW: show()
    MW->>MW: init_features()
```

## 3. Diagramme de Flux : Accès aux Fonctionnalités

```mermaid
graph TD
    A[Utilisateur clique sur un bouton du SideMenu] --> B{Utilisateur Connecté?}
    B -- Non --> C[Afficher LoginDialog]
    B -- Oui --> D{Niveau d'Accès Suffisant?}
    D -- Non --> E[Afficher Message: Upgrade requis]
    D -- Oui --> F[Afficher le Widget de la fonctionnalité]
```
