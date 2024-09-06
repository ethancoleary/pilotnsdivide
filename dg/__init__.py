from otree.api import *


doc = """
Dictator game
"""


class C(BaseConstants):
    NAME_IN_URL = 'recipient'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    CORRECT_ANSWERS = [3,1,2,3]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    dictator = models.IntegerField()
    # Question 1: How many tokens will you receive at the beginning of the game?
    check1 = models.IntegerField(
        choices=[
            [1, '0'],
            [2, '2'],
            [3, '4'],
            [4, '5'],
            [5, '10']
        ]
    )

    # Question 2: How many tokens will your partner receive at the beginning of the game?
    check2 = models.IntegerField(
        choices=[
            [1, '0'],
            [2, '2'],
            [3, '4'],
            [4, '5'],
            [5, '10']
        ]
    )

    # Question 3: If you send 3 tokens what will be your payment for this stage?
    check3 = models.IntegerField(
        choices=[
            [1, '0'],
            [2, '1'],
            [3, '2'],
            [4, '3'],
            [5, '4']
        ]
    )

    # Question 4: And your partner?
    check4 = models.IntegerField(
        choices=[
            [1, '1'],
            [2, '2'],
            [3, '3'],
            [4, '6'],
            [5, '9']
        ]
    )





class StageTwoIntro(Page):


    @staticmethod
    def vars_for_template(player):
        if player.participant.tgfirst == 1 :
            round = "2"
        if player.participant.tgfirst == 0 :
            round = "1"

        return {
            'round': round
        }


class AttentionChecks(Page):
    form_model = 'player'
    form_fields = ['check1', 'check2', 'check3', 'check4']

    def error_message(self, values):
        if values['check1'] != C.CORRECT_ANSWERS[0] or values['check2'] != C.CORRECT_ANSWERS[1] or values['check3'] != C.CORRECT_ANSWERS[2] or values['check4'] != C.CORRECT_ANSWERS[3]:
            return ('At least one of your answers is incorrect. Recall, you receive 5 tokens at the start of the stage; your partner receives nothing.'
                    ' If you send 3 tokens then you keep the remaining 2 and your partner is paid the number of tokens you send. Please try again.')


class Dictator(Page):
    form_model = 'player'
    form_fields = ['dictator']

    @staticmethod
    def vars_for_template(player):
        if player.participant.northern == 1 and player.participant.ingroup == 1:
            partner = "a Northerner"
            you = "also a Northerner"
        elif player.participant.northern == 0 and player.participant.ingroup == 0:
            partner = "a Northerner"
            you = "a Southerner"
        elif player.participant.northern == 1 and player.participant.ingroup == 0:
            partner = "a Southerner"
            you = "a Northerner"
        elif player.participant.northern == 0 and player.participant.ingroup == 1:
            partner = "a Southerner"
            you = "also a Southerner"
        else:
            partner = ""
            you = ""

        return{
            'partner':partner,
            'you':you
        }

class Out(Page):

    @staticmethod
    def vars_for_template(player):
        if player.participant.tgfirst == 1:
            round = "2"
        if player.participant.tgfirst == 0:
            round = "1"

        return {
            'round': round
        }
    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.participant.tgfirst == 0:
            return "tg2"
        if player.participant.tgfirst == 1:
            return "outro"



page_sequence = [StageTwoIntro,
                # AttentionChecks,
                Dictator,
                 Out]
