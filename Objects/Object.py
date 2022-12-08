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
from __future__ import annotations
from abc import ABC

from Position import Vecteur, Point, Dimension2D

class Object(ABC):
    """Classe abstraite représentant un objet du jeu quel qu'il soit."""
    def __init__(self, position: Point, width: float, height: float):
        self.dimension = Dimension2D(width, height)
        self.position = position
        """Centre de l'objet"""
        self.points = self.dimension.to_points(self.position, True)  # TODO: remove duplicate code (maybe remove annotation)
        """Points supérieur gauche ↖ et inférieur droit ↘ de l'objeté"""
        self.velocity = Vecteur(0, 0)
        self.acceleration: float = 0

    def _update_points(self) -> None:
        self.points = self.dimension.to_points(self.position, True)

    @property
    def width(self):
        return self.dimension.width

    @width.setter
    def width(self, value):
        self.dimension.width = value
        self._update_points()

    @property
    def height(self):
        return self.dimension.height

    @height.setter
    def height(self, value):
        self.dimension.height = value
        self._update_points()

    @property
    def speed(self) -> float:
        return self.velocity.norme

    @speed.setter
    def speed(self, value) -> None:
        self.velocity.norme = value

    def collides(self, other: Object) -> bool:
        """Vérifie si deux objets sont en collision"""
        overlap_x = (
            self.points[0].x <= other.points[0].x <= self.points[1].x or
            self.points[0].x <= other.points[1].x <= self.points[1].x
        )
        overlap_y = (
            self.points[0].y <= other.points[0].y <= self.points[1].y or
            self.points[0].y <= other.points[1].y <= self.points[1].y
        )

        return overlap_x and overlap_y

    def update(self) -> None:
        """Mise à jour de la position de l'objet selon sa vélocité"""
        self.speed += self.acceleration
        self.position += self.velocity
