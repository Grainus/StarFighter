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
from abc import ABC, abstractmethod
import random

from .Object import Object  # type: ignore
from .Position import Vecteur, Point  # type: ignore
from .Vaisseau import Vaisseau  # type: ignore


class Modifiers(Object, ABC):
    """Classe abstaite des modificateurs de vaisseau"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocity = Vecteur(0, 5)

    @abstractmethod
    def activate(self, player: Vaisseau) -> None: ...


class Health(Modifiers):
    """Modificateur de vaisseau: HP+"""
    def __init__(self, position: Point):
        super().__init__(position, width=25, height=25)

    def activate(self, player: Vaisseau):
        player.health += 25


# class Shield(Modifiers):
#     """Modificateur de vaisseau: Bouclier"""
#     def __init__(self, position: Point):
#         super().__init__(position, width=50, height=50)


# class Weapons(Modifiers):
#     """Modificateur de vaisseau: Armes"""
#     def __init__(self, position: Point):
#         super().__init__(position, width=50, height=50)


class Experience(Modifiers):
    """Objet qui donne des points en le touchant."""
    def __init__(self, position: Point, value: int, player: Vaisseau):
        super().__init__(position, width=10, height=10)
        self.velocity = Vecteur(0, random.random() * 10)
        self.value = value
        self.player = player
        self.acceleration = -0.1

    def activate(self):
        """Utilisé dans modèle directement."""
        pass

    def update(self) -> None:
        super().update()

        destination = self.player.center
        movevec = destination - self.position
        a = destination - self.center
        b = a.norme
        self.velocity += movevec.asnorm(75 / b)
        # if movevec.norme:
        #     movevec = movevec.asnorm(
        #             min(
        #                 movevec.norme,
        #                 self.max_speed
        #             )
        #     )
        #     self.position += movevec


ALLMODS = (Health,)
