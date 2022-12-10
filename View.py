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
from Container import BetterCanvas, BetterFrame, BetterLabel, BetterButton
from tkinter import PhotoImage
from PIL import Image, ImageTk
from abc import ABC


class View(ABC):
    """Classe abstraite de la vue

    :argument main_frame: Frame principale de la vue

    :param this.main_frame: Frame principale de la vue
    """
    def __init__(self, main_frame: BetterFrame):
        self.main_frame = main_frame

        self.background_width = 1200
        self.background_height = 800

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

    @staticmethod
    def img_format(file: str, dimensions: tuple[int, int]) -> PhotoImage:
        img = Image.open(file)
        img = img.resize(dimensions)
        img = img.convert('RGBA')
        data = img.getdata()
        
        new_data = []
        for item in data:
            if item[0] == 255 and item[1] == 255 and item[2] == 0:  # finding yellow colour
                # replacing it with a transparent value
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        
        img.putdata(new_data)
        return ImageTk.PhotoImage(img)


class MenuView(View):
    """Classe de la vue du menu
    :argument: main_frame: Frame principale de la vue
    :param: this.title: Label du titre du jeu
    """
    def __init__(self, main_frame: BetterFrame):
        super().__init__(main_frame)

        self.btn_width = 400
        self.btn_height = 200
        self.logo_width = 600
        self.logo_height = 200

        self.background_img = self.img_format(
            "Graphics/background.gif", (self.background_width,
                                        self.background_height)
        )
        self.logo_img = self.img_format(
            "Graphics/logo.png", (self.logo_width, self.logo_height)
        )
        self.play_img = self.img_format(
            "Graphics/play.png", (self.btn_width, self.btn_height)
        )
        self.arsenal_img = self.img_format(
            "Graphics/arsenal.png", (self.btn_width, self.btn_height)
        )
        self.options_img = self.img_format(
            "Graphics/options.png", (self.btn_width, self.btn_height)
        )
        self.highscores_img = self.img_format(
            "Graphics/highscores.png", (self.btn_width, self.btn_height)
        )
        self.quit_img = self.img_format(
            "Graphics/quit.png", (self.btn_width, self.btn_height)
        )
        self.main_canvas = BetterCanvas(self.main_frame, 0.5, 0.5,
                                        width=self.background_width,
                                        height=self.background_height,
                                        highlightthickness=0)

        self.background = self.main_canvas.create_image(
            self.background_width/2, self.background_height/2,
            image=self.background_img)

        self.logo = self.main_canvas.create_image(
            self.background_width/2, self.logo_height/2,
            image=self.logo_img)

        self.play_button = self.main_canvas.create_image(
            self.background_width*0.25, self.background_height*0.4,
            image=self.play_img)

        self.arsenal_button = self.main_canvas.create_image(
            self.background_width*0.75, self.background_height*0.4,
            image=self.arsenal_img)

        self.options_button = self.main_canvas.create_image(
            self.background_width*0.25, self.background_height*0.6,
            image=self.options_img)
        
        self.highscores_button = self.main_canvas.create_image(
            self.background_width*0.75, self.background_height*0.6,
            image=self.highscores_img)

        self.quit_button = self.main_canvas.create_image(
            self.background_width*0.5, self.background_height*0.8,
            image=self.quit_img)
            
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

        self.aliens = []
        self.player = None
        self.bullet = []

        self.player_width = 100
        self.player_height = 100
        self.alien_width = 50
        self.alien_height = 50 
        self.bullet_width = 50
        self.bullet_height = 50


        self.canvas = BetterCanvas(self.main_frame, 0.5, 0.5)
        self.canvas.config(bg="black", width=1200, height=800)


        
        self.background_img = self.img_format(
            "Graphics/background.gif", (self.background_width,
                                        self.background_height)
        )

        self.player_img = self.img_format(
            "Graphics/player.png", (self.player_width, self.player_height)
        )

        self.alien1_img = self.img_format(
            "Graphics/alien1.png", (self.alien_width, self.alien_height)
        )
        self.alien2_img = self.img_format(
            "Graphics/alien2.png", (self.alien_width, self.alien_height)
        )
        self.alien3_img = self.img_format(
            "Graphics/alien3.png", (self.alien_width, self.alien_height)
        )
        self.alien4_img = self.img_format(
            "Graphics/alien4.png", (self.alien_width, self.alien_height)
        )
        self.alien5_img = self.img_format(
            "Graphics/alien5.png", (self.alien_width, self.alien_height)
        )
        self.bullet_img = self.img_format(
            "Graphics/bullet.png", (self.bullet_width, self.bullet_height)
        )
        self.asteroid_img = self.img_format(
            "Graphics/asteroid.png", (self.bullet_width, self.bullet_height)
        )
        self.aliensType = {
            1: self.alien1_img,
            2: self.alien2_img,
            3: self.alien3_img,
            4: self.alien4_img,
            5: self.alien5_img
        }

        self.background = self.canvas.create_image(
            self.background_width/2, self.background_height/2,
            image=self.background_img)

        self.spawnPlayer(590,750)

    def draw(self):
        """Méthode de lancement de la vue"""
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")
        super(GameView, self).draw()

    def spawnPlayer(self, x, y):
        self.player = self.canvas.create_image(x, y, image=self.player_img)

    def spawnAlien(self,alien_type:int,x,y):
        self.aliens.append(
            self.canvas.create_image(x, y, image=self.aliensType[alien_type]))
    
    def spawnBullet(self,x,y):
        self.bullet.append(self.canvas.create_image
                           (x, y, image=self.bullet_img))

    def spawnAsteroid(self,x,y):
        self.asteroid = self.canvas.create_image(x,y,image = self.asteroid_img)

    def moveSprite(self, sprite, x, y):
        self.canvas.move(sprite, x, y)

    def deleteSprite(self, sprite):
        self.canvas.delete(sprite)
    def isVisible(self, sprite):
        # If the sprite is not visible (out of the window), return False
        x, y= self.canvas.coords(sprite)
        if x < 0 or x > self.canvas.winfo_width() or y < 0 or y > self.canvas.winfo_height():
            return False
        else:
            return True


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


    