import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from pesmater.items import PesmaterItem
from urllib.parse import urljoin


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
            # item = PesmaterItem()
            # item['name'] = question.xpath(
            #     'td[@class="headcol pes-2021"]/a[@class="namelink"]/text()').extract_first()
            # item['age'] = question.xpath(
            #     'td[contains(@class, "squad-table-age")]/text()').extract_first()
            # item['pos'] = question.xpath(
            #     'td/span[contains(@class, "squad-table-pos")]/text()').extract_first()
            url = question.xpath('td[@class="headcol pes-2021"]/a[@class="namelink"]/@href').extract_first()
            yield scrapy.Request(url=urljoin(response.url, url), callback=self.parse_detail)
            # yield item

        if self.page <= 50:
            self.page += 1
            url = 'https://www.pesmaster.com/pes-2021/search/search.php?myclub=yes&sort=ovr&sort_order=desc&page=' + str(
                self.page)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        detail = response.xpath('//*')

        item = PesmaterItem()
        item['name'] = detail.xpath('figure/div[@class="player-card-name"]/text()').extract_first()
        item['ovr'] = detail.xpath('figure/div[@class="player-card-ovr"]/text()').extract_first()
        item['pos'] = detail.xpath('figure/div[@class="player-card-position"]/abbr/text()').extract_first()
        item['img_card'] = detail.xpath('figure/@data-bg').extract_first()
        item['desc'] = detail.xpath('div[@class="top-info"]/p/text()').get()
        #
        player_details = detail.xpath('table[@class="player-info"]/tbody/tr')
        item['fullName'] = player_details[0].xpath('td/text()').extract()[1]
        item['nationality'] = player_details[1].xpath('td/text()').extract()[1]
        item['market_value'] = player_details[2].xpath('td/text()').extract()[1]
        item['team'] = player_details[3].xpath('td/text()').extract()[1]
        item['contractDur'] = player_details[4].xpath('td/text()').extract()[1]
        item['strongerFoot'] = player_details[7].xpath('td/text()').extract()[1]
        item['height'] = player_details[8].xpath('td/text()').extract()[1]
        item['weight'] = player_details[9].xpath('td/text()').extract()[1]
        item['type'] = player_details[10].xpath('td/a/text()').get()

        ability = detail.xpath('div[@class="flex flex-wrap stats-block-container"]/div[@class="stats-block"]')

        item['attacking_total'] = ability[0].xpath('h4/span/text()').get()
        attacking_sub = ability[0].xpath('table/tbody/tr')
        item['offensive_awareness'] = attacking_sub[0].xpath('td/span/text()').get()
        item['finishing'] = attacking_sub[1].xpath('td/span/text()').get()
        item['kicking_power'] = attacking_sub[2].xpath('td/span/text()').get()
        item['weak_foot_usage'] = attacking_sub[3].xpath('td/span/text()').get()
        item['Weak_foot_acc'] = attacking_sub[4].xpath('td/span/text()').get()

        item['dribbling_total'] = ability[1].xpath('h4/span/text()').get()
        dribbling_sub = ability[1].xpath('table/tbody/tr')
        item['ball_control'] = dribbling_sub[0].xpath('td/span/text()').get()
        item['dribbling'] = dribbling_sub[1].xpath('td/span/text()').get()
        item['tight_possession'] = dribbling_sub[2].xpath('td/span/text()').get()
        item['balance'] = dribbling_sub[3].xpath('td/span/text()').get()

        item['defending_total'] = ability[2].xpath('h4/span/text()').get()
        defending_sub = ability[2].xpath('table/tbody/tr')
        item['heading'] = defending_sub[0].xpath('td/span/text()').get()
        item['jump'] = defending_sub[1].xpath('td/span/text()').get()
        item['defensive_awareness'] = defending_sub[2].xpath('td/span/text()').get()
        item['ball_winning'] = defending_sub[3].xpath('td/span/text()').get()
        item['aggression'] = defending_sub[4].xpath('td/span/text()').get()

        item['passing_total'] = ability[3].xpath('h4/span/text()').get()
        passing_sub = ability[3].xpath('table/tbody/tr')
        item['low_pass'] = passing_sub[0].xpath('td/span/text()').get()
        item['lofted_pass'] = passing_sub[0].xpath('td/span/text()').get()
        item['place'] = passing_sub[0].xpath('td/span/text()').get()
        item['kicking'] = passing_sub[0].xpath('td/span/text()').get()
        item['curl'] = passing_sub[0].xpath('td/span/text()').get()

        item['physicality_total'] = ability[4].xpath('h4/span/text()').get()
        physicality_sub = ability[4].xpath('table/tbody/tr')
        item['speed_acceleration'] = physicality_sub[0].xpath('td/span/text()').get()
        item['physical_contact'] = physicality_sub[0].xpath('td/span/text()').get()
        item['stamina'] = physicality_sub[0].xpath('td/span/text()').get()
        item['form'] = physicality_sub[0].xpath('td/span/text()').get()
        item['injury'] = physicality_sub[0].xpath('td/span/text()').get()
        item['resistance'] = physicality_sub[0].xpath('td/span/text()').get()

        item['goal_keeping_total'] = ability[5].xpath('h4/span/text()').get()
        goal_keeping_sub = ability[5].xpath('table/tbody/tr')
        item['gK_awareness'] = goal_keeping_sub[0].xpath('td/span/text()').get()
        item['gk_catching'] = goal_keeping_sub[0].xpath('td/span/text()').get()
        item['gk_clearing'] = goal_keeping_sub[0].xpath('td/span/text()').get()
        item['gk_reflexes'] = goal_keeping_sub[0].xpath('td/span/text()').get()
        item['gk_reach'] = goal_keeping_sub[0].xpath('td/span/text()').get()

        yield item
