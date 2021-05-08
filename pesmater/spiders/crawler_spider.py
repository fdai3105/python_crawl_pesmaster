import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from pesmater.items import PesmaterItem
from urllib.parse import urljoin
import json


class CrawlerSpider(Spider):
    name = "crawler"
    allowed_domains = ["pesmaster.com"]
    start_urls = [
        "https://www.pesmaster.com/pes-2021/search/search.php?myclub=yes&sort=ovr&sort_order=desc&page=",
    ]
    page = 0

    def parse(self, response):
        questions = Selector(response).xpath('//tbody/tr')

        for question in questions:
            avatar = question.xpath(
                'td[@class="headcol pes-2021"]/img/@data-src').extract_first()
            url = question.xpath('td[@class="headcol pes-2021"]/a[@class="namelink"]/@href').extract_first()
            yield scrapy.Request(url=urljoin(response.url, url), callback=self.parse_detail, meta={'avatar': avatar})

        # if self.page <= 859: self.page += 1 url =
        # 'https://www.pesmaster.com/pes-2021/search/search.php?myclub=yes&sort=ovr&sort_order=desc&page=' + str(
        # self.page) yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        detail = response.xpath('//*')

        item = PesmaterItem()

        item['name'] = detail.xpath('figure/div[@class="player-card-name"]/text()').extract_first()
        item['ovr'] = detail.xpath('figure/div[@class="player-card-ovr"]/text()').extract_first()
        item['pos'] = detail.xpath('figure/div[@class="player-card-position"]/abbr/text()').extract_first()
        item['img_avatar'] = response.meta['avatar']
        item['img_card'] = detail.xpath('figure/picture/source/@data-srcset').extract_first()
        item['desc'] = detail.xpath('div[@class="top-info"]/p/text()').get()
        item['player_max_level'] = detail.xpath('div[@class="level-slider-container"]/input/@max').get()

        #
        player_details = detail.xpath('table[@class="player-info"]/tbody/tr')
        if len(player_details) == 11:
            item['fullName'] = player_details[0].xpath('td/text()').extract()[1]
            item['nationality'] = player_details[1].xpath('td/text()').extract()[1]
            item['team'] = player_details[2].xpath('td/text()').extract()[1]
            item['strongerFoot'] = player_details[5].xpath('td/text()').extract()[1]
            item['height'] = player_details[6].xpath('td/text()').extract()[1]
            item['weight'] = player_details[7].xpath('td/text()').extract()[1]
            item['type'] = player_details[len(player_details) - 1].xpath('td/a/text()').get()
        elif len(player_details) == 10:
            item['nationality'] = player_details[0].xpath('td/text()').extract()[1]
            item['team'] = player_details[1].xpath('td/text()').extract()[1]
            item['strongerFoot'] = player_details[4].xpath('td/text()').extract()[1]
            item['height'] = player_details[5].xpath('td/text()').extract()[1]
            item['weight'] = player_details[6].xpath('td/text()').extract()[1]
            item['type'] = player_details[len(player_details) - 1].xpath('td/a/text()').get()
        else:
            item['fullName'] = player_details[0].xpath('td/text()').extract()[1]
            item['nationality'] = player_details[1].xpath('td/text()').extract()[1]
            item['market_value'] = player_details[2].xpath('td/text()').extract()[1]
            item['team'] = player_details[3].xpath('td/text()').extract()[1]
            item['contractDur'] = player_details[4].xpath('td/text()').extract()[1]
            item['strongerFoot'] = player_details[7].xpath('td/text()').extract()[1]
            item['height'] = player_details[8].xpath('td/text()').extract()[1]
            item['weight'] = player_details[9].xpath('td/text()').extract()[1]
            item['type'] = player_details[len(player_details) - 1].xpath('td/a/text()').get()

        item['player_stats'] = json.loads(str(detail.xpath('script/text()').re('.*levelStats.*'))[25:][:-3])

        yield item
