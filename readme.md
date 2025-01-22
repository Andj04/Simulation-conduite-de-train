# Train Simulator

## Description
Le **Train Simulator** est une application interactive développée en Python avec PyQt5. Cette application simule un environnement de train où vous pouvez contrôler la vitesse du train, surveiller son mouvement sur des rails, et gérer un système d'alarme en fonction de la vitesse.

L'interface utilisateur est divisée en trois zones :
- **Zone de contrôle de la vitesse** : permet de contrôler l'accélération, le freinage et l'arrêt du train.
- **Zone centrale** : affiche une vue de dessus du train en mouvement sur les rails.
- **Zone d'alarme** : indique l'état des alarmes en fonction de la vitesse.

---

## Fonctionnalités
### 1. Contrôle de la vitesse
- **Accélération** : Augmente la vitesse par incréments de 10 km/h.
- **Freinage** : Réduit la vitesse graduellement.
- **Arrêt complet** : Arrête le train instantanément après un délai de 2 secondes.

### 2. Vue de dessus réaliste
- Représentation d'un train avec des rails et un sol texturé.
- Défilement fluide des rails et des traverses pour simuler le mouvement.
- Train détaillé avec des fenêtres, des roues, et une lumière frontale.

### 3. Système d'alarme
- **Activation** : L'alarme s'active lorsque la vitesse dépasse 300 km/h.
- **Effet visuel** : Changement de couleur et clignotement pour signaler l'alarme.
- **Effet sonore** : Un bip sonore est émis toutes les 1,5 secondes lorsque l'alarme est active.

---

## Installation
### Prérequis
- **Python 3.7+**
- **PyQt5** :
  Installez PyQt5 avec pip :
  ```bash
  pip install PyQt5
  ```
- **PyQt5 Multimedia** (pour le son) :
  ```bash
  pip install PyQt5
  ```

### Cloner le projet
```bash
git clone <URL_DU_REPOSITORY>
cd train_simulator
```

### Lancer le simulateur
Exécutez le fichier principal :
```bash
python train_simulator.py
```

---

## Structure de l'application
### 1. **TrainSimulator** (classe principale)
- Initialise l'interface utilisateur avec les trois zones : contrôle de la vitesse, affichage central, et système d'alarme.
- Gère les événements liés au contrôle de la vitesse et au système d'alarme.

### 2. **TrainPositionWidget** (widget personnalisé)
- Affiche une vue de dessus du train en mouvement.
- Dessine le sol, les rails, les traverses, et le train.
- Met à jour la position des rails et du train en fonction de la vitesse.

### 3. **Timers**
- Un timer pour mettre à jour la simulation toutes les 100ms.
- Un timer pour gérer les sons d'alarme toutes les 1,5 secondes.

---

## Aperçu de l'interface
### Zones principales
1. **Contrôle de la vitesse** :
   - Trois boutons : `Accelerate`, `Brake`, et `Stop`.
   - Afficheur de vitesse stylisé.

2. **Zone centrale** :
   - Vue réaliste des rails et du train avec un défilement fluide.
   - Textures et dégradés pour simuler le sol et les traverses.

3. **Système d'alarme** :
   - Affiche l'état de l'alarme (`ON` ou `OFF`).
   - Couleur verte pour un état normal, rouge pour une alarme active.

---

## Contribution
Les contributions sont les bienvenues ! Suivez ces étapes pour participer :
1. Forkez ce repository.
2. Créez une branche pour vos modifications :
   ```bash
   git checkout -b feature/nom-de-la-feature
   ```
3. Faites vos changements et committez-les :
   ```bash
   git commit -m "Ajout de nouvelles fonctionnalités"
   ```
4. Poussez vos changements :
   ```bash
   git push origin feature/nom-de-la-feature
   ```
5. Ouvrez une pull request.

---

## Licence
Vous êtes libre de l'utiliser, de le modifier, et de le distribuer.

---

## Auteur
Développé par GAIT 