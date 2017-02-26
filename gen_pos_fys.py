""" Take a text document 
1) look for words withing tag
2) extract features and populate vector for each adjective
"""

import re
import os
import numpy
import nltk
from sets import Set
from collections import defaultdict
from gen_neg_fys import GenNegFys


""" An adjective is only one word long """

p = re.compile("<adj> (\w+) </adj>")

training_words = []
features = []
feature_names = []
target_label = []

feature_names.append("Length in chars")
feature_names.append("Is preceded by another adj")
feature_names.append("Is preceded by a/an ")
feature_names.append("Is preceded by was/is")
feature_names.append("Is preceded by are/were")
feature_names.append("Is preceded by so")
feature_names.append("Is preceded by super")
feature_names.append("Is preceded by very")
feature_names.append("Is succeded by noun")


list_indx = 0


directory = "/home/sabareesh/DataScience/DataScience-Foodie/Data/Dev_Set/"

it = 0

for filename in os.listdir(directory):
		

	filepath = directory + filename

	with open(filepath,'r') as myFile:
		data=myFile.read().replace('\n','')
	
	
	""" Same adjective may appear multiple times with
	    different features thus a default dictionary 
	    is created with key=word and value=tuple consisting of
	    (list_indx,visited_flag). Thus a key will point to a list
	    if multiple occurences are present """
	
	tokens = nltk.word_tokenize(data)
	tagged = nltk.pos_tag(tokens)
	nouns = [ word for word,pos in tagged if pos.startswith('N') ]
	cleaned_nouns = [ word for word in nouns if word != '>' and word != '<' and word != '/adj' and word != 'adj']
	noun_set = Set(cleaned_nouns)

	

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

			suc_word_indx = cur_indx + 2
			suc_word = ""
	
	
	
	
			if   prev_word_indx_2 >= 0 : 
				
				prev_word_2 = list_of_words[ prev_word_indx_2 ]
	
			if   prev_word_indx >=0 :
	
				prev_word = list_of_words[ prev_word_indx]
	        	
		
			""" Preceded by another adjective """


			if prev_word_2 in adj_list:
	
				features[list_indx].append( int(1) )
	
			else:
				features[list_indx].append( int(0) )
	
			 
	
			""" Preceded by was/a/.. """
	
			if  prev_word.lower()  == "a" or prev_word.lower() == "an" or prev_word_2.lower() == "a" or prev_word_2.lower() == "an" :
				
				features[list_indx].append(int(1))
	
			else: 
				features[list_indx].append( int(0) )


			if  prev_word.lower()  == "was" or prev_word.lower() == "is" or prev_word_2.lower() == "was" or prev_word_2.lower() == "is" :
				
				features[list_indx].append(int(1))
	
			else: 
				features[list_indx].append( int(0) )


			if  prev_word.lower()  == "are" or prev_word.lower() == "were" or prev_word_2.lower() == "are" or prev_word_2.lower() == "were" :
				
				features[list_indx].append(int(1))
	
			else: 
				features[list_indx].append( int(0) )


			if  prev_word.lower()  == "so" or  prev_word_2.lower() == "so":
				
				features[list_indx].append(int(1))
	
			else: 
				features[list_indx].append( int(0) )


			if  prev_word.lower()  == "super" or prev_word_2.lower() == "super" :
				
				features[list_indx].append(int(1))
	
			else: 
				features[list_indx].append( int(0) )
			
	
			""" Preceded by very """
	
			if prev_word.lower() == "very" or prev_word_2.lower() == "very" :
	
				features[list_indx].append( int(1) )
	
			else:
				features[list_indx].append( int(0) )
	
			
			""" Succeded by noun """

			if   suc_word_indx < len( list_of_words ) :
	
				suc_word = list_of_words[ suc_word_indx ]

			if suc_word in noun_set:

				features[list_indx].append( int(1) )
			else:

				features[list_indx].append( int(0) )

			
			
			list_indx+=1	
	
	
			
				
	target_num     = len(positive_words) + 10 
	[negative_fys,negative_words] = GenNegFys( list_of_words, target_num, noun_set, adj_list )
	features       = features + negative_fys
	list_indx      = list_indx + len( negative_fys ) 
	target_label   = target_label + [1]*len(positive_words) + [0]*len(negative_words)
	training_words =  training_words + positive_words + negative_words
		

print target_label.count(1)
print target_label.count(0)


numpy.save('Data/Training/features.npy',features) 
numpy.savetxt('Data/Training/features.txt',features)

numpy.save('Data/Training/target_label.npy',target_label)
numpy.savetxt('Data/Training/target_label.txt',target_label)

numpy.savetxt('Data/Training/training_words.txt',training_words,fmt='%s')

numpy.savetxt('Data/Training/feature_names.txt',feature_names,fmt='%s')	 

numpy.save('Data/Training/training_words.npy',training_words)

numpy.save('Data/Training/feature_names.npy',feature_names)
