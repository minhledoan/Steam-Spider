# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SteamParserItem(scrapy.Item):
    game_name = scrapy.Field()
    game_category = scrapy.Field()
    game_overall_review_number = scrapy.Field()
    game_release_date = scrapy.Field()
    game_developer = scrapy.Field()
    game_tags = scrapy.Field()
    game_price = scrapy.Field()
    game_platforms = scrapy.Field()
    pass
