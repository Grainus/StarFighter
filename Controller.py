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
from random import random
from tkinter import Tk
from Container import BetterFrame
from abc import ABC  # Classe abstraite

from View import MenuView, GameView, HighscoreView, OptionsView, ArsenalView


class Controller(ABC):
    """Classe abstraite des controlleurs
    :argument root: Fenêtre principale du jeu

    :param self.root: Fenêtre principale du jeu
    :param self.main_frame: Frame principale graphique du jeu.
    :param self.view: Vue associée au controlleur
    """

    def __init__(self, root: Tk):
        self.root = root
        """En quelque sorte, il s'agit de la fenêtre principale du jeu
        qui est aussi responsable de sa boucle principale."""

        self.main_frame = BetterFrame(root, 0, 0)
        """Frame principale du jeu. Elle contient toutes les autres frames"""
        self.main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.view = None
        """Vue associée au controlleur"""

    def start(self):
        """Lancement du controlleur"""
        self.view.draw()

    def quit_game(self):
        """Fermeture du jeu"""
        self.root.destroy()

    def change_controller(self, change_to):
        """Changement de controlleur"""
        self.view.destroy()
        self.root.controller = change_to(self.root)
        self.root.controller.start()


class MenuController(Controller):
    """Controlleur du menu principal

    :argument root: Fenêtre principale du jeu

    :param self.root: Fenêtre principale du jeu
    :param self.main_frame: Frame graphique principale du jeu.
    :param self.view: Vue associée au controlleur
    """

    def __init__(self, root: Tk):
        super().__init__(root)
        self.view = MenuView(self.main_frame)

    def start(self):
        self.view.main_canvas.tag_bind(self.view.quit_button,
                                       "<Button-1>",
                                       lambda _: self.quit_game())

        self.view.main_canvas.tag_bind(self.view.play_button,
                                       "<Button-1>",
                                       lambda _:
                                       self.change_controller(GameController))

        self.view.main_canvas.tag_bind(self.view.options_button,
                                       "<Button-1>",
                                       lambda _:
                                       self.change_controller
                                       (OptionsController))

        self.view.main_canvas.tag_bind(self.view.highscores_button,
                                       "<Button-1>",
                                       lambda _:
                                       self.change_controller
                                       (HighscoreController))

        self.view.main_canvas.tag_bind(self.view.arsenal_button,
                                       "<Button-1>",
                                       lambda _:
                                       self.change_controller
                                       (ArsenalController))

        super().start()


class GameController(Controller):
    """Controlleur du jeu
    :argument root: Fenêtre principale du jeu

    :param self.root: Fenêtre principale du jeu
    :param self.main_frame: Frame graphique principale du jeu.
    :param self.view: Vue associée au controlleur
    """

    def __init__(self, root: Tk):
        super().__init__(root)
        self.eventPos = (0,0)
        self.view = GameView(self.main_frame)
        self.bind_mouse_pregame()

    def start(self):
        super().start()

    def initalize_game(self):
        """Initialisation du jeu"""
        # TODO: Config.get_instant()
        self.bind_mouse_game()

    def bind_mouse_pregame(self):
        """Bind les boutons de la souris avant le début du jeu"""
        self.view.canvas.bind("<Button-1>", lambda event: self.initalize_game())

    def bind_mouse_game(self):
        """Bind du carré à la souris afin qu'il suive le curseur"""
        self.view.canvas.bind("<Motion>", self.mouse_listener_move)
        self.view.canvas.bind("<Button-1>", self.mouse_listener_left_click)
        self.view.canvas.bind("<Button-3>", self.mouse_listener_right_click)
        self.tick()

    def mouse_listener_move(self, event):
        """Déplacement du carré"""
        self.eventPos = (event.x, event.y)

    def mouse_listener_left_click(self, event):
        """Création d'un projectile"""
        player_pos = self.view.canvas.coords(self.view.player)
        self.view.spawnBullet(player_pos[0], player_pos[1])

    def mouse_listener_right_click(self, event):
        """Création d'un ennemi"""
        # Debug ALIEN
        # Random x from the screen width
        randX = random() * self.view.canvas.winfo_width()
        self.view.spawnAlien(1, randX, 0)

    def player_movement(self):
        """Déplacement du joueur"""
        playerX = self.view.canvas.coords(self.view.player)[0]
        playerY = self.view.canvas.coords(self.view.player)[1]
        speed = 10



        if self.eventPos[0] - playerX > speed:
            self.view.canvas.move(self.view.player, speed, 0)
        elif self.eventPos[0] - playerX < -speed:
            self.view.canvas.move(self.view.player, -speed, 0)
        if self.eventPos[1] - playerY > speed:
            self.view.canvas.move(self.view.player, 0, speed)
        elif self.eventPos[1] - playerY < -speed:
            self.view.canvas.move(self.view.player, 0, -speed)


    def tick(self):
        """Méthode appelée à chaque tick du jeu"""
        self.player_movement()

        for bullet in self.view.bullet:
            if self.view.isVisible(bullet):
                self.view.moveSprite(bullet, 0, -10)
            else:
                self.view.deleteSprite(bullet)
                self.view.bullet.remove(bullet)

        for alien in self.view.aliens:
            if self.view.isVisible(alien):
                self.view.moveSprite(alien, 0, 10)
            else:
                self.view.deleteSprite(alien)
                self.view.aliens.remove(alien)


        #60 fps
        self.view.canvas.after(16, self.tick)



class ArsenalController(Controller):
    """Controlleur de l'arsenal

    :argument root: Fenêtre principale du jeu

    :param self.root: Fenêtre principale du jeu
    :param self.main_frame: Frame graphique principale du jeu.
    :param self.view: Vue associée au controlleur

    """

    def __init__(self, root: Tk):
        super().__init__(root)
        self.view = ArsenalView(self.main_frame)


class HighscoreController(Controller):
    """Controlleur des highscores

    :argument root: Fenêtre principale du jeu

    :param self.root: Fenêtre principale du jeu
    :param self.main_frame: Frame graphique principale du jeu.
    :param self.view: Vue associée au controlleur
    """

    def __init__(self, root: Tk):
        super().__init__(root)
        self.view = HighscoreView(self.main_frame)


class OptionsController(Controller):
    """Controlleur des options

    :argument root: Fenêtre principale du jeu

    :param self.root: Fenêtre principale du jeu
    :param self.main_frame: Frame graphique principale du jeu.
    :param self.view: Vue associée au controlleur
    """
    
    def __init__(self, root: Tk):
        super().__init__(root)
        self.view = OptionsView(self.main_frame)
