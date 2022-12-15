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
import random
import tkinter as tk
from abc import ABC  # Classe abstraite

from Highscore import HighScore
from Container import BetterFrame
from View import (
    View,
    MenuView,
    GameView,
    HighscoreView,
    OptionsView,
    ArsenalView,
    GameOverView
)
from Model import GameModel, Difficulty
from Objects.Position import Point  # type: ignore
from Objects.Alien import Alien, ALIENTYPES  # type: ignore
from Objects.Modifiers import Experience

class Controller(ABC):
    """Classe abstraite des controlleurs
    :argument root: Fenêtre principale du jeu

    :param self.root: Fenêtre principale du jeu
    :param self.main_frame: Frame principale graphique du jeu.
    :param self.view: Vue associée au controlleur
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        """En quelque sorte, il s'agit de la fenêtre principale du jeu
        qui est aussi responsable de sa boucle principale."""

        self.main_frame = BetterFrame(root, 0, 0)
        """Frame principale du jeu. Elle contient toutes les autres frames"""
        self.main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.view: View
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
    def __init__(self, root: tk.Tk):
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


        super().start()


class GameController(Controller):
    """Controlleur du jeu
    :argument root: Fenêtre principale du jeu

    :param self.root: Fenêtre principale du jeu
    :param self.main_frame: Frame graphique principale du jeu.
    :param self.view: Vue associée au controlleur
    """
    def __init__(self, root: tk.Tk):
        super().__init__(root)
        self.eventPos = (1, 1)
        self.view: GameView = GameView(self.main_frame)
        self.game = GameModel(Difficulty.NORMAL)
        self.game.player.id = self.view.spawnPlayer(590, 750)
        self.bind_mouse_pregame()
        self._enemy_spawn = True

        self.ennemy_spawn_timer_max = 50
        self.asteroid_spawn_timer_max = 120

        self.ennemy_spawn_timer = random.randint(
                0, self.ennemy_spawn_timer_max
        )
        self.asteroid_spawn_timer = random.randint(
                0, self.asteroid_spawn_timer_max
        )

    def start(self):
        super().start()

    def initalize_game(self):
        """Initialisation du jeu"""
        self.bind_mouse_game()

    def bind_mouse_pregame(self):
        """Bind les boutons de la souris avant le début du jeu"""
        self.view.canvas.bind("<Button-1>", lambda event: self.initalize_game())

    def bind_mouse_game(self):
        """Bind du carré à la souris afin qu'il suive le curseur"""
        self.view.canvas.bind("<Motion>", self.mouse_listener_move)
        self.view.canvas.bind("<Button-1>", self.mouse_listener_left_click)
        self.view.canvas.bind("<Button-3>", self.debug_mouse_listener)
        self.tick()

    def mouse_listener_move(self, event):
        """Déplacement du carré"""
        self.eventPos = (event.x, event.y)

    def mouse_listener_left_click(self, event):
        """Création d'un projectile"""
        bullet = self.game.shoot(self.game.player)
        bullet.id = self.view.spawnBullet(*bullet.position)

    def debug_mouse_listener(self, *_):
        """Toggle les nouveaux objets"""
        self._enemy_spawn = not self._enemy_spawn

    def player_movement(self):
        """Déplacement du joueur"""
        destination = Point(*self.eventPos)
        player = self.game.player  # Simpler alias
        destination.x -= player.dimension.width / 2
        destination.y -= player.dimension.height / 2
        player.move_to(destination)
        self.game.player.update()
        self.view.canvas.moveto(self.game.player.id, *player.position)

    def tick(self):
        """Méthode appelée à chaque tick du jeu"""
        width = self.view.dimension.width
        if self._enemy_spawn:
            if self.asteroid_spawn_timer == 0:
                asteroid = self.game.spawn_asteroid(width)
                asteroid.id = self.view.spawnAsteroid(*asteroid.position)
                self.asteroid_spawn_timer = random.randint(
                        0, self.asteroid_spawn_timer_max
                )
            else:
                self.asteroid_spawn_timer -= 1

            if self.ennemy_spawn_timer == 0:
                alien = self.game.spawn_alien(width)
                alien.id = self.view.spawnAlien(
                        random.choice(ALIENTYPES), *alien.position
                )
                self.ennemy_spawn_timer = random.randint(
                        0, self.ennemy_spawn_timer_max
                )
            else:
                self.ennemy_spawn_timer -= 1
            
            if random.random() < 0.25 and self.game.get_all_of(Alien):
                bullet = self.game.shoot(Alien)
                bullet.id = self.view.spawnBulletAlien(*bullet.center)
            
            if random.random() < 0.005:
                mod = self.game.spawn_modifier(width)
                mod.id = self.view.spawnModifier(mod)
        
        if random.random() < 0.02:
            exp = self.game.spawn_experience(width)
            exp.id = self.view.spawnModifier(exp)

        # Effectue le mouvement du joueur
        self.player_movement()

        # Déplace tous les objets et les retire s'ils sont hors de l'écran

        killcond = lambda obj: (
                not self.view.isVisible(obj.id)
                and obj.position.y > obj.dimension.height
                and obj.__class__ is not Experience
        )

        self.view.updateScore(self.game.score)

        for trash in self.game.update(kill_if=killcond):
            self.view.deleteSprite(trash.id)

        for obj in self.game.sprites:
            self.view.moveSprite(obj.id, *obj.position)

        if self.game.player.alive():
            self.view.canvas.after(16, self.tick)
        else:
            self.change_controller(GameOverController)
            print(f"Your score: {self.game.score}")
            self.root.controller.score =self.game.score
            self.root.controller.show_score()
            


