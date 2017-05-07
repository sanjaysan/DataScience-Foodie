import pandas as pd
import numpy as np
from nltk import word_tokenize, pos_tag

## Python script used to process merged data [ processing - split address fields ]

match_data = pd.read_csv('./match_data.csv')

columns = ['number_of_reviews', 'price_range', 'ratingValue', 'name', 'street', 'city', 'state', 'zipcode']
num_matches = len(match_data)

# Index range for data frame
indx_range = range(num_matches)

# New data frame to hold address in separate fields
match_processed = pd.DataFrame(index=indx_range, columns=columns)

city_dict = {
    "Jose" : "San Jose",
    "City" : "Long Island City",
    "York" : "New York"
}

match_table_id = 0
for index, row in match_data.iterrows():

    # Copying all non-address fields from original match_data
    match_processed.iloc[match_table_id]['number_of_reviews'] = match_data.iloc[index]['number_of_reviews']
    match_processed.iloc[match_table_id]['price_range'] = np.float(match_data.iloc[index]['price_range'][1:])
    match_processed.iloc[match_table_id]['ratingValue'] = np.float(match_data.iloc[index]['ratingValue'])
    match_processed.iloc[match_table_id]['name'] = match_data.iloc[index]['name'].decode('utf-8')

    # Processing address string and splitting into fields based on space
    address_list = match_data.iloc[index]['address'].split(" ")

    street = ""

    # Finding city names using prefix
    city_prefix = ["San", "New"]

    if any(str in city_prefix for str in address_list[-4]):
        # If any of the prefixes are present, then skip the word before
        # the prefix. So if -4th index has the prefix, then skip -5 and
        # consider from -6 to beginning
        itr_limit = len(address_list) - 5
    elif "Island" in address_list[-4]:
        # Specific case - If Island is present in index -4, then skip the
        # next two indexes("Island" and "Long") as they will be part of
        # the city name. Start from -7 to beginning.
        itr_limit = len(address_list) - 6
    else:
        # If the prefixes or Island is not present, then it is a one word
        # city name. Hence, start from the -5th index
        itr_limit = len(address_list) - 4

    for i in range(itr_limit):
        street += address_list[i]
        if i < itr_limit - 1:
            street += " "

    zipcode = address_list[-1]
    state = address_list[-2]

    city_val = address_list[-3]
    if city_val in city_dict:
        # If the city prefix is present as a key in the dictionary,
        # refer its value, that is, the full name of the city
        city = city_dict[city_val]
    else:
        # Else just take the city name as it is
        city = city_val

    match_processed.iloc[match_table_id]['street'] = street
    match_processed.iloc[match_table_id]['city'] = city
    match_processed.iloc[match_table_id]['state'] = state
    match_processed.iloc[match_table_id]['zipcode'] = zipcode

    match_table_id += 1

match_processed.to_csv('../OLAPExploration/restaurant_details.csv', encoding='utf-8')
