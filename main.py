


#Test unitaire pour protocole expérimental
from experiments.protocol import Protocol

if __name__ == "__main__":
    protocole = Protocol(freq_cardiaque=70)  # Exemple avec une fréquence cardiaque de 70 BPM
    condition = input("Choisissez une condition expérimentale (synchrone, asynchrone, apériodique) : ").strip().lower()
    protocole.lancer_protocole(condition)
