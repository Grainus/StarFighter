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
""" Ce module est une adaptation de Tkinter pour le jeu StarFighter.

Il contient les classes suivantes:
    - BetterButton
    - Container
    - BetterLabel
"""

from tkinter import Frame as Frame, Label as Label, Button as Button


class BetterButton(Button):
    """Classe représentant un bouton tkinter modifiè pour le programme.
    Elle hérite de la classe tkinter.BetterButton.
    :param master: Le parent du bouton.
    :param x: La position x du bouton.
    :param y: La position y du bouton.
    :param kwargs: Les arguments de la classe tkinter.BetterButton.

    :keyword text: Le texte du bouton.
    :keyword command: La commande du bouton.
    :keyword width: La largeur du bouton.
    :keyword height: La hauteur du bouton.
    :keyword bg: La couleur de fond du bouton.
    :keyword fg: La couleur du texte du bouton.
    :keyword font: La police du texte du bouton.
    :keyword relief: Le relief du bouton.
    :keyword bd: La bordure du bouton.
    :keyword activebackground: La couleur de fond du bouton quand il est activé.
    :keyword activeforeground: La couleur du texte du bouton quand il est activé.
    :keyword cursor: Le curseur quand il est au dessus du bouton.
    :keyword anchor: L’ancrage du texte du bouton.
    :keyword image: L’image du bouton.
    :keyword state: L’état du bouton.
    :keyword padx: La marge horizontale du bouton.
    :keyword pady: La marge verticale du bouton.
    ... (voir la documentation de tkinter.BetterButton pour plus d’informations)

    :return: Un bouton tkinter modifié pour le programme.
    """
    def __init__(self, master, x: float, y: float, **kwargs):
        super().__init__(master, **kwargs)
        self.x = x
        self.y = y


class BetterLabel(Label):
    """Classe représentant un label tkinter modifié pour le programme.
    Elle hérite de la classe tkinter.BetterLabel.
    :param master: Le parent du label.
    :param x: La position x du label.
    :param y: La position y du label.

    :keyword text: Le texte du bouton.
    :keyword command: La commande du bouton.
    :keyword width: La largeur du bouton.
    :keyword height: La hauteur du bouton.
    :keyword bg: La couleur de fond du bouton.
    :keyword fg: La couleur du texte du bouton.
    :keyword font: La police du texte du bouton.
    :keyword relief: Le relief du bouton.
    :keyword bd: La bordure du bouton.
    :keyword activebackground: La couleur de fond du bouton quand il est activé.
    :keyword activeforeground: La couleur du texte du bouton quand il est activé.
    :keyword cursor: Le curseur quand il est au dessus du bouton.
    :keyword anchor: L’ancrage du texte du bouton.
    :keyword image: L’image du bouton.
    :keyword state: L’état du bouton.
    :keyword padx: La marge horizontale du bouton.
    :keyword pady: La marge verticale du bouton.
    ... (voir la documentation de tkinter.BetterLabel pour plus d’informations)

    :return: Un label tkinter modifié pour le programme.
    """
    def __init__(self, master, x: float, y: float, **kwargs):
        super().__init__(master, **kwargs)
        self.x = x
        self.y = y


class BetterFrame(Frame):
    """Classe représentant une frame tkinter modifié pour le programme.
    Elle hérite de la classe tkinter.Frame.

    :param master: Le parent du frame.
    :param x: La position x du frame.
    :param y: La position y du frame.
    :param kwargs: Les arguments de la classe tkinter.Frame.

    :keyword text: Le texte du bouton.
    :keyword command: La commande du bouton.
    :keyword width: La largeur du bouton.
    :keyword height: La hauteur du bouton.
    :keyword bg: La couleur de fond du bouton.
    :keyword fg: La couleur du texte du bouton.
    :keyword font: La police du texte du bouton.
    :keyword relief: Le relief du bouton.
    :keyword bd: La bordure du bouton.
    :keyword activebackground: La couleur de fond du bouton quand il est activé.
    :keyword activeforeground: La couleur du texte du bouton quand il est activé.
    :keyword cursor: Le curseur quand il est au dessus du bouton.
    :keyword anchor: L’ancrage du texte du bouton.
    :keyword image: L’image du bouton.
    :keyword state: L’état du bouton.
    :keyword padx: La marge horizontale du bouton.
    :keyword pady: La marge verticale du bouton.
    ... (voir la documentation de tkinter.Frame pour plus d’informations)

    :return: Un frame tkinter modifié pour le programme.
    """
    def __init__(self, master, x: float, y: float, **kwargs):
        super().__init__(master, **kwargs)
        self.x = x
        self.y = y
