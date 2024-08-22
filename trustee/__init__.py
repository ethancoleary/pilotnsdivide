import random

from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'trustee'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    partner = models.LongStringField()



# PAGES
class Intro(Page):

    @staticmethod
    def vars_for_template(player):
        if player.participant.group ==1 and player.participant.ingroup==1:
            player.partner = "Northern"
            partner = "also be a Northerner"
        if player.participant.group ==0 and player.participant.ingroup==0:
            player.partner = "Northern"
            partner = "be a Northerner"
        if player.participant.group ==1 and player.participant.ingroup==0:
            player.partner = "Southern"
            partner = "be a Southerner"
        if player.participant.group ==0 and player.participant.ingroup==1:
            player.partner = "Southern"
            partner= "also be a Southerner"



class StageOneIntro(Page):

    @staticmethod
    def vars_for_template(player):
        if player.participant.group == 1 and player.participant.ingroup == 1:
            partner = "also a Northerner"
        if player.participant.group == 0 and player.participant.ingroup == 0:
            partner = " a Northerner"
        if player.participant.group == 1 and player.participant.ingroup == 0:
            partner = "a Southerner"
        if player.participant.group == 0 and player.participant.ingroup == 1:
            partner = "also a Southerner"


class Results(Page):
    pass


page_sequence = [Intro, StageOneIntro]
