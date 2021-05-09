# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PesmasterSquad(scrapy.Item):
    name = scrapy.Field()
    img = scrapy.Field()
    url = scrapy.Field()
    ovr = scrapy.Field()
    defence = scrapy.Field()
    midfield = scrapy.Field()
    attack = scrapy.Field()
    speed = scrapy.Field()
    strength = scrapy.Field()

    players = scrapy.Field()


class PesmasterNation(scrapy.Item):
    name = scrapy.Field()
    img = scrapy.Field()
    teams = scrapy.Field()


class PesmasterPlayer(scrapy.Item):
    debug = scrapy.Field()
    nation = scrapy.Field()
    name = scrapy.Field()
    desc = scrapy.Field()
    ovr = scrapy.Field()
    age = scrapy.Field()
    pos = scrapy.Field()
    player_style = scrapy.Field()
    com_style = scrapy.Field()
    player_skills = scrapy.Field()
    img_avatar = scrapy.Field()
    img_card = scrapy.Field()
    player_max_level = scrapy.Field()
    url = scrapy.Field()
    player_stats = scrapy.Field()
