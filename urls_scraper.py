import scrapy
import json
from scrapy.http import FormRequest
from scrapy.crawler import CrawlerProcess
from scrapy.shell import inspect_response


class WalthamForestUrlsScraper(scrapy.Spider):
    name = 'WalthamForestUrlsScraper'

    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
        'RETRY_TIMES': 10,

        # export as CSV format
        'FEED_FORMAT': 'csv',
        'FEED_URI': "data/application_urls.csv",
    }

    def start_requests(self):
        url = "https://builtenvironment.walthamforest.gov.uk/planning/index.html"
        headers = {
            'cookie': 'PHPSESSID=f43a03e314be4e8919dac18eed150ecc; AWSALB=dWoflelzwwwNGFywIVnRN+NOejo9E6+a8JHUYOgq3xJHHt1v2ynjX09PDi4b3YtCp84mZHaGrzCqxgsRy29CKfq/wQl5IFlx58l5t/7RTpNVfHCyErd+IXxzAHTB; AWSALBCORS=dWoflelzwwwNGFywIVnRN+NOejo9E6+a8JHUYOgq3xJHHt1v2ynjX09PDi4b3YtCp84mZHaGrzCqxgsRy29CKfq/wQl5IFlx58l5t/7RTpNVfHCyErd+IXxzAHTB; AWSALB=QExpg3jrMrdoKqpog/5hEvAWk6VlCOTpRC/6mxy6+ab9MjHgSKm3wxmRIh4gNlY94CtAoXsgG5vrRt5CztNMYI6EwjZ1LKS87lf43EN10MIpCye2WP3AwPluEPD6; AWSALBCORS=QExpg3jrMrdoKqpog/5hEvAWk6VlCOTpRC/6mxy6+ab9MjHgSKm3wxmRIh4gNlY94CtAoXsgG5vrRt5CztNMYI6EwjZ1LKS87lf43EN10MIpCye2WP3AwPluEPD6',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }
        for i in range(1, 342+1):
            payload = {'fa': 'search',
                       'page': str(i),
                       'ajax': 'true',
                       'result_loader': 'true',
                       'submitted': 'true',
                       'valid_date_from': '01-01-2020',
                       'valid_date_to': '01-01-2023'}
            yield FormRequest(method="POST", url=url, callback=self.search_api_parsed, headers=headers, formdata=payload)

    def search_api_parsed(self, response):
        urls = response.css("tr > td > a ::attr(href)").extract()
        for item in urls:
            yield {"URL": response.urljoin(item)}


process = CrawlerProcess()
process.crawl(WalthamForestUrlsScraper)
process.start()
