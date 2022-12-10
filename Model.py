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
from abc import ABC
from typing import overload, Type, TypeVar, Any

from dataclasses import dataclass
from enum import Enum

from Objects.Object import Object
from Objects.Alien import Alien
from Objects.Modifiers import Modifiers
from Objects.Vaisseau import Vaisseau


ObjT1 = TypeVar("ObjT1", bound=Object)
ObjT2 = TypeVar("ObjT2", bound=Object)


@dataclass
class GameStats:
    enemies_killed: int = 0
    distance_traveled: float = 0

class Difficulty(Enum):
    """Représente une difficulté de jeu, et le multiplicateur de dégats
    qui y est associé.
    """
    EASY = 0.75
    NORMAL = 1
    HARD = 2
    EXTREME = 3
    IMPOSSIBLE = 10

class Model(ABC):
    def __init__(self):
        raise NotImplementedError



class GameModel(Model):
    """Contient la logique et l'état d'une partie en cours."""

    def __init__(self, difficulty: Difficulty):
        super().__init__()
        self.difficulty = difficulty
        self.player = Vaisseau()
        self.enemies: list[Alien] = []
        self.sprites: list[Object] = []
        self.stats = GameStats()

    @overload
    def get_collisions(
            self, instance: Object, cls: Type[ObjT1]
    ) -> list[ObjT1]: ...

    @overload
    def get_collisions(
            self, cls1: Type[ObjT1], cls2: Type[ObjT2]
    ) -> list[tuple[ObjT1, ObjT2]]: ...
    
    def get_collisions(
            self, arg: Object | Type[ObjT1], cls: Type[ObjT2]
    ) -> list[ObjT2] | list[tuple[ObjT1, ObjT2]]:
        """Retourne une liste d'objets en collision.

        Args:
            arg: L'objet ou le type principal.
            cls: La classe des objets qu'on veut comparer.

        Returns:
            Si le premier paramètre est un objet, une liste de tous les
            objets de type `cls` qui sont en collision avec `arg`.
            Si le premier paramètre est un type, une liste de tuples
            contenants toutes les paires d'objets de type `arg` et `cls`
            qui sont en collision.
        """
        if isinstance(arg, type):
            return [
                (obj1, obj2)
                for obj1 in self.sprites
                if isinstance(obj1, arg)
                for obj2 in self.sprites
                if isinstance(obj2, cls)
                if obj1.collides(obj2)
            ]
        else:
            return [
                obj
                for obj in self.sprites
                if isinstance(obj, cls)
                if obj.collides(obj)
            ]

    def update(self) -> None:
        """Met à jour la position de tous les objets."""
        for obj in self.sprites:
            obj.update()

    def start_wave(self, *args):
        """Débute une vague d'ennemis"""
        raise NotImplementedError


class HighscoreModel(Model):
    def __init__(self):
        raise NotImplementedError


class ArsenalModel(Model):
    def __init__(self):
        raise NotImplementedError


class OptionsModel(Model):
    def __init__(self):
        raise NotImplementedError
