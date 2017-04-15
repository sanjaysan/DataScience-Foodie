import sys
import pandas as pd
import os,sys
import math


#### Reading the necessary data ###

## load candidate set data

C = pd.read_pickle('./candidate_set.pkl')

## load candidate set predictions ( obtained after applying the trained classifier to candidate set )

Cpred = pd.read_pickle('./candidate_set_predictions.pkl')


### Creating the matched data frame ###

## Columns for the new data 
columns = ['number_of_reviews','price_range','ratingValue','name','address']

## Indx range for data frame

num_matches = len( Cpred[ ( Cpred['predicted'] == 1 ) ] )

indx_range = range(num_matches)

##New data frame
match = pd.DataFrame(index = indx_range, columns=columns)



### Merging data ### 

## Iterate over tuples in Cpred to find predicted matches

match_table_id = 0

for index, row in Cpred.iterrows():
	
	if int(row[ 'predicted' ]) == 1 :
		
		id = int( row[ '_id' ] )

## Print matches
##		print C.iloc[ id ] 

## Populate match data frame
## TODO Add merging rules- ltable is yelp, rtable is zomato

		match.iloc[ match_table_id ] [ 'number_of_reviews' ] = C.iloc[ id ] [ 'ltable_number_of_reviews']
		
		match.iloc[ match_table_id ] [ 'price_range' ] 	     = C.iloc[ id ] [ 'ltable_price_range']
		
		match.iloc[ match_table_id ] [ 'ratingValue' ] 	     = C.iloc[ id ] [ 'ltable_ratingValue']

		match.iloc[ match_table_id ] [ 'address' ] 	     = C.iloc[ id ] [ 'ltable_address']

		match.iloc[ match_table_id ] [ 'name' ] 	     = C.iloc[ id ] [ 'ltable_name']

		match_table_id +=1






## Store match dataframe
match.to_pickle ( './match_data.pkl')
match.to_csv('./match_data.csv')
