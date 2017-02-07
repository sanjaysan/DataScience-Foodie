import scrapy

class FoodieSpider(scrapy.Spider):
	name = "Foodie"
	
	start_urls = [
	"https://www.zomato.com/new-york-city/restaurants?page=1"
	"https://www.zomato.com/san-jose/restaurants?page=1"
	"https://www.zomato.com/austin/restaurants?page=1"
	"https://www.zomato.com/seattle/restaurants?page=1"
	]
	
	for i in range(1,30):
		start_urls.append("https://www.zomato.com/new-york-city/restaurants?page="+str(i))
		start_urls.append("https://www.zomato.com/san-jose/restaurants?page="+str(i))
		start_urls.append("https://www.zomato.com/austin/restaurants?page="+str(i))
	        start_urls.append("https://www.zomato.com/seattle/restaurants?page="+str(i))


	def parse(self,response):
	   
	       name = response.css("div.row a.result-title::text").extract()
	       address = response.css("div.row div.col-m-16::text").extract()
	       price = response.css("div.res-cost span.col-s-11::text").extract()
	       rating = response.css("div.ta-right div.rating-popup::text").extract()
	       num_reviews = response.css("div.ta-right a.result-reviews::text").extract() 
	  
	       for name_val,address_val,price_val,rating_val,num_review_val in zip(name,address,price,rating,num_reviews):
			yield {
		       		'number_of_reviews':str(num_review_val.strip()),
				'ratingValue':str(rating_val.strip()),
				'address':str(address_val.encode('ascii','ignore').strip()), 
	    			'price_range':str(price_val.strip()),
	    			'name':str(name_val.encode('ascii','ignore').strip()),

			      }





