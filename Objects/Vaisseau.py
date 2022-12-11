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
from .Object import Object  # type: ignore
from .Position import Vecteur, Point  # type: ignore

class Vaisseau(Object):
    """Classe représentant un vaisseau joueur."""
    def __init__(self, position: Point):
        super().__init__(position, width=100, height=100)
        self.max_speed = 10
        self.firepower = 25
        self.health = 100

    def move_to(self, destination: Point) -> None:
        movevec = destination - self.position
        if movevec.norme:
            movevec = movevec.asnorm(min(movevec.norme, self.max_speed))
            self.position += movevec

    def hit(self, damage: int) -> None:
        self.health -= damage