""" Take a text document 
1) look for words withing tag
2) extract features and populate vector for each adjective
"""

import re
from sets import Set


text_file = open('Data/text/review48.txt','r')

""" An adjective is only one or two words long """

p = re.compile("<adj> (\w+\s*\w*) </adj>")

features = []

features.append ( [] )
features[0].append("Length in words")
features[0].append("Contains super")
features[0].append("Is preceded by was/a/are/is/so")
features[0].append("Is positive example")

list_indx = 0

third_features = Set( ['was','a','are','is','so'] )

for line in text_file:
		
    adj_list = p.findall( line )
    
    list_of_words = line.split()

    for adj in adj_list:

	 features.append( [] )
	 list_indx+=1
	
	 """Length Feature"""

	 features[ list_indx ].append( len ( adj.split() ) )
	 
	
	 """Second Feature"""

	 first_word_adj = adj.split()[0]

	 if  first_word_adj.lower() == "super" : 
	
	 	features[ list_indx ].append( int(1) )

	 else:
	 	features[ list_indx ].append( int(0) )
	 
        
         """ Finding the prev word ( before tag ) for rest of features  """

	 prev_word_indx =  list_of_words.index(first_word_adj) - 2
	 prev_word = ""

	 if   prev_word_indx >= 0 : 
		
	 	prev_word = list_of_words[ prev_word_indx] 

	 
	 """Third Feature"""
	
	 if  prev_word.lower() in third_features :

	 	features[list_indx].append ( int(1) )

	 else :
	
	 	features[ list_indx].append( int(0) )

	
         """Fourth feature"""

	 features[list_indx].append( int(1) )




print features 
	 
