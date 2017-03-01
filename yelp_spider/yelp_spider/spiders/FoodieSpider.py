import scrapy

file_indx = 0;


class FoodieSpider(scrapy.Spider):
    name = "Foodie"

    start_urls = [
        "https://www.yelp.com/search?cflt=restaurants&find_loc=New+York%2C+NY&start=1",
        "https://www.yelp.com/search?cflt=restaurants&find_loc=San+Jose%2C+CA&start=1",
        "https://www.yelp.com/search?cflt=restaurants&find_loc=Austin%2C+TX&start=1",
        "https://www.yelp.com/search?cflt=restaurants&find_loc=Seattle%2C+WA&start=1",
    ]

    for i in range(1, 90):
        start_urls.append("https://www.yelp.com/search?cflt=restaurants&find_loc=New+York%2C+NY&start=" + str(i * 10))
        start_urls.append("https://www.yelp.com/search?cflt=restaurants&find_loc=San+Jose%2C+CA&start=" + str(i * 10))
        start_urls.append("https://www.yelp.com/search?cflt=restaurants&find_loc=Austin%2C+TX&start=" + str(i * 10))
        start_urls.append("https://www.yelp.com/search?cflt=restaurants&find_loc=Seattle%2C+WA&start=" + str(i * 10))

    def parse(self, response):

        for href in response.css('h3.search-result-title  a::attr(href)').extract()[1:]:
            yield scrapy.Request(response.urljoin(href), callback=self.parse_author)

    def parse_author(self, response):

        review_list = response.xpath('//p[@itemprop = "description"]//text()')

        global file_indx;

        if (file_indx <= 300):
            for review_text in review_list:
                filename = "review" + str(file_indx)
                target = open(filename, 'w')
                target.write(review_text.extract().encode('ascii', 'ignore'))
                target.close()
                file_indx = file_indx + 1

        address = [response.xpath('//span[@itemprop="streetAddress"]//text()').extract_first(),
                   response.xpath('//span[@itemprop="addressLocality"]//text()').extract_first(),
                   response.xpath('//span[@itemprop="addressRegion"]//text()').extract_first(),
                   response.xpath('//span[@itemprop="postalCode"]//text()').extract_first(),
                   ]

        s = " "

        yield {
            'number_of_reviews': response.xpath('//span[@itemprop="reviewCount"]//text()').extract_first(),
            'ratingValue': response.xpath('//meta[@itemprop="ratingValue"]/@content').extract_first(),
            'address': s.join(address),
            #	'telephone_number':response.xpath('//span[@itemprop="telephone"]//text()').extract_first().strip(),
            'price_range': response.xpath('//meta[@itemprop="priceRange"]/@content').extract_first(),
            'name': response.xpath('//meta[@itemprop="name"]/@content').extract()[1],

        }
