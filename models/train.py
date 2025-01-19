# train.py
class Train:
    def __init__(self, vitesse_max=120, vitesse_min=0):
        """
        Initialise un train avec une vitesse initiale et des limites.
        """
        self.vitesse = 0  # Vitesse actuelle
        self.vitesse_max = vitesse_max  # Vitesse maximale autorisée
        self.vitesse_min = vitesse_min  # Vitesse minimale (généralement 0)
        self.position_manipulateur = "neutre"  # Peut être 'accélérer', 'freiner', ou 'neutre'
        self.alarme_active = False  # Si une alarme est activée ou non

    def accelerer(self, increment):
        """
        Augmente la vitesse du train en fonction de l'incrément spécifié.
        Si la vitesse dépasse la limite maximale, une alarme est déclenchée.
        """
        if self.vitesse + increment > self.vitesse_max:
            self.vitesse = self.vitesse_max
            self.declencher_alarme("Vitesse maximale atteinte !")
        else:
            self.vitesse += increment
            self.position_manipulateur = "accélérer"
        print(f"Vitesse actuelle : {self.vitesse} km/h")

    def ralentir(self, decrement):
        """
        Réduit la vitesse du train en fonction du décrément spécifié.
        La vitesse ne peut pas être inférieure à la limite minimale.
        """
        if self.vitesse - decrement < self.vitesse_min:
            self.vitesse = self.vitesse_min
        else:
            self.vitesse -= decrement
            self.position_manipulateur = "freiner"
        print(f"Vitesse actuelle : {self.vitesse} km/h")

    def arreter(self):
        """
        Arrête complètement le train en ramenant la vitesse à zéro.
        """
        self.vitesse = 0
        self.position_manipulateur = "neutre"
        print("Le train est arrêté.")

    def declencher_alarme(self, message):
        """
        Active une alarme et affiche un message d'alerte.
        """
        self.alarme_active = True
        print(f"ALERTE : {message}")

    def arreter_alarme(self):
        """
        Désactive l'alarme.
        """
        self.alarme_active = False
        print("Alarme désactivée.")

    def afficher_etat(self):
        """
        Affiche l'état actuel du train.
        """
        etat = f"""
        Vitesse actuelle : {self.vitesse} km/h
        Position du manipulateur : {self.position_manipulateur}
        Alarme active : {'Oui' if self.alarme_active else 'Non'}
        """
        print(etat)
