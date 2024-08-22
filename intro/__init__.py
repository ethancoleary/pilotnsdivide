import random

from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'workshop_overview_app'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent = models.IntegerField(initial=0)
    age = models.IntegerField(
        choices=[
            [1, '<20 years'],
            [2, '20-29 years'],
            [3, '30-39 years'],
            [4, '40-49 years'],
            [5, '50-59 years'],
            [6, '60-69 years'],
            [7, '70 years and over']
        ],
        widget=widgets.RadioSelect
    )
    education = models.IntegerField(
        choices=[
            [1, 'Did not graduate high school'],
            [2, 'High school graduate'],
            [3, 'Some college education'],
            [4, 'Undergraduate degree'],
            [5, 'Postgraduate degree']
        ],
        widget=widgets.RadioSelect
    )
    accepted = models.IntegerField(initial=0)
    english_by_birth = models.IntegerField(initial=1)
    region_of_birth = models.IntegerField(
        choices=[
            [1, 'East of England'],
            [2, 'East Midlands'],
            [3, 'London'],
            [4, 'North East'],
            [5, 'North West'],
            [6, 'South East'],
            [7, 'South West'],
            [8, 'Yorkshire and the Humber'],
        ], widget=widgets.RadioSelect
    )
    currently_live_in_england = models.IntegerField()
    region_of_domicile = models.IntegerField(
        choices=[
            [1, 'East of England'],
            [2, 'East Midlands'],
            [3, 'London'],
            [4, 'North East'],
            [5, 'North West'],
            [6, 'South East'],
            [7, 'South West'],
            [8, 'Yorkshire and the Humber']
        ], widget=widgets.RadioSelect
    )
    regional_identity = models.IntegerField(
        choices=[
            [1, 'Midlander'],
            [2, 'Northerner'],
            [3, 'Southerner'],
            [4, 'None of the above']
        ]
    )
    northern = models.IntegerField(initial=0)
    southern = models.IntegerField(initial=0)

# PAGES
class Intro(Page):
    form_model = 'player'
    form_fields = ['consent']

    @staticmethod
    def error_message(player, values):
        solutions = dict(consent=1)
        if values != solutions:
            return "Please consent to participation or withdraw from the experiment by closing your browser."

class English(Page):
    form_model = 'player'
    form_fields = ['english_by_birth']

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.english_by_birth == 1:
            player.accepted = 1
        else:
            player.accepted = 0

class Birth(Page):
    form_model = 'player'
    form_fields = ['region_of_birth']

    @staticmethod
    def is_displayed(player):
        return player.accepted == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.region_of_birth >2:
            player.accepted = 1
        else:
            player.accepted = 0

class EnglandLive(Page):
    form_model = 'player'
    form_fields = ['currently_live_in_england']

    @staticmethod
    def is_displayed(player):
        return player.accepted == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.currently_live_in_england ==1:
            player.accepted = 1
        else:
            player.accepted = 0

class Domicile(Page):
    form_model = 'player'
    form_fields = ['region_of_domicile']

    @staticmethod
    def is_displayed(player):
        return player.accepted == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.region_of_birth == 3 or player.region_of_birth == 6 or player.region_of_birth ==7 :
            if player.region_of_domicile == 3 or player.region_of_domicile == 6 or player.region_of_domicile == 7:
                player.southern = 1

        if player.region_of_birth == 4 or player.region_of_birth == 5 or player.region_of_birth == 8 :
            if player.region_of_domicile == 4 or player.region_of_domicile == 5 or player.region_of_domicile == 8:
                player.northern = 1

        if player.southern + player.northern > 0:
            player.accepted = 1
        else:
            player.accepted = 0

class Identity(Page):
    form_model = 'player'
    form_fields = ['regional_identity']

    @staticmethod
    def is_displayed(player):
        return player.accepted == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.southern == 1 and player.regional_identity == 3:
            player.accepted = 1
        elif player.northern == 1 and player.regional_identity == 2:
            player.accepted = 1
        else:
            player.accepted = 0

class Other(Page):
    form_model = 'player'
    form_fields = ['age', 'education']

    @staticmethod
    def is_displayed(player):
        return player.accepted == 1

class Unsuccessful(Page):

    @staticmethod
    def is_displayed(player):
        return player.accepted == 0
class Accepted(Page):

    @staticmethod
    def is_displayed(player):
        return player.accepted == 1

    @staticmethod
    def before_next_page(player, timeout_happened):

        participant = player.participant

        if player.southern == 1:
            participant.group = 0
        if player.northern == 1:
            participant.group = 1

        participant.ingroup = random.choice([0, 1])


page_sequence = [Intro, English, Birth, EnglandLive, Domicile, Identity, Other, Unsuccessful, Accepted]