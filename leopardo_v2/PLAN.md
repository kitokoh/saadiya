### Phase 0 : Préparation et Initialisation

1.  **Créer la nouvelle structure du projet.**
    *   Je vais créer un nouveau répertoire nommé `leopardo_v2` à la racine du projet pour héberger la nouvelle version de l'application.
    *   À l'intérieur de `leopardo_v2`, je mettrai en place une architecture modulaire et claire, avec des dossiers distincts pour l'application (`app`), les tests (`tests`), les ressources (`assets`), les composants d'interface (`components`), les fonctionnalités (`features`), les services (`services`), etc.

2.  **Créer le squelette de l'application principale.**
    *   Je vais créer un nouveau fichier `main.py` dans `leopardo_v2/app/` qui servira de point d'entrée pour la nouvelle application.
    *   Ce fichier contiendra une classe principale `QMainWindow` simple avec une barre de menu et une zone de contenu, prête à accueillir les fonctionnalités refactorisées.

### Phase 1 : Refactorisation du Bouton "Accueil"

3.  **Analyser le code de l'accueil actuel.**
    *   Le bouton "Accueil" dans le `main.py` actuel lance `MarketingAIAnalyzer` du fichier `promptes/promptmarketing.py`. Je vais lire et analyser ce fichier pour comprendre sa fonctionnalité exacte.

4.  **Refactoriser et intégrer la fonctionnalité "Accueil".**
    *   Je vais réécrire la logique de `MarketingAIAnalyzer` en suivant les meilleures pratiques.
    *   Le code refactorisé sera placé dans un nouveau module, par exemple `leopardo_v2/app/features/home/home_widget.py`.
    *   J'intégrerai ce nouveau widget comme onglet par défaut qui s'ouvre au lancement de la nouvelle application.

### Phases suivantes (planification à haut niveau)

Après avoir terminé la première phase, je suivrai une approche similaire pour chaque bouton et fonctionnalité principale de l'application, en suivant cet ordre (qui pourra être ajusté) :

*   **Phase 2 :** Bouton "Marketing" et ses sous-fonctionnalités.
*   **Phase 3 :** Bouton "Sales" (Ventes).
*   **Phase 4 :** Bouton "Run".
*   **Phase 5 :** Bouton "Finance".
*   **Phase 6 :** Bouton "Settings" (Paramètres) et la gestion des instances.
*   **Phase 7 :** Les outils (Tools) comme l'édition de PDF, la gestion des liens, etc.
*   **Phase ...N :** Chaque phase se concentrera sur un bouton ou une fonctionnalité spécifique, jusqu'à ce que toute l'application de bureau soit portée sur la nouvelle architecture.

Pour chaque phase, je m'assurerai que la fonctionnalité est non seulement fonctionnelle mais aussi bien intégrée, testable et facile à maintenir.
