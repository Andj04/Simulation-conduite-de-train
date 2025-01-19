import sys
import os

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.train import Train

# Initialiser un objet Train
mon_train = Train(vitesse_max=150)

# Tester les fonctionnalités
mon_train.accelerer(50)  # Augmenter la vitesse de 50 km/h
mon_train.accelerer(120)  # Augmenter la vitesse, dépasser la limite
mon_train.ralentir(30)  # Réduire la vitesse de 30 km/h
mon_train.arreter()  # Arrêter complètement le train
mon_train.afficher_etat()  # Afficher l'état actuel
