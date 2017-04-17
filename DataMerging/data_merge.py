import numpy as np
import pandas as pd
import py_entitymatching as em

### Reading the necessary data ###

# Loading candidate set data
C = pd.read_pickle('./candidate_set.pkl')

# Loading candidate set predictions (obtained after applying the trained classifier to candidate set)
Cpred = pd.read_pickle('./candidate_set_predictions.pkl')

### Creating the matched data frame ###

# Columns for the new data frame which will hold the merged data
columns = ['number_of_reviews', 'price_range', 'ratingValue', 'name', 'address']
num_matches = len(Cpred[(Cpred['predicted'] == 1)])

# Index range for data frame
indx_range = range(num_matches)

# New data frame to hold merged data
match = pd.DataFrame(index=indx_range, columns=columns)

### Merging data ###

# Iterating over tuples in Cpred to find predicted matches
match_table_id = 0
for index, row in Cpred.iterrows():

    # Extracting only those tuples which are classified as a match by the trained classifier
    if int(row['predicted']) == 1:
        id = int(row['_id'])

        # Populating match data frame
        # Computing Jaccard over 3-gram J(3g) tokenization score for name
        name_match_score = em.jaccard(em.tok_qgram(C.iloc[id]['ltable_name'], 3),
                                      em.tok_qgram(C.iloc[id]['rtable_name'], 3))

        # Those names whose J(3g) score > 0.3 are considered matches
        if (name_match_score > 0.3):
            # For tuples whose J(3g(name)) is > 0.3, J(3g) is computed on address
            address_match_score = em.jaccard(em.tok_qgram(C.iloc[id]['ltable_address'], 3),
                                             em.tok_qgram(C.iloc[id]['rtable_address'], 3))
            if (address_match_score > 0.3):
                # For those tuples whose J(3g(name)) and J(3g(address)) > 0.3

                # Rules for picking the restaurant name from the two tables
                if C.iloc[id]['ltable_name'] == C.iloc[id]['rtable_name']:
                    match.iloc[match_table_id]['name'] = C.iloc[id]['ltable_name']
                else:
                    # Picking the longer name from the two tables
                    if len(C.iloc[id]['ltable_name']) > len(C.iloc[id]['rtable_name']):
                        match.iloc[match_table_id]['name'] = C.iloc[id]['ltable_name']
                    else:
                        match.iloc[match_table_id]['name'] = C.iloc[id]['rtable_name']

                # Rules for picking the restaurant address from the two tables
                if C.iloc[id]['ltable_address'] == C.iloc[id]['rtable_address']:
                    match.iloc[match_table_id]['address'] = C.iloc[id]['ltable_address']
                else:
                    # Picking the longer address from the two tables
                    if len(C.iloc[id]['ltable_address']) > len(C.iloc[id]['rtable_address']):
                        match.iloc[match_table_id]['address'] = C.iloc[id]['ltable_address']
                    else:
                        match.iloc[match_table_id]['address'] = C.iloc[id]['rtable_address']

                # Rules for picking the number of reviews for a restaurant from the two tables
                # Picking the one which has higher number of reviews
                if C.iloc[id]['ltable_number_of_reviews'] > C.iloc[id]['rtable_number_of_reviews']:
                    match.iloc[match_table_id]['number_of_reviews'] = C.iloc[id]['ltable_number_of_reviews']
                else:
                    match.iloc[match_table_id]['number_of_reviews'] = C.iloc[id]['rtable_number_of_reviews']

                # Rules for picking the price range for a restaurant from the two tables
                # Computing and storing the average of the two price ranges in the merged table
                if C.iloc[id]['ltable_price_range'] == C.iloc[id]['rtable_price_range']:
                    match.iloc[match_table_id]['price_range'] = C.iloc[id]['ltable_price_range']
                else:
                    match.iloc[match_table_id]['price_range'] = np.mean(np.array(
                        [np.float(C.iloc[id]['ltable_price_range'][1:]),
                         np.float(C.iloc[id]['rtable_price_range'][1:])]))

                # Rules for picking the rating value for a restaurant from the two tables

                # If both tables have non-null values for rating, pick the highest rating out of the two values
                if (C.iloc[id]['ltable_ratingValue'] != '-' and C.iloc[id]['rtable_ratingValue'] != '-'):
                    if (float(C.iloc[id]['ltable_ratingValue'][1:]) > float(C.iloc[id]['rtable_ratingValue'][1:])):
                        match.iloc[match_table_id]['ratingValue'] = C.iloc[id]['ltable_ratingValue']
                    else:
                        match.iloc[match_table_id]['ratingValue'] = C.iloc[id]['rtable_ratingValue']

                # If there are null values in either table, pick the non-null values
                elif (C.iloc[id]['ltable_ratingValue'] == '-' and C.iloc[id]['rtable_ratingValue'] != '-'):
                    match.iloc[match_table_id]['ratingValue'] = C.iloc[id]['rtable_ratingValue']
                elif (C.iloc[id]['ltable_ratingValue'] != '-' and C.iloc[id]['rtable_ratingValue'] == '-'):
                    match.iloc[match_table_id]['ratingValue'] = C.iloc[id]['ltable_ratingValue']
                else:
                    # If both tables have null values for rating, then choose either
                    match.iloc[match_table_id]['ratingValue'] = C.iloc[id]['ltable_ratingValue']
        match_table_id += 1

# Filtering out only the tuples which have non-null values for the "name" attribute
match = match[pd.notnull(match['name'])]

# Storing the merged dataframe in a pickle and csv file
match.to_pickle('./match_data.pkl')
match.to_csv('./match_data.csv')
