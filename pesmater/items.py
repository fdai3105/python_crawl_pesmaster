# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PesmaterItem(scrapy.Item):
    # define the fields for your item here like:

    debug = scrapy.Field()
    name = scrapy.Field()
    fullName = scrapy.Field()
    desc = scrapy.Field()
    nationality = scrapy.Field()
    market_value = scrapy.Field()
    team = scrapy.Field()
    contractDur = scrapy.Field()
    strongerFoot = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    type = scrapy.Field()
    ovr = scrapy.Field()
    age = scrapy.Field()
    pos = scrapy.Field()
    player_style = scrapy.Field()
    img_card = scrapy.Field()

    # attack
    attacking_total = scrapy.Field()
    offensive_awareness = scrapy.Field()
    finishing = scrapy.Field()
    kicking_power = scrapy.Field()
    weak_foot_usage = scrapy.Field()
    Weak_foot_acc = scrapy.Field()

    #
    dribbling_total = scrapy.Field()
    ball_control = scrapy.Field()
    dribbling = scrapy.Field()
    tight_possession = scrapy.Field()
    balance = scrapy.Field()

    #
    defending_total = scrapy.Field()
    heading = scrapy.Field()
    jump = scrapy.Field()
    defensive_awareness = scrapy.Field()
    ball_winning = scrapy.Field()
    aggression = scrapy.Field()

    #
    passing_total = scrapy.Field()
    low_pass = scrapy.Field()
    lofted_pass = scrapy.Field()
    place = scrapy.Field()
    kicking = scrapy.Field()
    curl = scrapy.Field()

    physicality_total = scrapy.Field()
    speed_acceleration = scrapy.Field()
    physical_contact = scrapy.Field()
    stamina = scrapy.Field()
    form = scrapy.Field()
    injury = scrapy.Field()
    resistance = scrapy.Field()

    goal_keeping_total = scrapy.Field()
    gK_awareness = scrapy.Field()
    gk_catching = scrapy.Field()
    gk_clearing = scrapy.Field()
    gk_reflexes = scrapy.Field()
    gk_reach = scrapy.Field()
