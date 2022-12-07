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

from Container import BetterButton, BetterLabel, BetterFrame
from tkinter import Frame,PhotoImage
from typing import TYPE_CHECKING
import os.path
from PIL import Image, ImageTk

class View:
    """Classe abstraite de la vue

    :argument main_frame: Frame principale de la vue

    :param this.main_frame: Frame principale de la vue
    """
    def __init__(self, main_frame: Frame):
        self.main_frame = main_frame

    def draw(self):
        """Méthode abstraite de lancement de la vue"""
        # Recursively place all the widgets in the frame
        self.place_children(self.main_frame)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

    def place_children(self, container):
        """Méthode abstraite de placement des widgets de la vue"""
        for widget in container.winfo_children():
            if widget.winfo_children():
                self.place_children(widget)
            widget.place(relx=widget.x, rely=widget.y, anchor="center")

    def destroy(self):
        """Méthode de destruction de la vue"""
        for content in self.main_frame.winfo_children():
            content.destroy()
        self.main_frame.destroy()

    def forget(self):
        """Méthode d'oublie de la vue"""
        for content in self.main_frame.winfo_children():
            content.pack_forget()
        self.main_frame.pack_forget()

    def img_resize(self, file: str, dimensions: tuple[int, int]) -> PhotoImage:
        img = Image.open(file)
        img = img.resize(dimensions)
        img = img.convert('RGB')

        return ImageTk.PhotoImage(img)


class MenuView(View):
    """Classe de la vue du menu

    :argument main_frame: Frame principale de la vue

    :param this.main_frame: Frame principale de la vue
    :param this.title: BetterLabel du titre
    :param this.buttonContainer: Container des boutons
    :param this.quit_button: Bouton de fermeture du jeu
    """
    def __init__(self, main_frame: Frame):
        super().__init__(main_frame)

        self.btn_width = 400
        self.btn_height = 200
        self.logo_width = 600
        self.logo_height = 200

        self.background_img = self.img_resize(
            "Graphics/background.gif",(1200,800)
        )
        self.logo_img = self.img_resize(
            "Graphics/logo.png",(self.logo_width,self.logo_height)
        )
        self.play_img = self.img_resize(
            "Graphics/play.png",(self.btn_width,self.btn_height)
        )
        self.arsenal_img = self.img_resize(
            "Graphics/arsenal.png",(self.btn_width,self.btn_height)
        )
        self.options_img = self.img_resize(
            "Graphics/options.png",(self.btn_width,self.btn_height)
        )
        self.highscores_img = self.img_resize(
            "Graphics/highscores.png",(self.btn_width,self.btn_height)
        )
        self.quit_img = self.img_resize(
            "Graphics/quit.png",(self.btn_width,self.btn_height)
        )
        
        self.background = BetterLabel(self.main_frame,0.5,0.5,image=self.background_img)
        self.logo = BetterLabel(self.main_frame, 0.5, 0.1, image=self.logo_img,width=self.logo_width,height=self.logo_height)
        
        self.play_button = BetterButton(self.main_frame, 0.25, 0.4, image=self.play_img,borderwidth=0,width=self.btn_width,height=self.btn_height)
        self.arsenal_button = BetterButton(self.main_frame, 0.75, 0.4, image=self.arsenal_img,borderwidth=0,width=self.btn_width,height=self.btn_height)
        self.options_button = BetterButton(self.main_frame, 0.25, 0.65, image=self.options_img,borderwidth=0,width=self.btn_width,height=self.btn_height)
        self.highscores_button = BetterButton(self.main_frame, 0.75, 0.65, image=self.highscores_img,borderwidth=0,width=self.btn_width,height=self.btn_height)
        self.quit_button = BetterButton(self.main_frame, 0.5, 0.9, image=self.quit_img,borderwidth=0)


    def draw(self):
        """Méthode de lancement de la vue"""
        super(MenuView, self).draw()


class GameView(View):
    """Classe de la vue du jeu

    :argument main_frame: Frame principale de la vue

    :param this.main_frame: Frame principale de la vue
    """
    def __init__(self, main_frame: Frame):
        super().__init__(main_frame)


class HighscoreView(View):
    """Classe de la vue des highscores

    :argument main_frame: Frame principale de la vue

    :param this.main_frame: Frame principale de la vue
    """
    def __init__(self, main_frame: Frame):
        super().__init__(main_frame)


class OptionsView(View):
    """Classe de la vue des options

    :argument main_frame: Frame principale de la vue

    :param this.main_frame: Frame principale de la vue
    """
    def __init__(self, main_frame: Frame):
        super().__init__(main_frame)


class ArsenalView(View):
    """Classe de la vue de l'arsenal
    :argument main_frame: Frame principale de la vue

    :param this.main_frame: Frame principale de la vue
    """
    def __init__(self, main_frame: Frame):
        super().__init__(main_frame)