class ArsenalController(Controller):
    """Controlleur de l'arsenal

    :argument root: Fenêtre principale du jeu

    :param self.root: Fenêtre principale du jeu
    :param self.main_frame: Frame graphique principale du jeu.
    :param self.view: Vue associée au controlleur

    """
    def __init__(self, root: tk.Tk):
        super().__init__(root)
        self.view = ArsenalView(self.main_frame)


class HighscoreController(Controller):
    """Controlleur des highscores

    :argument root: Fenêtre principale du jeu

    :param self.root: Fenêtre principale du jeu
    :param self.main_frame: Frame graphique principale du jeu.
    :param self.view: Vue associée au controlleur
    """
    def __init__(self, root: tk.Tk):
        super().__init__(root)
        self.view = HighscoreView(self.main_frame)
        self.view.main_canvas.tag_bind(self.view.menu_button, "<Button-1>",
                                       lambda event:
                                       self.change_controller(MenuController))
        self.view.load_scores(HighScore.get_scores())
        # Saving score: Highscore.save_score(name, score)
        # Getting score: HighScore.get_scores()

class GameOverController(Controller):
    """Controlleur de la fin de partie

    :argument root: Fenêtre principale du jeu

    :param self.root: Fenêtre principale du jeu
    :param self.main_frame: Frame graphique principale du jeu.
    :param self.view: Vue associée au controlleur

    """
    def __init__(self, root: tk.Tk):
        super().__init__(root)
        self.view = GameOverView(self.main_frame)
        self.score = 0
        self.view.name_entry.bind("<Return>", self.on_submit)
        self.view.name_entry.focus_set()

    def show_score(self):
        self.view.show_score(self.score)

    def on_submit(self,_):
        self.name = self.view.name_entry.get() 
        if(self.name):
            HighScore.save_score(self.name,self.score)
        self.change_controller(HighscoreController)

class OptionsController(Controller):
    """Controlleur des options

    :argument root: Fenêtre principale du jeu

    :param self.root: Fenêtre principale du jeu
    :param self.main_frame: Frame graphique principale du jeu.
    :param self.view: Vue associée au controlleur
    """
    def __init__(self, root: tk.Tk):
        super().__init__(root)
        self.view = OptionsView(self.main_frame)

        self.view.main_canvas.tag_bind(self.view.menu_button, "<Button-1>",
                                       lambda event:
                                       self.change_controller(MenuController))
