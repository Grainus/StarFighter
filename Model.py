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
from typing import overload, Type, TypeVar, Callable

from dataclasses import dataclass
from enum import Enum
import random

from Objects.Object import Object  # type: ignore
from Objects.AliveObject import AliveObject  # type: ignore
from Objects.Alien import Alien  # type: ignore
from Objects.Asteroid import Asteroid  # type: ignore
from Objects.Bullet import Bullet  # type: ignore
from Objects.Modifiers import ALLMODS, Experience, Modifiers  # type: ignore
from Objects.Position import Point  # type: ignore
from Objects.Vaisseau import Vaisseau  # type: ignore


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



class GameModel:
    """Contient la logique et l'état d'une partie en cours."""

    def __init__(self, difficulty: Difficulty):
        self.difficulty = difficulty
        self.player = Vaisseau(Point(590, 750))
        self.sprites: list[Object] = [self.player]
        self.stats = GameStats()
        self.score = 0

    @overload
    def get_collisions(
            self, arg: Type[ObjT1], cls: Type[ObjT2]
    ) -> list[tuple[ObjT1, ObjT2]]: ...

    @overload
    def get_collisions(
            self, arg: Type[ObjT1], cls: tuple[Type[Object], ...]
    ) -> list[tuple[ObjT1, Object]]: ...

    @overload
    def get_collisions(
            self, arg: Object, cls: Type[ObjT1]
    ) -> list[ObjT1]: ...

    @overload
    def get_collisions(
            self, arg: Object, cls: tuple[Type[Object], ...]
    ) -> list[Object]: ...

    def get_collisions(
            self, arg: Object | Type[ObjT1],
            cls: Type[ObjT2] | tuple[Type[Object], ...],
    ):
        """Retourne une liste d'objets en collision.

        Args:
            arg: L'objet ou le type principal.
            cls: La ou les classes des objets qu'on veut comparer.

        Returns:
            Si le premier paramètre est un objet, une liste de tous les
            objets de type `cls` qui sont en collision avec `arg`.
            Si le premier paramètre est un type, une liste de tuples
            contenants toutes les paires d'objets de type `arg` et `cls`
            qui sont en collision.
        """
        comparelist = self.get_all_of(cls)
        if isinstance(arg, (type, tuple)):
            return [
                (obj1, obj2)
                for obj1 in self.get_all_of(arg)
                for obj2 in comparelist
                if obj1.collides(obj2)
                and obj1 is not obj2
            ]
        else:
            return [
                obj
                for obj in comparelist
                if obj.collides(arg)
            ]

    def collisions_update(self) -> set[Object]:
        # TODO: Could probably be done in a single loop
        out: set[Object] = set()

        # Collisions avec le joueur
        for obj in self.get_collisions(self.player, (Alien, Asteroid)):
            self.player.hit(obj.damage)
            out.add(obj)

        # Collisions balles
        for (bullet, victim) in self.get_collisions(Bullet, AliveObject):
            if bullet.side != victim.side and bullet not in out:
                victim.hit(bullet.damage)
                out.add(bullet)
                if not victim.alive():
                    out.add(victim)
                    if bullet.side == self.player.side:
                        self.stats.enemies_killed += 1
                        self.score += 1

        # Collisions exp
        for exp in self.get_collisions(self.player, Experience):
            self.score += exp.value
            out.add(exp)

        # Modifiers exp
        for mod in self.get_collisions(self.player, ALLMODS):
            mod.activate(self.player)
            out.add(mod)

        return out

    def update(self, *, kill_if: Callable[[Object], bool]) -> set[Object]:
        """Met à jour la position de tous les objets et vérifie les
        collisions.
        """
        out: set[Object] = set()
        for obj in self.sprites:
            obj.update()
            if kill_if(obj):
                out.add(obj)

        out.update(self.collisions_update())

        for obj in out:
            self.sprites.remove(obj)

        return out

    def spawn_alien(self, maxwidth: float) -> Alien:
        alien = Alien(Point(random.random()*maxwidth, 0))
        self.sprites.append(alien)
        return alien

    def spawn_asteroid(self, maxwidth: float) -> Asteroid:
        asteroid = Asteroid(Point(random.random()*maxwidth, 0))
        self.sprites.append(asteroid)
        return asteroid

    def spawn_modifier(self, maxwidth: float) -> Modifiers:
        modtype = random.choice(ALLMODS)
        mod = modtype(Point(random.random()*maxwidth, 0))
        self.sprites.append(mod)
        return mod

    def spawn_experience(self, maxwidth: float, val: int = None) -> Experience:
        val = val or int(self.difficulty.value)  # Easy ne donne pas d'exp
        exp = Experience(Point(random.random()*maxwidth, 0), val, self.player)
        self.sprites.append(exp)
        return exp

    def shoot(
            self, 
            shooter: AliveObject | Type[AliveObject] | tuple[Type[AliveObject], ...]
    ) -> Bullet:
        """Crée et retourne une balle tirée par l'objet passé en
        paramètre.
        
        Si `shooter` est une instance, la balle est tirée par cet objet.
        Si `shooter` est un type ou tuple de types, la balle est tirée
        par un objet aléatoire qui est une instance directe.
        """
        if isinstance(shooter, (type, tuple)):
            shooters: list[AliveObject] = self.get_all_of(shooter)
            bullet = random.choice(shooters).shoot()
        else:
            bullet = shooter.shoot()
        self.sprites.append(bullet)
        return bullet

    @overload
    def get_all_of(self, cls: Type[ObjT1]) -> list[ObjT1]: ...

    @overload
    def get_all_of(self, cls: tuple[Type[Object], ...]) -> list[Object]: ...

    def get_all_of(self, cls: Type[ObjT1] | tuple[Type[Object], ...]):
        """Retourne tous les sprites d'une ou plusieurs classes."""
        return [obj for obj in self.sprites if isinstance(obj, cls)]


class HighscoreModel(Model):
    def __init__(self):
        raise NotImplementedError


class ArsenalModel(Model):
    def __init__(self):
        raise NotImplementedError


class OptionsModel(Model):
    def __init__(self):
        raise NotImplementedError
