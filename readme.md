README.md
markdown
Copy
Edit
# Train Simulator

Train Simulator est une application interactive développée en Python avec PyQt5, simulant un train avec gestion de vitesse, des arrêts aux stations et des temps de réaction enregistrés pour chaque action.

## Fonctionnalités

- **Simulation de vitesse** : Contrôlez la vitesse du train à l'aide des boutons d'accélération, de freinage et d'arrêt.
- **Stations** : Le train effectue des arrêts automatiques à des stations situées à intervalles réguliers.
- **Alarmes** :
  - Alarme de ralentissement lorsque la distance à la station est critique.
  - Alarme de porte si elles restent ouvertes.
  - Déclenchement d'arrêt d'urgence via un système "Deadman".
- **Temps de réaction** :
  - Les temps de réaction des actions utilisateur (accélération, freinage, ouverture/fermeture des portes) sont enregistrés.
  - Exportation des temps de réaction dans un fichier CSV.
- **Interface utilisateur interactive** : Zones dédiées pour les contrôles de vitesse, affichage des alarmes et position du train.

## Installation

### Prérequis

- Python 3.8 ou plus
- `pip` installé

### Étapes

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/votre-repo/train-simulator.git
   cd train-simulator
Installez les dépendances :

bash
Copy
Edit
pip install -r requirements.txt
Lancez l'application :

bash
Copy
Edit
python train_simulator.py
Utilisation
Contrôle du train :

Cliquez sur Accelerate pour augmenter la vitesse.
Cliquez sur Brake pour réduire la vitesse.
Cliquez sur Stop pour arrêter le train progressivement.
Gestion des portes :

Utilisez les boutons Open Doors et Close Doors.
Exportation des temps de réaction :

Cliquez sur Save Reaction Times pour sauvegarder un fichier CSV contenant les temps de réaction.
Structure du projet
plaintext
Copy
Edit
train_simulator/
├── train_simulator.py     # Code principal de l'application
├── requirements.txt       # Dépendances nécessaires
├── README.md              # Documentation
└── alarm.wav              # Fichier sonore pour les alarmes (optionnel)
Dépendances
PyQt5 : Framework pour l'interface graphique.
PyQt5.QtMultimedia : Gestion des sons d'alarme.
