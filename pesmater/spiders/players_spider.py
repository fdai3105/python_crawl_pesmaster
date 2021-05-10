import json

import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from pesmater.items import PesPlayer, PesLeague, PesTeam
from urllib.parse import urljoin


class PlayersSpider(Spider):
    name = "players"
    allowed_domains = ["pesmaster.com"]
    start_urls = [
        "https://www.pesmaster.com/pes-2021/search/search.php?type=default&sort=ovr&sort_order=desc&page=",
    ]
    page = 0
    end_page = 635

    def parse(self, response):

        questions = Selector(response).xpath('//tbody/tr')

        for question in questions:
            avatar = question.xpath(
                'td[@class="headcol pes-2021"]/img/@data-src').extract_first()
            url = question.xpath('td[@class="headcol pes-2021"]/a[@class="namelink"]/@href').extract_first()
            yield scrapy.Request(url=urljoin(response.url, url), callback=self.parse_detail,
                                 meta={'avatar': avatar, 'url': urljoin(response.url, url)})

        if self.page <= 100:
            self.page += 1
            url = 'https://www.pesmaster.com/pes-2021/search/search.php?type=default&sort=ovr&sort_order=desc&page=' \
                  + str(self.page)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        detail = response.xpath('//*')

        item = PesPlayer()
        league = PesLeague()
        team = PesTeam()

        select = detail.xpath('div/a[@class="namelink"]')
        img_url = 'https://www.pesmaster.com/pes-2021/graphics/teamlogos/e_'
        if select:
            if len(select) > 1:
                team['team_id'] = str(select[0].xpath('@href').get()).split('/')[4]
                team['name'] = select[0].xpath('text()').get()
                team['img'] = img_url + str(select[0].xpath('@href').get()).split('/')[4] + '.png'
                league['league_id'] = str(select[1].xpath('@href').get()).split('/')[4]
                league['name'] = select[1].xpath('text()').get()
                league['img'] = img_url + str(select[1].xpath('@href').get()).split('/')[4].zfill(6) + '.png'
            else:
                team['team_id'] = str(select[0].xpath('@href').get()).split('/')[4]
                team['name'] = select[0].xpath('text()').get()
                team['img'] = img_url + str(select[0].xpath('@href').get()).split('/')[4].zfill(6) + '.png'

        item['league'] = league
        item['team'] = team
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
                item[name] = item_detail.xpath('td/a/text()').get()
            else:
                if name != 'team':
                    if name != 'league':
                        item[name] = item_detail.xpath('td/text()').extract()[1]

        item['player_stats'] = json.loads(str(detail.xpath('script/text()').re('.*levelStats.*'))[25:][:-3])

        yield item
