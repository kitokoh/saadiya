# Guide du Développeur et Intégration IA - Leopardo AI

Ce guide est destiné aux développeurs (humains ou IA) souhaitant mettre à jour, étendre ou recréer la plateforme.

## 1. Comment ajouter une nouvelle fonctionnalité (Feature)

Pour ajouter un module `ma_nouvelle_feature` :
1. Créez un dossier `leopardo_v2/app/features/ma_nouvelle_feature/`.
2. Créez les fichiers `__init__.py`, `ma_nouvelle_feature_model.py`, `ma_nouvelle_feature_widget.py`, et `ma_nouvelle_feature_controller.py`.
3. Implémentez la fonction `create_ma_nouvelle_feature_feature()` dans le `__init__.py` qui retourne le widget et son contrôleur.
4. Dans `leopardo_v2/app/core/app_setup.py` :
   - Importez la fonction de création.
   - Appelez-la dans `init_features(main_window)`.
   - Ajoutez le widget retourné au `content_stack` de `main_window`.
5. Ajoutez un bouton dans `leopardo_v2/app/ui/side_menu.py` et connectez son signal `clicked` dans `app_setup.py`.

## 2. Accès aux Services Globaux

N'instanciez pas de nouveaux services si un service global existe. Utilisez le `ServiceContainer` :
```python
from ..services.service_container import container

auth_service = container.get('auth_service')
if auth_service.has_access('pro'):
    # logique pour accès pro
```

## 3. Conventions de Codage
- **Type Hinting** : Utilisez des annotations de type partout où c'est possible.
- **Documentation** : Chaque classe et fonction doit avoir une Docstring (style Google).
- **Gestion des Erreurs** : Encapsulez les appels aux bases de données dans des blocs `try/except`.
- **Signaux PyQt5** : Préférez la communication via les signaux plutôt que le couplage direct entre les classes.

## 4. Maintenance des Bases de Données
Si vous modifiez le schéma de la base de données, mettez à jour `leopardo_v2/app/core/database.py` pour inclure les nouveaux champs dans `init_data_db()` ou créez un script de migration séparé.

## 5. Notes pour les IA
- **Contexte** : Avant de proposer des changements, lisez toujours `architecture_globale.md` et `composants.md`.
- **Génération de Code** : Assurez-vous que le code généré suit le patron MVC.
- **Intégration** : L'IA doit être capable d'analyser `app_setup.py` pour comprendre comment les composants sont liés.
