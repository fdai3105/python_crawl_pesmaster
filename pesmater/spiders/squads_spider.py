import json

import scrapy
from scrapy import Spider, Selector
from urllib.parse import urljoin

from pesmater.items import PesmasterSquad, PesmasterNation, PesmasterPlayer


class SquadsSpider(Spider):
    name = 'squads'
    allowed_domains = ["pesmaster.com"]
    start_urls = ['https://www.pesmaster.com/pes-2021/#leagues']

    def parse(self, response, **kwargs):
        selector = Selector(response).xpath('//*')

        squads = selector.xpath('div[@class="team-block-container"]')
        for sel in squads[2].xpath('div[@class="team-block"]'):
            img = sel.xpath('a/div/img/@data-src').get()
            name = sel.xpath('a/div/span/text()').get()
            url = sel.xpath('a/@href').extract_first()
            nation = PesmasterNation()
            nation['name'] = name
            nation['img'] = img
            yield scrapy.Request(url=urljoin(response.url, url), callback=self.parse_team, meta={'nation': nation})

    def parse_team(self, response):
        nation = response.meta['nation']
        selector = response.xpath('//*')

        teams = []
        for sel in selector.xpath('div[@class="team-block-container"]/div[@class="team-block"]'):
            team = PesmasterSquad()
            team['name'] = sel.xpath('a/div/span[@class="team-block-name"]/text()').get()
            url = sel.xpath('a/@href').extract_first()
            teams.append(team)
            yield scrapy.Request(url=urljoin(response.url, url), callback=self.parse_team_detail,
                                 meta={'teams': team, 'nation': nation})

    def parse_team_detail(self, response):
        nation = response.meta['nation']

        selector = response.xpath('//*')

        for sel in selector.xpath('table/tbody/tr'):
            avatar = sel.xpath('td/img/@data-src').get()
            url = sel.xpath('td/a/@href').get()
            # yield player
            yield scrapy.Request(url=urljoin(response.url, url), callback=self.parse_player_detail,
                                 meta={'nation': nation, 'avatar': avatar, 'url': url})

    def parse_player_detail(self, response):
        nation = response.meta['nation']

        detail = response.xpath('//*')
        item = PesmasterPlayer()

        item['name'] = detail.xpath('figure/div[@class="player-card-name"]/text()').extract_first()
        item['ovr'] = detail.xpath('figure/div[@class="player-card-ovr"]/text()').extract_first()
        item['pos'] = detail.xpath('figure/div[@class="player-card-position"]/abbr/text()').extract_first()
        item['img_avatar'] = response.meta['avatar']
        item['img_card'] = detail.xpath('figure/picture/source/@data-srcset').extract_first()
        item['desc'] = detail.xpath('div[@class="top-info"]/p/text()').get()
        item['player_max_level'] = detail.xpath('div[@class="level-slider-container"]/input/@max').get()
        item['url'] = response.meta['url']

        ds = detail.xpath('table[@class="player-info"]/tbody/tr')

        for i, item_detail in enumerate(ds):
            name = str(item_detail.xpath('td/text()').extract()[0]).lower().replace(' ', '_')
            item.fields[name] = scrapy.Field()
            if i == len(ds) - 1:
                if item_detail.xpath('td/a/text()').get():
                    item[name] = item_detail.xpath('td/a/text()').get()
                else:
                    item[name] = str(item_detail.xpath('td/text()').extract()[1]).strip()
            else:
                item[name] = item_detail.xpath('td/text()').extract()[1]

        item['player_stats'] = json.loads(str(detail.xpath('script/text()').re('.*levelStats.*'))[25:][:-3])
        item['nation'] = nation
        yield item
