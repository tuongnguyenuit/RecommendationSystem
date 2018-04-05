import scrapy
from scrapy.spiders import CrawlSpider, Rule
from stack.items import StackItem
from scrapy.linkextractors import LinkExtractor

class StackSpider(CrawlSpider):
    name = 'stack'
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        'http://stackoverflow.com/questions?pagesize=50&sort=newest',
    ]

    # Thêm Rule để Scrapy biết cách tìm link trang kế tiếp và request đến trang đó
    rules = (
        Rule(LinkExtractor(allow=r"questions\?page=[0-5]&sort=newest"), 
            callback="parse_item", follow=True),
    )
    
    # Lấy crawl URl từ trang danh sách câu hỏi và gửi request đến những URL này và callback đến hàm parse_question
    def parse_item(self, response):
        questions = response.xpath('//div[@class="summary"]/h3')

        for question in questions:
            # Lấy URL
            question_location = question.xpath(
                'a[@class="question-hyperlink"]/@href').extract()[0]
            # Lưu danh sách các URL
            full_url = response.urljoin(question_location)
            yield scrapy.Request(full_url, callback=self.parse_question)

    # Với từng URL, trả về các giá trị như title, url, content
    def parse_question(self, response):
        item = StackItem()
        item['title'] = response.css(
            "#question-header h1 a::text").extract()[0]
        item['url'] = response.url
        item['content'] = response.css(
            ".question .post-text").extract()[0]
        yield item


