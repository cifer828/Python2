import scrapy

class StackOverflowSpider(scrapy.Spider):
    name = 'csdn'
    start_urls = ['http://ask.csdn.net/?sort_by=answers_count']

    def parse(self, response):
        for href in response.css('.questions_detail_con>dl>dt>a::attr(href)'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_question)

    def parse_question(self, response):
        yield {
            'title': response.css('.questions_detail_con dt::text').extract()[0],
            'link': response.url,
        }