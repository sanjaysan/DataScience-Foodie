""" Take a text document 
1) look for words withing tag
2) extract features and populate vector for each adjective
"""

import re
import os
import numpy
from sets import Set
from collections import defaultdict



def hasNumbers(inputString):
      return any(char.isdigit() for char in inputString)


def GenNegFys( list_of_words ):

	features = []
	negative_words = []

	tag1    = "<adj>"
	tag2	= "</adj>"
	tag_set = Set( [tag1,tag2] )
 
	third_features = Set( ['was','a','are','is','so','were'] )
	

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


			features.append( fys_list )
			negative_words.append( list_of_words[windx] )
			



	return features,negative_words



""" An adjective is only one word long """

p = re.compile("<adj> (\w+) </adj>")

testing_words = []
features = []
feature_names = []
target_label = []

feature_names.append("Length in chars")
feature_names.append("Is preceded by super")
feature_names.append("Is preceded by was/a/are/is/were/so")
feature_names.append("Is preceded by very")
feature_names.append("Is positive example")


list_indx = 0

third_features = Set( ['was','a','are','is','so','were'] )

directory = "/home/sabareesh/DataScience/DataScience-Foodie/Data/Test_Set/"


for filename in os.listdir(directory):
		
	filepath = directory + filename

	with open(filepath,'r') as myFile:
		data=myFile.read().replace('\n','')
	
	
	""" Same adjective may appear multiple times with
	    different features thus a default dictionary 
	    is created with key=word and value=tuple consisting of
	    (list_indx,visited_flag). Thus a key will point to a list
	    if multiple occurences are present """
	
	

	list_of_words = data.split()
	
	index_list = list ( range(0,len(list_of_words) ) )
	flag_list = [0]*len(list_of_words)
	
	index_flag_list = zip(index_list,flag_list)
	
	word_dict = defaultdict( list )
	
	for i in range ( len (list_of_words) ):
		word_dict[ list_of_words[i] ].append( index_flag_list[i] )
	
	adj_list = p.findall( data )

	positive_words = []
	
	for adj in adj_list:
	
	
		if len(adj) >= 4:
		
			positive_words.append( adj )
	
			""" Length """
		
			features.append( [] )
	
			features[list_indx].append( len( adj ) )
	
	
	       		""" Finding index,visited list from dictionary """
	
			cur_indx = list_of_words.index( adj )
	
			indx_visited_list = word_dict[ adj ]
	
		
			for i in range( len(indx_visited_list) ):
			
		    		if indx_visited_list[i][1] == 0:
	
					cur_indx = indx_visited_list[i][0]
					indx_visited_list[i] = (cur_indx,1)
					break
	
		
			""" Updating word_dict with visited information """
	
			word_dict[ adj ] = indx_visited_list
	
			prev_word_indx =  cur_indx - 2
			prev_word_indx_2 = prev_word_indx-1
			prev_word = ""
			prev_word_2 = ""
	
	
	        	""" Preceded by super """
	
	
			if   prev_word_indx_2 >= 0 : 
				
				prev_word_2 = list_of_words[ prev_word_indx_2 ]
	
				if prev_word_2.lower() == "super":
	
					features[list_indx].append( int(1) )
	
				else:
					features[list_indx].append( int(0) )
	
	
			else:
	
				features[ list_indx ].append( int(0) )
	
			 
			if   prev_word_indx >=0 :
	
				prev_word = list_of_words[ prev_word_indx]
	
	
			if  prev_word.lower() in third_features :
				
				features[list_indx].append(int(1))
	
			else: 
				features[list_indx].append( int(0) )
	
	
			""" Preceded by very """
	
			if prev_word.lower() == "very" :
	
				features[list_indx].append( int(1) )
	
			else:
				features[list_indx].append( int(0) )
	
			
			list_indx+=1

			
				
	[negative_fys,negative_words] = GenNegFys( list_of_words )
	features       = features + negative_fys
	list_indx      = list_indx + len( negative_fys ) 
	target_label   = target_label + [1]*len(positive_words) + [0]*len(negative_words)
	testing_words  =  testing_words + positive_words + negative_words
		



print target_label.count(1)
print target_label.count(0)

numpy.save('test_features.npy',features) 
numpy.savetxt('test_features.txt',features)

numpy.save('test_target_label.npy',target_label)
numpy.savetxt('test_target_label.txt',target_label)


numpy.savetxt('testing_words.txt',testing_words,fmt='%s')

numpy.save('testing_words.npy',testing_words)

