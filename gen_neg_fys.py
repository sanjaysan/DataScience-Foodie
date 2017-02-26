""" Take a text document
1) Ignore words in the adj tag
2) Prune the negative examples
	- those that are atleast 4 chars long and have atleast one of "preceding chars" features set
"""


import re
from sets import Set


def GenNegFys( list_of_words,target_num,noun_set,adj_list ):

	features = []
	negative_words = []

	tag1    = "<adj>"
	tag2	= "</adj>"
	tag_set = Set( [tag1,tag2] )
 
	num_negative = 0

	for windx in range( len(list_of_words) ):

		prev_word_indx = windx - 1

		if num_negative > target_num:
			break

		if prev_word_indx >=0  and list_of_words[windx] not in tag_set and tag1 not in list_of_words[windx] and tag2 not in list_of_words[windx] :


			""" Feature - len in chars """

			fys_list = []

			fys_list.append ( len( list_of_words[windx] ) )


			""" Feature-Preceded by another adj """
		
			prev_word_indx_2 = prev_word_indx-1
			prev_word_2 = ""

			if prev_word_indx_2 > 0 :

				prev_word_2 = list_of_words[ prev_word_indx_2 ]

			
			if prev_word_2 in adj_list :
			
				fys_list.append( int(1) )
			else:
				fys_list.append( int(0) )

		
			""" Feature- Rest of them """

			prev_word = list_of_words[ prev_word_indx ]
	
			if  prev_word.lower()  == "a" or prev_word.lower() == "an" or prev_word_2.lower() == "a" or prev_word_2.lower() == "an" :
				
				fys_list.append(int(1))
	
			else: 
				fys_list.append( int(0) )


			if  prev_word.lower()  == "was" or prev_word.lower() == "is" or prev_word_2.lower() == "was" or prev_word_2.lower() == "is" :
				
				fys_list.append(int(1))
	
			else: 
				fys_list.append( int(0) )


			if  prev_word.lower()  == "are" or prev_word.lower() == "were" or prev_word_2.lower() == "are" or prev_word_2.lower() == "were" :
				
				fys_list.append(int(1))
	
			else: 
				fys_list.append( int(0) )


			if  prev_word.lower()  == "so" or  prev_word_2.lower() == "so":
				
				fys_list.append(int(1))
	
			else: 
				fys_list.append( int(0) )


			if  prev_word.lower()  == "super" or prev_word_2.lower() == "super" :
				
				fys_list.append(int(1))
	
			else: 
				fys_list.append( int(0) )
			

			if prev_word.lower() == "very" or prev_word_2.lower() == "very":

				fys_list.append( int(1) )
			else:
			
				fys_list.append( int(0) )


			suc_word_indx = windx + 1
			suc_word = ""
	
			if   suc_word_indx < len( list_of_words ) :
	
				suc_word = list_of_words[ suc_word_indx ]

			if suc_word in noun_set:
				fys_list.append( int(1) )
			else:
				fys_list.append( int(0) )



			""" Pruning examples"""

			if  sum(fys_list[1:8])  >= 1 :

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
					fys_list = [len( list_of_words[windx] ),0,0,0,0,0,0,0,0]
					features.append ( fys_list )
					negative_words.append( list_of_words[windx] )
					num_negative+=1
				

		



	return features,negative_words

