train_simulation/
├── main.py                 # Point d'entrée de l'application
├── config/
│   └── settings.py         # Configuration générale (ex. fréquence cardiaque, durées, paramètres)
├── controllers/
│   ├── train_controller.py # Logique métier pour la simulation de train
│   └── user_feedback.py    # Gestion des évaluations utilisateur (stress, certitude)
├── models/
│   ├── train.py            # Modèle pour représenter l'état du train
│   ├── alarms.py           # Modèle pour gérer les alarmes
│   └── user.py             # Modèle pour enregistrer les données utilisateur
├── views/
│   ├── interface.py        # Gestion de l'interface utilisateur (Tkinter ou autre framework)
│   └── components.py       # Éléments spécifiques de l'interface (boutons, sliders)
├── utils/
│   ├── data_saver.py       # Sauvegarde des données enregistrées
│   ├── logger.py           # Journaux pour débogage
│   └── sound_manager.py    # Gestion des sons (bips, alarmes)
├── experiments/
│   └── protocol.py         # Gestion des conditions expérimentales (synchrone, asynchrone, apériodique)
├── tests/
│   ├── test_train.py       # Tests unitaires pour le modèle du train
│   ├── test_alarms.py      # Tests unitaires pour les alarmes
│   └── test_interface.py   # Tests pour l'interface utilisateur
└── README.md               # Documentation du projet


main.py
- Point d'entrée de l'application.
- Initialise les modules nécessaires (interface, -modèle du train, gestion des alarmes).
- Démarre la boucle principale de la simulation.

config/settings.py
- Contient les paramètres de configuration :
    - Fréquences cardiaques par condition.
    - Durées des alarmes.
    - Vitesse initiale du train.
    - Chemin du fichier pour enregistrer les données.

controllers/train_controller.py
- Logique métier pour :
    - Contrôler la vitesse du train.
    - Détecter les événements (ouverture/fermeture des portes, annonces).
    - Gérer les actions utilisateur sur le manipulateur.

controllers/user_feedback.py
- Collecte les données utilisateur sur le stress, la performance et la certitude.
- Enregistre les données dans un format exploitable (CSV ou JSON).

models/train.py
- Représente l'état du train (vitesse, position, alarme active).
- Méthodes pour modifier la vitesse, freiner, etc.

models/alarms.py
- Modélise les alarmes visuelles et sonores.
- Gère l'état des alarmes (actif/inactif).
- Chronomètre pour vérifier les réponses.

views/interface.py
- Crée l'interface utilisateur principale.
- Gère les interactions avec les utilisateurs (boutons, sliders, affichage des alarmes).
- Affiche le retour utilisateur après chaque session.

views/components.py
- Contient des fonctions réutilisables pour créer des éléments d'interface comme :
    - Un bouton stylisé.
    - Une barre de progression.
    - Une fenêtre contextuelle.

utils/data_saver.py
- Sauvegarde des données :
    - Temps de réponse des utilisateurs.
    - Non-réponses aux alarmes.
a   - Données démographiques (âge, genre, fréquence cardiaque).

experiments/protocol.py
- Implémente les trois conditions expérimentales (synchrone, asynchrone, apériodique).
- Change dynamiquement le comportement des alarmes en fonction des conditions.
