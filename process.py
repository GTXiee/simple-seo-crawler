from basic_seo_crawler.basic_seo_crawler.spiders.seo_spider import SEOSpider
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from multiprocessing import Queue, Process
from urllib import parse
from pathlib import Path
from datetime import datetime


def process_crawl(start_url, output_location):
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    output_uri = get_output_uri(start_url, output_location)

    run_crawler_process(start_url, output_uri)


def get_output_uri(start_url, output_location):
    """
    Takes the start_url and user picked output_location to create a output location
    """
    output_location = Path(output_location)
    datetime_format = '%d%m%Y_%H%M%S'
    protocol = parse.urlparse(start_url).scheme
    domain = parse.urlparse(start_url).netloc
    domain = domain.replace('.', '_')
    datetime_stamp = datetime.strftime(datetime.now(), datetime_format)
    filename = '{0}_{1}__{2}.csv'.format(protocol, domain, datetime_stamp)
    output_path = output_location / filename

    return output_path.as_uri()


def validate_start_url(start_url):
    """
    Checks the given start_url includes the scheme/protocol i.e. http
    """
    return parse.urlparse(start_url).scheme != ''


def run_crawler_process(start_url, output_uri):
    """
    Creates reactor and runs the crawler
    """
    domain = parse.urlparse(start_url).netloc
    runner = CrawlerRunner(settings={
        'FEED_FORMAT': 'csv',
        'FEED_URI': output_uri
    })

    d = runner.crawl(SEOSpider,
                 start_urls=[start_url],
                 allowed_domains=[domain])
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
