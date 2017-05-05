import numpy as np
import pandas as pd

## Python script used to process merged data [ processing - split address fields ]

match_data = pd.read_csv('./match_data.csv')

columns = ['number_of_reviews', 'price_range', 'ratingValue', 'name', 'street_city','state','zipcode']
num_matches = len(match_data)

# Index range for data frame
indx_range = range(num_matches)

# New data frame to hold address in separate fields
match_processed = pd.DataFrame(index=indx_range, columns=columns)


match_table_id = 0

for index,row in match_data.iterrows():

#Copying all non-address fields from original match_data
	match_processed.iloc[match_table_id]['number_of_reviews'] = match_data.iloc[index]['number_of_reviews']
	match_processed.iloc[match_table_id]['price_range']       = match_data.iloc[index]['price_range']
	match_processed.iloc[match_table_id]['ratingValue']       = str( match_data.iloc[index]['ratingValue'] )
	match_processed.iloc[match_table_id]['name']	          = match_data.iloc[index]['name']

#Processing address string and splitting into fields 

	address_list = match_data.iloc[index]['address'].split(" ")

	street_city = ""
	
	itr_limit = len( address_list ) -2

	for i in range(itr_limit):
		street_city +=address_list[ i ]
		if  i < itr_limit -1 :
			street_city +=" "

	zipcode = address_list[-1]
	state   = address_list[-2]

	match_processed.iloc[match_table_id]['street_city']  = street_city
	match_processed.iloc[match_table_id]['state']	     = state
	match_processed.iloc[match_table_id]['zipcode']	     = zipcode

	match_table_id+=1



match_processed.to_csv('./match_processed.csv')
 


	 
