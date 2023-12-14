import scrapy
from steam_parser.items import SteamParserItem
import datetime


class SteamspiderSpider(scrapy.Spider):
    name = "SteamSpider"
    allowed_domains = ["store.steampowered.com"]
    start_urls = [
        # Fps игры
        'https://store.steampowered.com/search/?term=fps&ignore_preferences=1&page=1&ndl=1',
        'https://store.steampowered.com/search/?term=fps&ignore_preferences=1&page=2&ndl=1',
        # Simulation игры
        'https://store.steampowered.com/search/?ignore_preferences=1&tags=599&page=1&ndl=1',
        'https://store.steampowered.com/search/?ignore_preferences=1&tags=599&page=2&ndl=1',
        # Story Rich игры
        'https://store.steampowered.com/search/?ignore_preferences=1&tags=1742&page=1&ndl=1',
        'https://store.steampowered.com/search/?ignore_preferences=1&tags=1742&page=2&ndl=1',

    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        games = response.css('a[class = "search_result_row ds_collapse_flag "]::attr(href)').extract()
        for link in games:
            if 'agecheck' not in link:
                yield scrapy.Request(link, callback=self.parse_game)

    def parse_game(self, response):
        items = SteamParserItem()
        game_name = response.xpath('//span[@itemprop="name"]/text()').extract()
        game_category = response.xpath('//span[@data-panel]/a/text()').extract()
        game_overall_review_number = response.xpath('//span[@class="responsive_reviewdesc_short"]/text()').extract()
        game_release_date_str = response.xpath('//div[@class="date"]/text()').extract_first()
        game_developer = response.xpath('//div[@id="developers_list"]/a/text()').extract()
        game_tags = response.xpath('//a[@class="app_tag"]/text()').extract()
        game_price = response.xpath('//div[@class="game_purchase_price price"]/text()').extract_first()
        game_platforms = response.css('div').xpath('@data-os')

        if game_name and game_release_date_str:
            date_formats = ['%b %d, %Y', '%d %b, %Y']

            for date_format in date_formats:
                try:
                    game_release_date = datetime.datetime.strptime(game_release_date_str.strip(), date_format)
                    if game_release_date.year > 2000:
                        items['game_name'] = ''.join(game_name).strip().replace('™', '')
                        items['game_category'] = ', '.join(game_category).strip()
                        items['game_overall_review_number'] = ', '.join(
                            x.strip() for x in game_overall_review_number).strip().replace('(', '').replace(')', '')
                        items['game_release_date'] = game_release_date_str.strip()
                        items['game_developer'] = ', '.join(x.strip() for x in game_developer).strip()
                        items['game_tags'] = ', '.join(x.strip() for x in game_tags).strip()
                        items['game_price'] = ''.join(game_price).strip().replace('уб', '')
                        items['game_platforms'] = ' '.join(set(x.get().strip() for x in game_platforms))

                        yield items
                        break  # Выйдите из цикла, если найдена действительная дата
                except ValueError:
                    pass # Продолжает пробовать другие форматы дат, если возникнет ошибка
