from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field
import re

base_url = "http://www.bfro.net/GDB/default.asp"

class Sighting(Item):
    url = Field()
    classification = Field()
    report_id = Field()
    description = Field()
    year = Field()
    season = Field()
    month = Field()
    state = Field()
    county = Field()
    location_details = Field()
    nearest_town = Field()
    nearest_road = Field()
    observed = Field()
    also_noticed = Field()
    other_witnesses = Field()
    other_stories = Field()
    time_and_conditions = Field()
    environment = Field()
    follow_up = Field()
    about_investigator = Field()
    
class BigfootSpider(CrawlSpider):

    name = "bfro"
    allowed_domains = ['www.bfro.net']
    start_urls = [base_url]
    rules = [Rule(SgmlLinkExtractor(allow=['/GDB/show_report.asp?id=\d+']), 'parse_sightings')]

    def fix_field_names(self, field_name):
        field_name = re.sub(" ","_", field_name)
        field_name = re.sub(":","", field_name)
        return field_name
    
    def parse_sightings(self, response):
        x = HtmlXPathSelector(response)

        sighting = Sighting()
        
        sighting['url'] = response.url
        sighting['classification'] = x.select("//span[@class='reportclassification']/text()").extract()
        sighting['report_id'] = x.select("//span[@class='reportheader']/text()").extract()
        paragraphs = x.select("//p")
        fields = x.select("//span[@class='field']/text()")
        for i in xrange(0,len(fields)):
            p = paragraphs[i]
            text = " ".join(p.select("//text()").extract())
            field = fields[i].extract().lower()
            sighting[self.fix_field_names(field)] = text
        return sighting
