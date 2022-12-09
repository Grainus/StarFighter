# Copyright (c) 2022 Grainus, WyllasSidjeno, AsadPug, Phil-DB
# Licence Libre MIT

# L’autorisation est accordée, gracieusement, à toute personne acquérant une copie
# de ce logiciel et des fichiers de documentation associés (le « logiciel »), de commercialiser
# le logiciel sans restriction, notamment les droits d’utiliser, de copier, de modifier,
# de fusionner, de publier, de distribuer, de sous-licencier et / ou de vendre des copies du logiciel,
# ainsi que d’autoriser les personnes auxquelles la logiciel est fournie à le faire,
# sous réserve des conditions suivantes :
#
# La déclaration de copyright ci-dessus et la présente autorisation doivent être incluses dans
# toutes copies ou parties substantielles du logiciel.
#
# LE LOGICIEL EST FOURNI « TEL QUEL », SANS GARANTIE D’AUCUNE SORTE, EXPLICITE OU IMPLICITE,
# NOTAMMENT SANS GARANTIE DE QUALITÉ MARCHANDE, D’ADÉQUATION À UN USAGE PARTICULIER ET D’ABSENCE
# DE CONTREFAÇON. EN AUCUN CAS, LES AUTEURS OU TITULAIRES DU DROIT D’AUTEUR NE SERONT RESPONSABLES
# DE TOUT DOMMAGE, RÉCLAMATION OU AUTRE RESPONSABILITÉ, QUE CE SOIT DANS LE CADRE D’UN CONTRAT,
# D’UN DÉLIT OU AUTRE, EN PROVENANCE DE, CONSÉCUTIF À OU EN RELATION AVEC LE LOGICIEL OU SON UTILISATION,
# OU AVEC D’AUTRES ÉLÉMENTS DU LOGICIEL.
"""Module principal du jeu Starfighter

Ce module contient la classe Root qui est la fenêtre principale du jeu.
Elle est aussi responsable de lancer le controlleur de menu et de lancer
la boucle principale du jeu."""

import tkinter as tk

from Controller import MenuController


class Root(tk.Tk):
    """Création de la fenêtre principale du jeu. Elle est responsable
    de la mainloop ainsi que d'être l'affichage principal du jeu

    :param this.title: Titre de la fenêtre
    :param this.controller: Controlleur du menu
    :param this.resizable: Redimensionnement de la fenêtre
    :param this.geometry: Taille de la fenêtre
    """
    def __init__(self):
        super().__init__()
        self.title("Starfighter")
        self.controller = MenuController(self)
        self.resizable(False, False)
        self.geometry("1200x800")


if __name__ == "__main__":
    """Lancement du jeu
    
    Lancement du jeu en créant une instance de Root et en lançant"""
    root = Root()
    root.controller.start()
    root.mainloop()
