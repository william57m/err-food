import json
import random

from urllib.request import Request
from urllib.request import urlopen

from errbot import botcmd
from errbot import BotPlugin
from errcron import CrontabMixin


FOOD_TIME_SENTENCES = [
    'Do you hear this howling? :will_mura:'
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

# Yelp Documentation
# https://www.yelp.com/developers/documentation/v3/business_search
DEFAULT_LATITUDE = '45.503215'
DEFAULT_LONGITUDE = '-73.571466'
DEFAULT_RADIUS_METERS = '1000'
DEFAULT_PRICE_RANGE = '1,2'  # 1=$, 2=$$, 3=$$$


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
            'LATITUDE': DEFAULT_LATITUDE,
            'LONGITUDE': DEFAULT_LONGITUDE,
            'RADIUS_METERS': DEFAULT_RADIUS_METERS,
            'PRICE': DEFAULT_PRICE_RANGE
        }

    def food_time_call(self, polled_time, identity):
        return random.choice(FOOD_TIME_SENTENCES)

    #
    # Resto Commands
    #

    @botcmd
    def resto_pick(self, msg, args):
        """ Returns a random restaurant among a predefined list """
        text = 'I suggest ' + random.choice(RESTAURANT_LIST)
        return text

    #
    # Yelp Commands
    #

    @botcmd
    def yelp_pick(self, msg, args):
        """ Returns a random restaurant from Yelp """
        restaurants = self._search_yelp()
        restaurant = random.choice(restaurants)
        return self.format_result_card(msg, restaurant)

    @botcmd
    def yelp_search(self, msg, search_value):
        """ Returns a list of restaurant from yelp """
        restaurants = self._search_yelp(search_value)
        return self.format_results(restaurants)

    #
    # API request
    #

    def _search_yelp(self, term=''):
        # Get params
        api_key = self.config['API_KEY']
        latitude = self.config['LATITUDE']
        longitude = self.config['LONGITUDE']
        price = self.config['PRICE']
        radius_meters = self.config['RADIUS_METERS']
        url = 'https://api.yelp.com/v3/businesses/search?latitude={latitude}&longitude={longitude}&radius={radius_meters}&price={price}&term={term}'.format(
            latitude=latitude, 
            longitude=longitude, 
            radius_meters=radius_meters,
            price=price,
            term=term
        )

        # Request
        q = Request(url)
        q.add_header('Authorization', 'Bearer {api_key}'.format(api_key=api_key))
        response = urlopen(q).read().decode()
        response = json.loads(response)
        restaurants = response['businesses']
        return restaurants

    #
    # Formatting
    #

    def format_result_card(self, msg, restaurant):
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

    def format_results(self, restaurants):
        restaurants_str = [self.format_restaurant(restaurant) for restaurant in restaurants]
        return '\n'.join(restaurants_str)

    def format_restaurant(self, restaurant):
        return '- [{name}]({link}) ({price}) [{meters} meters away]'.format(
            link=restaurant['url'],
            name=restaurant['name'],
            price=restaurant['price'] if 'price' in restaurant else '',
            meters=str(int(restaurant['distance'])) if 'distance' in restaurant else ''
        )
