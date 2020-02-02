from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlsplit


class SEOSpider(CrawlSpider):
	name = 'seospider'
	allowed_domains = ['example.com']
	start_urls = ['https://example.com']

	rules = (
		Rule(LinkExtractor(), callback='parse_item'),
	)

	def parse_item(self, response):
		return {
			'url': response.url,
			'path': urlsplit(response.url).path,
			'content': response.headers['Content-Type'],
			'status_code': response.status,
			'title': response.xpath('//title/text()').get(),
			'meta_description': response.xpath('//meta[@name="description"]/@content').get(),
			'multiple_h1': len(response.xpath('//h1').getall()),
			'h1_1': response.xpath('//h1//text()').get(),
			'multiple_canonical': len(response.xpath('//link[@rel="canonical"]/@href').getall()),
			'canonical_link_1': response.xpath('//link[@rel="canonical"]/@href').get(),
		}
