import csv
from datetime import datetime

class DataSaver:
    def __init__(self, chemin_fichier='interactions_utilisateur.csv'):
        self.chemin_fichier = chemin_fichier
        self.donnees = []  # Stocke temporairement les données

    def enregistrer_interaction(self, type_interaction, temps_reponse, statut):
        """
        Ajoute une interaction utilisateur à la liste des données.
        :param type_interaction: str, type d'interaction (ex. "Alarme sonore").
        :param temps_reponse: float, temps de réponse en secondes.
        :param statut: str, statut de l'interaction (ex. "Réponse", "Non-réponse").
        """
        interaction = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type_interaction': type_interaction,
            'temps_reponse': temps_reponse,
            'statut': statut
        }
        self.donnees.append(interaction)

    def sauvegarder_donnees(self):
        """
        Sauvegarde les données collectées dans un fichier CSV.
        """
        with open(self.chemin_fichier, mode='a', newline='') as fichier_csv:
            writer = csv.DictWriter(fichier_csv, fieldnames=['timestamp', 'type_interaction', 'temps_reponse', 'statut'])
            if fichier_csv.tell() == 0:  # Écrit l'en-tête uniquement si le fichier est vide
                writer.writeheader()
            writer.writerows(self.donnees)
        self.donnees = []  # Réinitialise les données après la sauvegarde

    def charger_donnees(self):
        """
        Charge les données depuis le fichier CSV.
        :return: list of dict, données chargées.
        """
        try:
            with open(self.chemin_fichier, mode='r') as fichier_csv:
                reader = csv.DictReader(fichier_csv)
                return list(reader)
        except FileNotFoundError:
            print("Aucun fichier trouvé. Retour d'une liste vide.")
            return []
        

if __name__ == "__main__":
    data_saver = DataSaver()

    # Ajouter des interactions simulées
    data_saver.enregistrer_interaction("Alarme sonore", 1.25, "Réponse")
    data_saver.enregistrer_interaction("Alarme visuelle", 2.50, "Non-réponse")

    # Sauvegarder les interactions dans un fichier CSV
    data_saver.sauvegarder_donnees()

    # Charger et afficher les données sauvegardées
    donnees = data_saver.charger_donnees()
    print(donnees)
