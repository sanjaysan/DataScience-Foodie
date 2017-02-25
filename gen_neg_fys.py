""" Take a text document
1) Ignore words in the adj tag
2) Prune the negative examples
	- those that are atleast 4 chars long and have atleast one of "preceding chars" features set
"""


import re
from sets import Set


def GenNegFys( list_of_words,target_num ):

	features = []
	negative_words = []

	tag1    = "<adj>"
	tag2	= "</adj>"
	tag_set = Set( [tag1,tag2] )
 
	third_features = Set( ['was','a','are','is','so','were'] )
	
	num_negative = 0

	for windx in range( len(list_of_words) ):

		prev_word_indx = windx - 1

		if prev_word_indx >=0  and list_of_words[windx] not in tag_set and tag1 not in list_of_words[windx] and tag2 not in list_of_words[windx] :


			""" Feature - len in chars """

			fys_list = []

			fys_list.append ( len( list_of_words[windx] ) )


			""" Feature-Preceded by Super """
		
			prev_word_indx_2 = prev_word_indx-1

			if prev_word_indx_2 > 0 :

				if  list_of_words[ prev_word_indx_2 ].lower() == "super" :
			
					fys_list.append( int(1) )
				else:
					fys_list.append( int(0) )

			else:

				fys_list.append( int(0) )
		
			""" Feature- third and fourth """

			prev_word = list_of_words[ prev_word_indx ]
		
			if prev_word.lower() in third_features :

				fys_list.append( int(1) )
			else:
			
				fys_list.append( int(0) )

			if prev_word.lower() == "very":
				fys_list.append( int(1) )
			else:
			
				fys_list.append( int(0) )


			""" Pruning examples"""

			if  fys_list[1] + fys_list[2] + fys_list[3] >= 1 :

				features.append( fys_list )
				negative_words.append( list_of_words[windx] )
				num_negative+=1

			

	if num_negative < target_num:
	
		negative_word_set = Set( negative_words )
		
		for windx in range( len(list_of_words) ):

			prev_word_indx = windx - 1

			if num_negative >= target_num:
				break


			if prev_word_indx >=0  and list_of_words[windx] not in tag_set and list_of_words[windx] not in negative_word_set and tag1 not in list_of_words[windx] and tag2 not in list_of_words[windx]:

			
				if ( len ( list_of_words[windx] ) >= 4 ):
					fys_list = [len( list_of_words[windx] ),0,0,0]
					features.append ( fys_list )
					negative_words.append( list_of_words[windx] )
					num_negative+=1
				

		



	return features,negative_words

