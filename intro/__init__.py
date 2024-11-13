import random

from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'workshop_overview_app'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    MIN_NORTHERN = 10
    MIN_SOUTHERN = 10
    MAX_PLAYERS = 30


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent = models.IntegerField(initial=0)
    age = models.IntegerField(
        choices=[
            [1, 'Younger than 20 years'],
            [2, '20-39 years'],
            [3, '40-59 years'],
            [4, '60 years and over']
        ],
        widget=widgets.RadioSelect
    )
    education = models.IntegerField(
        choices=[
            [1, 'GCSEs/O-Levels or equivalent'],
            [2, 'A-Levels or equivalent'],
            [3, 'Undergraduate degree or equivalent'],
            [4, 'Postgraduate degree or equivalent'],
            [5, 'PhD']
        ],
        widget=widgets.RadioSelect
    )
    accepted = models.IntegerField(initial=0)
    english_by_birth = models.IntegerField(
        choices=[
            [1, 'Yes'],
            [2, 'No'],
        ],
        widget=widgets.RadioSelect
    )
    region_of_birth = models.IntegerField(
        choices=[
            [1, 'East of England'],
            [2, 'East Midlands'],
            [3, 'London'],
            [4, 'North East'],
            [5, 'North West'],
            [6, 'South East'],
            [7, 'South West'],
            [8, 'West Midlands'],
            [9, 'Yorkshire and the Humber'],
        ],
        widget=widgets.RadioSelect
    )
    currently_live_in_england = models.IntegerField(
        choices=[
            [1, 'Yes'],
            [2, 'No'],
        ],
        widget=widgets.RadioSelect
    )
    gender = models.IntegerField(
        choices=[
            [1, 'Female'],
            [2, 'Male'],
            [3, 'Other'],
            [4, 'Prefer not to say']
        ],
        widget=widgets.RadioSelect
    )
    region_of_domicile = models.IntegerField(
        choices=[
            [1, 'East of England'],
            [2, 'East Midlands'],
            [3, 'London'],
            [4, 'North East'],
            [5, 'North West'],
            [6, 'South East'],
            [7, 'South West'],
            [8, 'West Midlands'],
            [9, 'Yorkshire and the Humber'],
        ],
        widget=widgets.RadioSelect
    )
    regional_identity = models.IntegerField(
        choices=[
            [1, 'Midlander'],
            [2, 'Northerner'],
            [3, 'Southerner'],
            [4, 'None of the above']
        ],
        widget=widgets.RadioSelect
    )
    northern = models.IntegerField(initial=0)  # Initialize as 0
    southern = models.IntegerField(initial=0)
    northerngeog = models.IntegerField(initial=0)  # Initialize as 0
    southerngeog = models.IntegerField(initial=0)

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
        if player.region_of_birth == 1 or player.region_of_birth == 3 or player.region_of_birth == 6 or player.region_of_birth ==7 :
            if player.region_of_domicile == 1 or player.region_of_domicile == 3 or player.region_of_domicile == 6 or player.region_of_domicile == 7:
                player.southerngeog = 1

        elif player.region_of_birth == 4 or player.region_of_birth == 5 or player.region_of_birth == 9 :
            if player.region_of_domicile == 4 or player.region_of_domicile == 5 or player.region_of_domicile == 9:
                player.northerngeog = 1



class Identity(Page):
    form_model = 'player'
    form_fields = ['regional_identity']

    @staticmethod
    def is_displayed(player):
        return player.accepted == 1

    @staticmethod
    def before_next_page(player, timeout_happened):

        if player.southerngeog == 1 and player.regional_identity == 3:
            player.southern = 1
        elif player.northerngeog == 1 and player.regional_identity == 2:
            player.northern = 1
        else:
            player.northern = 0
            player.southern = 0
        all_players = player.subsession.get_players()

        # Count already admitted participants
        admitted_northern = len([p for p in all_players if p.northern == 1 and p.accepted == 1])
        admitted_southern = len([p for p in all_players if p.southern == 1 and p.accepted == 1])
        total_admitted = len([p for p in all_players if p.accepted == 1])

        remaining_spaces = C.MAX_PLAYERS - total_admitted
        remaining_northern_needed = max(0, C.MIN_NORTHERN - admitted_northern)
        remaining_southern_needed = max(0, C.MIN_SOUTHERN - admitted_southern)

        print(f"Admitted Northern: {admitted_northern}")
        print(f"Admitted Southern: {admitted_southern}")
        print(f"Remaining spaces: {remaining_spaces}")
        print(f"Remaining Northern needed: {remaining_northern_needed}")
        print(f"Remaining Southern needed: {remaining_southern_needed}")

        # Check if there is room for this player, given the constraints
        if player.northern == 1:
            if admitted_northern <= C.MIN_NORTHERN and total_admitted <= C.MAX_PLAYERS:
                player.accepted = 1
            elif remaining_spaces >= (remaining_northern_needed + remaining_southern_needed) and admitted_northern > C.MIN_NORTHERN:
                player.accepted = 1
            else:
                player.accepted = 0
        elif player.southern == 1:
            if admitted_southern <= C.MIN_SOUTHERN and total_admitted <= C.MAX_PLAYERS:
                player.accepted = 1
            elif remaining_spaces >= (remaining_northern_needed + remaining_southern_needed) and admitted_southern > C.MIN_SOUTHERN:
                player.accepted = 1
            else:
                player.accepted = 0
        else:  # This player is neither Northern nor Southern
            if remaining_spaces >= (remaining_northern_needed + remaining_southern_needed):
                player.accepted = 1
            else:
                player.accepted = 0

class Other(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education']

    @staticmethod
    def is_displayed(player):
        return player.accepted == 1

    @staticmethod
    def before_next_page(player, timeout_happened):

        participant = player.participant

        if player.southern == 1:
            participant.northern = 0
        if player.northern == 1:
            participant.northern = 1


class Unsuccessful(Page):

    @staticmethod
    def is_displayed(player):
        return player.accepted == 0

    @staticmethod
    def vars_for_template(player): ## Need a code here that's different to the one they use when they finish.
        code = player.session.config['completion_code']
        link = f"https://app.prolific.co/submissions/complete?cc={code}"

        return dict(
            link=link,
        )

class Accepted(Page):

    @staticmethod
    def is_displayed(player):
        return player.accepted == 1

    def before_next_page(player, timeout_happened):
        player.participant.tgfirst = random.randint(0,1)





class Outro(Page):

    @staticmethod
    def is_displayed(player):
        return player.accepted == 1



    @staticmethod
    def app_after_this_page(player, upcoming_apps):

        if player.participant.tgfirst == 1:
            return "tg"
        if player.participant.tgfirst == 0:
            return "dg"



page_sequence = [
    Intro,
    English,
    Birth,
    EnglandLive,
    Domicile,
    Identity,
    Other,
    Unsuccessful,
    Accepted,
    Outro
]
