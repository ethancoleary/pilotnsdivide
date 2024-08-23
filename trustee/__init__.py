import random

from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'trustee'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    CORRECT_ANSWERS = [3, 1, 5, 3, 3, 4]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    partner = models.LongStringField()
    # Question 1: How many tokens will your partner receive at the beginning of the game?
    check1 = models.IntegerField(
        choices=[
            [1, '0'],
            [2, '2'],
            [3, '5'],
            [4, '10'],
            [5, '20']
        ]
    )

    # Question 2: How many tokens will you receive at the beginning of the game?
    check2 = models.IntegerField(
        choices=[
            [1, '0'],
            [2, '2'],
            [3, '5'],
            [4, '10'],
            [5, '20']
        ]
    )

    # Question 3: If your partner sends you 4 tokens, how many will you receive?
    check3 = models.IntegerField(
        choices=[
            [1, '0'],
            [2, '2'],
            [3, '4'],
            [4, '10'],
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

    # Question 5: If your partner sends you 4 tokens and you return 4 tokens, how much will your partner earn?
    check5 = models.IntegerField(
        choices=[
            [1, '2'],
            [2, '4'],
            [3, '5'],
            [4, '8'],
            [5, '12']
        ]
    )

    # Question 6: If your partner sends you 4 tokens and you return 4 tokens, how much will you earn?
    check6 = models.IntegerField(
        choices=[
            [1, '2'],
            [2, '4'],
            [3, '5'],
            [4, '8'],
            [5, '12']
        ]
    )

    return1 = models.IntegerField(
        choices = [
            [0, '0'],
            [1, '1'],
            [2, '2'],
            [3, '3']
        ]
    )
    return2 = models.IntegerField()
    return3 = models.IntegerField()
    return4 = models.IntegerField()
    return5 = models.IntegerField()



# PAGES



class StageOneIntro(Page):
    @staticmethod
    def vars_for_template(player):
        if player.participant.order == 0:
            round = "1"
        if player.participant.order == 1:
            round = "2"

        return {
            'round': round
        }


class AttentionCheck1(Page):
    form_model = 'player'
    form_fields = ['check1']

    def error_message(self, values):
        if values['check1'] != C.CORRECT_ANSWERS[0]:
            return 'Incorrect answer. Recall your partner receives 5 tokens. Please try again.'

class AttentionCheck2(Page):
    form_model = 'player'
    form_fields = ['check2']

    def error_message(self, values):
        if values['check2'] != C.CORRECT_ANSWERS[1]:
            return 'Incorrect answer. Recall you receive no tokens at the beginning of the game. Please try again.'

class AttentionCheck3(Page):
    form_model = 'player'
    form_fields = ['check3']

    def error_message(self, values):
        if values['check3'] != C.CORRECT_ANSWERS[2]:
            return 'Incorrect answer. Recall that any token amount sent to you is tripled. Please try again.'

class AttentionCheck4(Page):
    form_model = 'player'
    form_fields = ['check4']

    def error_message(self, values):
        if values['check4'] != C.CORRECT_ANSWERS[3]:
            return 'Incorrect answer. Recall you must decide how many tokens to return to person A. Please try again.'

class AttentionCheck5(Page):
    form_model = 'player'
    form_fields = ['check5', 'check6']

    def error_message(self, values):
        if values['check5'] != C.CORRECT_ANSWERS[4] or values['check6'] != C.CORRECT_ANSWERS[5]:
            return 'At least one of your answers is incorrect. Recall if your partner sends you 4 tokens then they are left with 1 token. If they send 4 tokens then you receive triple this.Please try again.'

class Partner(Page):

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

class Decision1(Page):
    form_model = 'player'
    form_fields = ['return1', 'return2', 'return3', 'return4', 'return5']

    @staticmethod
    def before_next_page(player, timeout_happened):

        participant=player.participant
        participant.return1 = player.return1
        participant.return2 = player.return2
        participant.return3 = player.return3
        participant.return4 = player.return4
        participant.return5 = player.return5

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.participant.order == 1:
            return "outro"
        if player.participant.order == 0:
            return "recipient"



page_sequence = [StageOneIntro,
                 AttentionCheck1,
                AttentionCheck2, AttentionCheck3, AttentionCheck4, AttentionCheck5,
                 Partner,
                   Decision1]

