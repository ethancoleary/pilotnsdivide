import random

from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'trustee'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    CORRECT_ANSWERS = [3, 1, 5, 2, 4]


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
            [2, '1'],
            [3, '2'],
            [4, '3'],
            [5, '4']
        ]
    )

    check2 = models.IntegerField(
        choices=[
            [1, '£0.00'],
            [2, '£1.00'],
            [3, '£2.00'],
            [4, '£3.00'],
            [5, '£4.00']
        ]
    )

    # Question 3: If your partner sends you 4 tokens, how many will you receive?
    check3 = models.IntegerField(
        choices=[
            [1, '0'],
            [2, '1'],
            [3, '2'],
            [4, '5'],
            [5, '6']
        ]
    )

    # Question 5: If your partner sends you 4 tokens and you return 4 tokens, how much will your partner earn?
    check4 = models.IntegerField(
        choices=[
            [1, '£0.00'],
            [2, '£2.00'],
            [3, '£4.00'],
            [4, '£6.00'],
            [5, '£8.00']
        ]
    )

    # Question 6: If your partner sends you 4 tokens and you return 4 tokens, how much will you earn?
    check5 = models.IntegerField(
        choices=[
            [1, '£0.00'],
            [2, '£2.00'],
            [3, '£4.00'],
            [4, '£6.00'],
            [5, '£8.00']
        ]
    )

    return1 = models.IntegerField(
        widget = widgets.RadioSelect,
        choices = [
            [0, '0'],
            [1, '1'],
            [2, '2'],
            [3, '3']
        ]
    )
    return2 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[
            [0, '0'],
            [1, '1'],
            [2, '2'],
            [3, '3'],
            [4, '4'],
            [5, '5'],
            [6, '6']
        ]
    )



# PAGES



class StageOneIntro(Page):
    pass

class AttentionChecks(Page):
    form_model = 'player'
    form_fields = ['check1', 'check2', 'check3', 'check4', 'check5']

    def error_message(self, values):
        if values['check1'] != C.CORRECT_ANSWERS[0] or values['check2'] != C.CORRECT_ANSWERS[1] or values['check3'] != \
                C.CORRECT_ANSWERS[2] or values['check4'] != C.CORRECT_ANSWERS[3] or values['check5'] != C.CORRECT_ANSWERS[4]:
            return (
                'At least one of your answers is incorrect. Recall, your partner receives 2 tokens at the start of the stage; you receive nothing.'
                ' Any token amount sent to you is tripled. Please try again.')

class Trustee0(Page):
    @staticmethod
    def vars_for_template(player):
        if player.participant.northern == 1 and player.participant.ingroup == 1:
            partner = "a Northerner"
            you = "also a Northerner"
        elif player.participant.northern == 0 and player.participant.ingroup == 0:
            partner = " a Northerner"
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

        return {
            'partner': partner,
            'you': you
        }
class Trustee1(Page):
    form_model = 'player'
    form_fields = ['return1']

    @staticmethod
    def vars_for_template(player):
        if player.participant.northern == 1 and player.participant.ingroup == 1:
            partner = "a Northerner"
            you = "also a Northerner"
        elif player.participant.northern == 0 and player.participant.ingroup == 0:
            partner = " a Northerner"
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

        return {
            'partner': partner,
            'you': you
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.return1 = player.return1


class Trustee2(Page):
    form_model = 'player'
    form_fields = ['return2']

    @staticmethod
    def vars_for_template(player):
        if player.participant.northern == 1 and player.participant.ingroup == 1:
            partner = "a Northerner"
            you = "also a Northerner"
        elif player.participant.northern == 0 and player.participant.ingroup == 0:
            partner = " a Northerner"
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

        return {
            'partner': partner,
            'you': you
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.return2 = player.return2



class Out(Page):
    @staticmethod
    def vars_for_template(player):
        if player.participant.tgfirst == 1:
            round = "1"
        if player.participant.tgfirst == 0:
            round = "2"

        return {
            'round': round
        }

page_sequence = [StageOneIntro,
                 AttentionChecks,
                 Trustee0, Trustee1, Trustee2,
                 Out]
