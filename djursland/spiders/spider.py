import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import DjurslandItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class DjurslandSpider(scrapy.Spider):
	name = 'djursland'
	start_urls = ['https://www.djurslandsbank.dk/raadgivning/nyheder-alle']

	def parse(self, response):
		post_links = response.xpath('//table[@class="align-left"]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//p/time/text()').get()
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//h4[@itemprop="about"]//text()').getall() + response.xpath('//div[@itemprop="articleBody"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=DjurslandItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
