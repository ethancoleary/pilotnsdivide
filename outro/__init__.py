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
    profession = models.IntegerField(
        choices = [
            [1, 'Full-time employed'],
            [2, 'Part-time employed'],
            [3, 'Self-employed'],
            [4, 'Student'],
            [5, 'Retired']
        ]
    )
    children = models.IntegerField()
    gentrust = models.IntegerField(
        choices=C.choices,
        widget=widgets.RadioSelectHorizontal,
    )
    neightrust = models.IntegerField(
        choices=C.choices,
        widget=widgets.RadioSelectHorizontal,
    )
    govtrust = models.IntegerField(
        choices=C.choices,
        widget=widgets.RadioSelectHorizontal,
    )
    regidentity = models.IntegerField(
        choices = [
            [1, 'Not at all'],
            [2, 'A little bit, but it did not impact my decision'],
            [3, 'A little bit, and it impacted my decision slightly'],
            [4, 'A lot and my decision was based on this']
        ]
    )
    genderpartner = models.IntegerField(
        choices = [
            [1, 'Male'],
            [2, 'Female'],
            [3, 'Neither/Both']
        ]
    )
    agepartner = models.IntegerField(
        choices=[
            [1, 'Younger than 20 years'],
            [2, '20-39 years'],
            [3, '40-59 years'],
            [4, '60 years and over']
        ],
    )
    educpartner = models.IntegerField(
        choices=[
            [1, 'GCSEs/O-Levels or equivalent'],
            [2, 'A-Levels or equivalent'],
            [3, 'Undergraduate degree or equivalent'],
            [4, 'Postgraduate degree or equivalent'],
            [5, 'PhD']
        ],
    )
    socialcloseness = models.IntegerField(
        choices = [
            [1,'1'],
            [2,'2'],
            [3,'3'],
            [4,'4'],
            [5,'5']
        ]
    )



# PAGES
class Further1(Page):
    form_model = 'player'
    form_fields = ['profession', 'children', 'gentrust', 'neightrust', 'govtrust']

    def vars_for_template(self):
        return {
            'questions': [
                {'statement': 'Most people can be trusted', 'field': 'gentrust'},
                {'statement': 'I can trust my neighbours', 'field': 'neightrust'},
                {'statement': 'I can trust the government', 'field': 'govtrust'}
            ]
        }

class Further2(Page):
    form_model = 'player'
    form_fields = ['regidentity', 'genderpartner', 'agepartner', 'educpartner']

class Socialclose(Page):
    form_model = 'player'
    form_fields = ['socialcloseness']

class Feedback(Page):
    form_model = 'player'
    form_fields = ['feedback']


class Redirect(Page):
    @staticmethod
    def vars_for_template(player):
        code = player.session.config['completion_code']
        link = f"https://app.prolific.co/submissions/complete?cc={code}"

        return dict(
            link=link,
        )


page_sequence = [
    Further1,
                 Socialclose, Further2,
    Feedback,
    Redirect
]
