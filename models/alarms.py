# alarms.py

import time
import threading

class Alarm:
    def __init__(self, type_alarme: str, duree: int):
        """
        Initialise une alarme avec un type et une durée.
        :param type_alarme: Type de l'alarme (visuelle, sonore, etc.).
        :param duree: Durée de l'alarme en secondes.
        """
        self.type_alarme = type_alarme
        self.duree = duree
        self.statut = "Arrêtée"  # Peut être 'Active' ou 'Arrêtée'

    def declencher_alarme(self):
        """
        Déclenche l'alarme et la maintient active pour la durée spécifiée.
        """
        if self.statut == "Active":
            print(f"L'alarme {self.type_alarme} est déjà active.")
            return

        self.statut = "Active"
        print(f"Alarme {self.type_alarme} déclenchée.")
        threading.Thread(target=self._maintenir_alarme).start()

    def _maintenir_alarme(self):
        """
        Maintient l'alarme active pendant la durée spécifiée.
        """
        time.sleep(self.duree)
        self.arreter_alarme()

    def arreter_alarme(self):
        """
        Arrête l'alarme si elle est active.
        """
        if self.statut == "Arrêtée":
            print(f"L'alarme {self.type_alarme} est déjà arrêtée.")
            return

        self.statut = "Arrêtée"
        print(f"Alarme {self.type_alarme} arrêtée.")

# Exemple d'utilisation
if __name__ == "__main__":
    # Synchrone : Deux alarmes démarrent en même temps
    alarme_sonore = Alarm("Sonore", 5)
    alarme_visuelle = Alarm("Visuelle", 3)

    alarme_sonore.declencher_alarme()
    alarme_visuelle.declencher_alarme()

    time.sleep(6)

    # Asynchrone : Activation et arrêt indépendants
    alarme_sonore.declencher_alarme()
    time.sleep(2)
    alarme_visuelle.declencher_alarme()

    # Apériodique : Activation sans périodicité
    time.sleep(5)
    alarme_sonore.declencher_alarme()
