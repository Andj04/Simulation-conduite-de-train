import time
import random
from models.alarms import Alarm  # Assurez-vous que le chemin est correct


class Protocol:
    """Classe pour gérer les différents protocoles expérimentaux."""

    def __init__(self, freq_cardiaque: int = 60):
        """
        Initialise le protocole avec une fréquence cardiaque.
        :param freq_cardiaque: Fréquence cardiaque en BPM (par défaut 60 BPM).
        """
        self.freq_cardiaque = freq_cardiaque

    def _declencher_alarme(self, type_alarme: str, duree: int = 5):
        """
        Déclenche une alarme de type spécifié pour une durée donnée.
        :param type_alarme: Le type de l'alarme (e.g., visuelle, sonore).
        :param duree: La durée pendant laquelle l'alarme reste active.
        """
        alarme = Alarm(type_alarme, duree)
        alarme.declencher_alarme()

        start_time = time.time()  # Temps de début de l'alarme

        # Simulation d'une réaction utilisateur
        user_response = input(f"L'alarme {type_alarme} est active. Appuyez sur [Entrée] pour désactiver.")

        if user_response.strip():
            reaction_time = time.time() - start_time
            print(f"Réponse utilisateur détectée pour l'alarme {type_alarme}. Temps de réaction : {reaction_time:.2f} secondes.")
        else:
            print(f"Aucune réponse pour l'alarme {type_alarme}.")

    def condition_synchrone(self):
        """
        Déclenche des alarmes à intervalles fixes basés sur la fréquence cardiaque.
        """
        interval = 60 / self.freq_cardiaque  # Intervalle entre deux alarmes
        print("Condition synchrone : déclenchement d'alarmes à intervalles fixes.")

        for _ in range(5):  # Exemple avec 5 cycles d'alarmes
            self._declencher_alarme("visuelle et sonore", 5)
            time.sleep(interval)

    def condition_asynchrone(self):
        """
        Déclenche des alarmes à des intervalles aléatoires.
        """
        print("Condition asynchrone : déclenchement d'alarmes à des intervalles aléatoires.")

        for _ in range(5):
            delay = random.uniform(1, 10)  # Intervalle aléatoire entre 1 et 10 secondes
            self._declencher_alarme("visuelle et sonore", 5)
            time.sleep(delay)

    def condition_aperiodique(self):
        """
        Déclenche des alarmes selon une séquence prédéfinie d'intervalles irréguliers.
        """
        print("Condition apériodique : déclenchement d'alarmes selon des intervalles prédéfinis.")
        intervals = [3, 7, 2, 8, 4]  # Exemple d'intervalles spécifiques

        for delay in intervals:
            self._declencher_alarme("visuelle et sonore", 5)
            time.sleep(delay)

    def lancer_protocole(self, condition: str):
        """
        Lance une condition expérimentale parmi : synchrone, asynchrone ou apériodique.
        :param condition: Type de protocole à exécuter.
        """
        if condition == "synchrone":
            self.condition_synchrone()
        elif condition == "asynchrone":
            self.condition_asynchrone()
        elif condition == "apériodique":
            self.condition_aperiodique()
        else:
            print(f"Condition inconnue : {condition}. Options disponibles : synchrone, asynchrone, apériodique.")
