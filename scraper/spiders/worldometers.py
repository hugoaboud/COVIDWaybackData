import scrapy


class WorldometersSpider(scrapy.Spider):
    name = 'worldometers'
    allowed_domains = ['worldometers.info']
    start_urls = ['https://worldometers.info/coronavirus']
    results = []

    def parse(self, response):
        table = response.css("table#main_table_countries_today")
        rows = table.xpath("tbody//tr")
        for row in rows:
            line = [r.xpath(".//text()").get(default='') for r in row.xpath('td')]
            if ("Brazil" in line):
                entry = str(response.request.meta['wayback_machine_time'])+"\t"
                for e in line:
                    entry += str(e) + "\t"
                entry += "\n"
                with open("output/data.tsv","a") as file:
                    file.write(str(entry))
                print(entry)
        pass
