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

"""Module de la vue
Ce module contient les classes et fonctions nécessaires à la création de la vue

Classe:
    - View : Classe abstraite de la vue
    - MenuView : Classe de la vue du menu
    - GameView : Classe de la vue du jeu
    - HighscoreView : Classe de la vue des highscores
    - optionsView : Classe de la vue des options
    - ArsenalView : Classe de la vue de l'arsenal
"""

from Container import BetterButton, BetterLabel, BetterFrame, BetterCanvas
from abc import ABC
from typing import TYPE_CHECKING


class View(ABC):
    """Classe abstraite de la vue

    :argument main_frame: Frame principale de la vue

    :param this.main_frame: Frame principale de la vue
    """
    def __init__(self, main_frame: BetterFrame):
        self.main_frame = main_frame

    def draw(self):
        """Méthode abstraite de lancement de la vue"""
        # Recursively place all the widgets in the frame
        self.place_children(self.main_frame)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

    def place_children(self, container):
        """Méthode abstraite de placement des widgets de la vue"""
        for widget in container.winfo_children():
            if isinstance(widget, (BetterButton, BetterLabel, BetterFrame, BetterCanvas)):
                if widget.winfo_children():
                    self.place_children(widget)
                widget.place(relx=widget.x, rely=widget.y, anchor="center")

    def destroy(self):
        """Méthode de destruction de la vue"""
        self.main_frame.forget()

    def forget(self):
        """Méthode d'oublie de la vue"""
        for content in self.main_frame.winfo_children():
            content.pack_forget()
        self.main_frame.pack_forget()


class MenuView(View):
    """Classe de la vue du menu
    :argument: main_frame: Frame principale de la vue
    :param: this.title: Label du titre du jeu
    """
    def __init__(self, main_frame: BetterFrame):
        super().__init__(main_frame)
        print(self.main_frame)

        self.title = BetterLabel(self.main_frame, 0.5, 0.05, text="StarFighter",
                                 font=("Arial", 50))

        self.buttonContainer = BetterFrame(self.main_frame, 0.5, 0.9)

        self.buttonContainer.config(width=800, height=150)
        self.buttonContainer.config(highlightbackground="black",
                                    highlightthickness=1)

        self.start_game_button = BetterButton(self.buttonContainer, 0.5, 0.5,
                                                text="Jouer", font=("Arial", 20))
        self.start_game_button.config(width=10, height=2)

    def draw(self):
        """Méthode de lancement de la vue"""
        super(MenuView, self).draw()


class GameView(View):
    """Classe de la vue du jeu

    :argument main_frame: Frame principale de la vue

    :param this.main_frame: Frame principale de la vue
    """
    def __init__(self, main_frame: BetterFrame):
        super().__init__(main_frame)
        self.canvas = BetterCanvas(self.main_frame)
        self.canvas.config(bg="black")

    def draw(self):
        """Méthode de lancement de la vue"""
        super(GameView, self).draw()


class HighscoreView(View):
    """Classe de la vue des highscores

    :argument main_frame: Frame principale de la vue

    :param this.main_frame: Frame principale de la vue
    """
    def __init__(self, main_frame: BetterFrame):
        super().__init__(main_frame)


class OptionsView(View):
    """Classe de la vue des options

    :argument main_frame: Frame principale de la vue

    :param this.main_frame: Frame principale de la vue
    """
    def __init__(self, main_frame: BetterFrame):
        super().__init__(main_frame)


class ArsenalView(View):
    """Classe de la vue de l'arsenal
    :argument main_frame: Frame principale de la vue

    :param this.main_frame: Frame principale de la vue
    """
    def __init__(self, main_frame: BetterFrame):
        super().__init__(main_frame)
