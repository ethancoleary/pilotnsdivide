from otree.api import *


doc = """
Dictator game
"""


class C(BaseConstants):
    NAME_IN_URL = 'recipient'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    CORRECT_ANSWERS = [4,1,3,4]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    dictator = models.IntegerField(
        choices = [
            [0, '0'],
            [1, '1'],
            [2, '2'],
            [3, '3'],
            [4, '4'],
            [5,'5']
        ]
    )
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
            [1, '£0.00'],
            [2, '£2.00'],
            [3, '£4.00'],
            [4, '£6.00'],
            [5, '£8.00']
        ]
    )

    # Question 4: And your partner?
    check4 = models.IntegerField(
        choices=[
            [1, '£0.00'],
            [2, '£2.00'],
            [3, '£4.00'],
            [4, '£6.00'],
            [5, '£8.00']
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

    @staticmethod
    def error_message(self, values):
        if values['check1'] != C.CORRECT_ANSWERS[0]:
            return ('Your answer to question 1 is wrong.')

        elif values['check2'] != C.CORRECT_ANSWERS[1]:
            return ('Your answer to question 2 is wrong.')

        elif values['check3'] != C.CORRECT_ANSWERS[2]:
            return ('Your answer to question 3(i) is wrong.')

        elif values['check4'] != C.CORRECT_ANSWERS[3]:
            return ('Your answer to question 3(ii) is wrong.')




class Dictator(Page):
    form_model = 'player'
    form_fields = ['dictator']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.dictator = player.dictator



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
                AttentionChecks,
                Dictator,
                 Out]
