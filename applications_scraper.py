import scrapy, csv, re
from scrapy.crawler import CrawlerProcess
from scrapy.shell import inspect_response

def decode_text(text : str, no_newline : bool = False) -> str:
    text = text.replace("\xa0", " ").replace("\r\n", "\n")
    if no_newline:
        text = text.replace("\n", " ")
    text = re.sub('\s+', ' ', text)
    return text

class WalthamForestApplicationScraper(scrapy.Spider):
    name = 'WalthamForestApplicationScraper'

    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
        'RETRY_TIMES': 10,

        # export as CSV format
        'FEED_FORMAT': 'csv',
        'FEED_URI': "data/applications_database.csv",
        'USER_AGENT' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }

    def start_requests(self):
        
        # read urls file
        with open("data/application_urls.csv", mode="r") as file:
            file_reader = csv.reader(file)
            urls = [ row[0] for row in file_reader ][1:]
        
        for i in range(0, len(urls), 100):
            yield scrapy.Request(url=urls[i], callback=self.application_parse)

    def application_parse(self, response):
        id_ = response.url.split('&')[-1][3:]

        # application_details_element will be used to extract further elements
        application_details_element = response.css("div.widget-body,fuelux")
        application_reference_number = decode_text(application_details_element.xpath("//strong[text()='Application Reference Number:']/../../div[2]/text()").extract_first().strip())
        application_type = decode_text(application_details_element.xpath("//strong[text()='Application Type:']/../../div[2]/text()").extract_first().strip())
        proposal = decode_text(application_details_element.xpath("//strong[text()='Proposal:']/../../div[2]/text()").extract_first().strip())
        applicant = decode_text(application_details_element.xpath("//strong[text()='Applicant:']/../../div[2]/text()").extract_first().strip())
        
        try:
            agent = decode_text(application_details_element.xpath("//strong[text()='Agent:']/../../div[2]/text()").extract_first().strip())
        except:
            agent = ""

        location = decode_text(application_details_element.xpath("//strong[text()='Location:']/../../div[2]/text()").extract_first().strip())
        ward = decode_text(application_details_element.xpath("//strong[text()='Ward:']/../../div[2]/text()").extract_first().strip())
        officer = decode_text(application_details_element.xpath("//strong[text()='Officer:']/../../div[2]/text()").extract_first().strip())
        decision_level = decode_text(application_details_element.xpath("//strong[text()='Decision level:']/../../div[2]/text()").extract_first().strip())
        application_status = decode_text(application_details_element.xpath("//strong[text()='Application Status:']/../../div[2]/text()").extract_first().strip())
        received_date = decode_text(application_details_element.xpath("//strong[text()='Received Date:']/../../div[2]/text()").extract_first().strip())
        valid_date = decode_text(application_details_element.xpath("//strong[text()='Valid Date:']/../../div[2]/text()").extract_first().strip())
        expiry_date = decode_text(application_details_element.xpath("//strong[text()='Expiry date:']/../../div[2]/text()").extract_first().strip())
        extension_of_time = decode_text(application_details_element.xpath("//strong[text()='Extension of time:']/../../div[2]/text()").extract_first().strip())
        extension_of_time_due_date = decode_text(application_details_element.xpath("//strong[text()='Extension of time due date:']/../../div[2]/text()").extract_first().strip())
        planning_performance_agreement = decode_text(application_details_element.xpath("//strong[text()='Planning performance agreement:']/../../div[2]/text()").extract_first().strip())
        planning_performance_agreement_due_date = print(decode_text(application_details_element.xpath("//strong[text()='Planning performance agreement due date:']/../../div[2]/text()").extract_first().strip()))
        proposed_committee_date = print(decode_text(application_details_element.xpath("//strong[text()='Proposed Committee Date:']/../../div[2]/text()").extract_first().strip()))
        actual_committee_date = print(decode_text(application_details_element.xpath("//strong[text()='Actual committee date:']/../../div[2]/text()").extract_first().strip()))
        decision_issued_date = print(decode_text(application_details_element.xpath("//strong[text()='Decision Issued Date:']/../../div[2]/text()").extract_first().strip()))
        decision = print(decode_text(application_details_element.xpath("//strong[text()='Decision:']/../../div[2]/text()").extract_first().strip()))
        appeal_reference = print(decode_text(application_details_element.xpath("//strong[text()='Appeal reference:']/../../div[2]/text()").extract_first().strip()))
        appeal_status = print(decode_text(application_details_element.xpath("//strong[text()='Appeal status:']/../../div[2]/text()").extract_first().strip()))
        appeal_external_decision = print(decode_text(application_details_element.xpath("//strong[text()='Appeal external decision:']/../../div[2]/text()").extract_first().strip()))
        appeal_external_decision_date = print(decode_text(application_details_element.xpath("//strong[text()='Appeal external decision date:']/../../div[2]/text()").extract_first().strip()))
        
        yield {
            "id" : id_,
            "url" : response.url,
            "application_reference_number" : application_reference_number,
            "application_type" : application_type,
            "proposal" : proposal,
            "applicant" : applicant,
            "agent" : agent,
            "location" : location,
            "ward" : ward,
            "officer" : officer,
            "decision_level" : decision_level,
            "application_status" : application_status,
            "received_date" : received_date,
            "valid_date" : valid_date,
            "expiry_date" : expiry_date,
            "extension_of_time" : extension_of_time,
            "extension_of_time_due_date" : extension_of_time_due_date,
            "planning_performance_agreement" : planning_performance_agreement,
            "planning_performance_agreement_due_date" : planning_performance_agreement_due_date,
            "proposed_committee_date" : proposed_committee_date,
            "actual_committee_date" : actual_committee_date,
            "decision_issued_date" : decision_issued_date,
            "decision" : decision,
            "appeal_reference" : appeal_reference,
            "appeal_status" : appeal_status,
            "appeal_external_decision" : appeal_external_decision,
            "appeal_external_decision_date" : appeal_external_decision_date
        }

process = CrawlerProcess()
process.crawl(WalthamForestApplicationScraper)
process.start()
