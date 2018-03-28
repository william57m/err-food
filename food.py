import json
import random

from urllib.request import Request
from urllib.request import urlopen

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
    'Il Focolaio, mangia una buona pizza',
    'Soup Bol!',
    'Sushi Nippon'
]


class Food(CrontabMixin, BotPlugin):
    TIMEZONE = 'America/New_York'
    CRONTAB = [
        '30 11 * * * .food_time_call @mix-squad'
    ]

    def activate(self):
        super().activate()
        self.activate_crontab()

    def get_configuration_template(self):
        return {
            'API_KEY': 'TO_BE_DEFINED',
            'LATITUDE': '45.503215',
            'LONGITUDE': '-73.571466',
            'RADIUS_METERS': '1000'
        }

    def food_time_call(self):
        return random.choice(FOOD_TIME_SENTENCES)

    @botcmd
    def resto(self, msg, args):

        # Documentation
        if not args:
            return self.return_doc()

        # Get state
        if args == 'pick':
            return self.random_list(msg, args)
        elif args == 'yelp':
            return self.random_yelp(msg, args)
        else:
            return self.return_doc()

    def random_list(self, msg, args):
        text = 'I suggest ' + random.choice(RESTAURANT_LIST)
        return text

    def random_yelp(self, msg, args):
        # Get params
        api_key = self.config['API_KEY']
        latitude = self.config['LATITUDE']
        longitude = self.config['LONGITUDE']
        radius_meters = self.config['RADIUS_METERS']
        url = 'https://api.yelp.com/v3/businesses/search?term=food&latitude={latitude}&longitude={longitude}&radius={radius_meters}'.format(
            latitude=latitude, 
            longitude=longitude, 
            radius_meters=radius_meters
        )

        # Request
        q = Request(url)
        q.add_header('Authorization', 'Bearer {api_key}'.format(api_key=api_key))
        response = urlopen(q).read().decode()
        response = json.loads(response)
        restaurants = response['businesses']
        restaurant = random.choice(restaurants)
        return self.format_result(msg, restaurant)

    def format_result(self, msg, restaurant):
        return self.send_card(
            title=restaurant['name'],
            thumbnail=restaurant['image_url'],
            image=restaurant['image_url'],
            link=restaurant['url'],
            in_reply_to=msg,
            fields=(
                ('Address', ', '.join(restaurant['location']['display_address'])),
                ('Distance', '{meters} meters away from the office'.format(meters=str(int(restaurant['distance'])))),
                ('Price', restaurant['price']),
                ('Rating', restaurant['rating'])
            )
        )

    def return_doc(self):
        return "This is not a valid command man, please use 'pick' or 'yelp'"

