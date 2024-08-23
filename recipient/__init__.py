from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'recipient'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    CORRECT_ANSWERS = [1, 3, 4,1,3,4]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    guess = models.IntegerField()
    # Question 1: How many tokens will you receive at the beginning of the game?
    check1 = models.IntegerField(
        choices=[
            [1, '0'],
            [2, '2'],
            [3, '5'],
            [4, '10'],
            [5, '20']
        ]
    )

    # Question 2: How many tokens will your partner receive at the beginning of the game?
    check2 = models.IntegerField(
        choices=[
            [1, '0'],
            [2, '2'],
            [3, '5'],
            [4, '10'],
            [5, '20']
        ]
    )

    # Question 3: If your partner sends you 3 tokens, how many will you receive?
    check3 = models.IntegerField(
        choices=[
            [1, '0'],
            [2, '3'],
            [3, '6'],
            [4, '9'],
            [5, '12']
        ]
    )

    # Question 4: What will be your decision in the game?
    check4 = models.IntegerField(
        choices=[
            [1, 'I will not make a decision.'],
            [2, 'I will decide whether to accept the tokens sent by my partner.'],
            [3, 'I will decide how many tokens to return to my partner.']
        ]
    )

    # Question 5: If your partner sends you 3 tokens, how much will your partner earn?
    check5 = models.IntegerField(
        choices=[
            [1, '0'],
            [2, '1'],
            [3, '2'],
            [4, '3'],
            [5, '4']
        ]
    )

    # Question 6: If your partner sends you 3 tokens, how much will you earn?
    check6 = models.IntegerField(
        choices=[
            [1, '0'],
            [2, '3'],
            [3, '5'],
            [4, '9'],
            [5, '12']
        ]
    )


# PAGES
class Intro(Page):
    pass




class StageTwoIntro(Page):


    @staticmethod
    def vars_for_template(player):
        if player.participant.order == 0 :
            round = "2"
        if player.participant.order == 1 :
            round = "1"

        return {
            'round': round
        }


class AttentionCheck1(Page):
    form_model = 'player'
    form_fields = ['check1']

    def error_message(self, values):
        if values['check1'] != C.CORRECT_ANSWERS[0]:
            return 'Incorrect answer to question 1. Recall you do not receive any tokens at the beginning of the game. Please try again.'

class AttentionCheck2(Page):
    form_model = 'player'
    form_fields = ['check2']

    def error_message(self, values):
        if values['check2'] != C.CORRECT_ANSWERS[1]:
            return 'Incorrect answer to question 2. Recall your partner receives 5 tokens at the beginning of the game. Please try again.'

class AttentionCheck3(Page):
    form_model = 'player'
    form_fields = ['check3']

    def error_message(self, values):
        if values['check3'] != C.CORRECT_ANSWERS[2]:
            return 'Incorrect answer to question 3. Recall any amount sent by your partner is tripled. Please try again.'

class AttentionCheck4(Page):
    form_model = 'player'
    form_fields = ['check4']

    def error_message(self, values):
        if values['check4'] != C.CORRECT_ANSWERS[3]:
            return 'Incorrect answer to question 4. Recall you make no decision in this game: the game is over after person A makes a decision. Please try again.'

class AttentionCheck5(Page):
    form_model = 'player'
    form_fields = ['check5', 'check6']

    def error_message(self, values):
        if values['check5'] != C.CORRECT_ANSWERS[4] or values['check6'] != C.CORRECT_ANSWERS[5]:
            return 'At least one of your answers is incorrect. Recall if your partner sends you 3 tokens then they are left with 2 tokens. If they send 3 tokens then you receive triple this. Please try again.'

class Partner(Page):
    form_model = 'player'
    form_fields = ['guess']

    @staticmethod
    def vars_for_template(player):
        if player.participant.group == 1 and player.participant.ingroup == 1:
            partner = "a Northerner"
            you = "also a Northerner"
        elif player.participant.group == 0 and player.participant.ingroup == 0:
            partner = " a Northerner"
            you = "a Southerner"
        elif player.participant.group == 1 and player.participant.ingroup == 0:
            partner = "a Southerner"
            you = "a Northerner"
        elif player.participant.group == 0 and player.participant.ingroup == 1:
            partner = "a Southerner"
            you = "also a Southerner"

        return{
            'partner':partner,
            'you':you
        }

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.participant.order == 1:
            return "trustee"
        if player.participant.order == 0:
            return "outro"



page_sequence = [StageTwoIntro,
                 AttentionCheck1,
                 AttentionCheck2, AttentionCheck3, AttentionCheck4, AttentionCheck5,
                Partner]
