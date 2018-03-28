import random

from errbot import botcmd
from errbot import BotPlugin
from errcron import CrontabMixin


FOOD_TIME_SENTENCES = [
    'Do you hear this howling? :will_mura:',
    'What are you doing guys? It\'s time to eat.',
    'Still working? Stop and go eating, I\'m starving.'
]

RESTAURANT_LIST = [
    'Atti, go to eat a delicious Bulgogi.',
    'Five Guys, I know there are some haters in the team but please do the peace.',
    'Freshii, it\'s good for your health.',
    'Frites Alors, but are you sure you want to catch a cancer?',
    'Jerry Ferrer!',
    'La Belle et la Boeuf, eat beef and save a chicken.',
    'La Brigade, mangia una buona pizza',
    'Il Focolaio, mangia una buona pizza'
    'Soup Bol!',
    'Sushi Nippon'
]


class Food(CrontabMixin, BotPlugin):
    CRONTAB = [
        '30 11 * * * .food_time_call @mix-squad'
    ]

    def food_time_call(self):
        return random.choice(FOOD_TIME_SENTENCES)

    @botcmd
    def pick(self, msg, args):
        text = 'I suggest ' + random.choice(RESTAURANT_LIST)
        return text
