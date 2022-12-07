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
"""Fichier principal des controlleurs du jeu

Contient :
    - Controlleur principal
    - Controlleur du jeu
    - Controlleur du menu des options
    - Controlleur du menu des highscores
    - Controlleur du menu de l'arsenal
"""

# Importation des modules de type hinting
from __future__ import annotations

# Importation des modules standards
import tkinter as tk
from abc import ABC  # Classe abstraite

from View import MenuView, GameView, HighscoreView, OptionsView, ArsenalView


class Controller(ABC):
    """Classe abstraite des controlleurs
    :argument root: Fenêtre principale du jeu

    :param self.root: Fenêtre principale du jeu
    :param self.main_frame: Frame principale graphique du jeu.
    :param self.view: Vue associée au controlleur
    """

    def __init__(self, root: tk):
        self.root = root
        """En quelque sorte, il s'agit de la fenêtre principale du jeu
        qui est aussi responsable de sa boucle principale."""

        self.main_frame = tk.Frame(root)
        """Frame principale du jeu. Elle contient toutes les autres frames"""
        self.main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.view = None
        """Vue associée au controlleur"""

    def start(self):
        """Lancement du controlleur"""
        self.view.draw()
        self.bind_base_buttons()

    def quit_game(self):
        """Fermeture du jeu"""
        self.root.destroy()

    def change_controller(self, change_to):
        """Changement de controlleur"""
        self.view.destroy()
        self.root.controller = change_to(self.root)
        self.root.controller.draw()

    def bind_base_buttons(self):
        # If present, bind the quit_button, the start_game button and the options button
        if hasattr(self.view, "quit_button"):
            self.view.quit_button.bind("<Button-1>",
                                       lambda event: self.quit_game())

        if hasattr(self.view, "start_game_button"):
            self.view.play_button.bind("<Button-1>",
                                             lambda event: self.change_controller(GameController))

        if hasattr(self.view, "options_button"):
            self.view.options_button.bind("<Button-1>",
                                          lambda event: self.change_controller(OptionsController))

        if hasattr(self.view, "highscore_button"):
            self.view.highscores_button.bind("<Button-1>",
                                            lambda event: self.change_controller(HighscoreController))

        if hasattr(self.view, "arsenal_button"):
            self.view.arsenal_button.bind("<Button-1>",
                                          lambda event: self.change_controller(ArsenalController))


class MenuController(Controller):
    """Controlleur du menu principal

    :argument root: Fenêtre principale du jeu

    :param self.root: Fenêtre principale du jeu
    :param self.main_frame: Frame graphique principale du jeu.
    :param self.view: Vue associée au controlleur
    """
    def __init__(self, root: tk):
        super().__init__(root)
        self.view = MenuView(self.main_frame)


class GameController(Controller):
    """Controlleur du jeu
    :argument root: Fenêtre principale du jeu

    :param self.root: Fenêtre principale du jeu
    :param self.main_frame: Frame graphique principale du jeu.
    :param self.view: Vue associée au controlleur
    """
    def __init__(self, root: tk):
        super().__init__(root)
        self.view = GameView(self.main_frame)


class ArsenalController(Controller):
    """Controlleur de l'arsenal

    :argument root: Fenêtre principale du jeu

    :param self.root: Fenêtre principale du jeu
    :param self.main_frame: Frame graphique principale du jeu.
    :param self.view: Vue associée au controlleur

    """
    def __init__(self, root: tk):
        super().__init__(root)
        self.view = ArsenalView(self.main_frame)


class HighscoreController(Controller):
    """Controlleur des highscores

    :argument root: Fenêtre principale du jeu

    :param self.root: Fenêtre principale du jeu
    :param self.main_frame: Frame graphique principale du jeu.
    :param self.view: Vue associée au controlleur
    """
    def __init__(self, root: tk):
        super().__init__(root)
        self.view = HighscoreView(self.main_frame)


class OptionsController(Controller):
    """Controlleur des options

    :argument root: Fenêtre principale du jeu

    :param self.root: Fenêtre principale du jeu
    :param self.main_frame: Frame graphique principale du jeu.
    :param self.view: Vue associée au controlleur
    """
    def __init__(self, root: tk):
        super().__init__(root)
        self.view = OptionsView(self.main_frame)
