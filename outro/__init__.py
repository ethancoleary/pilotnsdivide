import random

from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'outro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    choices = [
        [1, '1'],
        [2, '2'],
        [3, '3'],
        [4, '4'],
        [5, '5'],
        [6, '6'],
        [7, '7']
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    feedback = models.LongStringField(blank=True)

# PAGES

class Feedback(Page):
    form_model = 'player'
    form_fields = ['feedback']

    @staticmethod
    def vars_for_template(player):

        participant = player.participant
        participant.paymentstage = random.randint(1,2)

        if participant.paymentstage == 1 :
            if participant.tgfirst == 1 :
                earnings1 = (3-participant.return1)*2
                earnings2 = (6-participant.return2)*2
                earnings3 = (9 - participant.return3) * 2

                return{
                    'earnings1': earnings1,
                    'earnings2': earnings2,
                    'earnings3': earnings3
                }
            if participant.tgfirst == 0:
                earnings = (5-participant.dictator)*2

                return {
                    'earnings': earnings
                }

        if participant.paymentstage == 2:

            if participant.tgfirst == 0:
                earnings1 = (3 - participant.return1) * 2
                earnings2 = (6 - participant.return2) * 2
                earnings3 = (9 - participant.return3) * 2

                return {
                    'earnings1': earnings1,
                    'earnings2': earnings2,
                    'earnings3': earnings3
                }
            if participant.tgfirst == 1:
                earnings = (5 - participant.dictator) * 2

                return {
                    'earnings': earnings
                }


class Redirect(Page):
    @staticmethod
    def vars_for_template(player):
        code = player.session.config['completion_code']
        link = f"https://app.prolific.co/submissions/complete?cc={code}"

        return dict(
            link=link,
        )


page_sequence = [
    Feedback,
    Redirect
]
