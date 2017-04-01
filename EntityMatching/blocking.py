
# coding: utf-8

# In[14]:

import py_entitymatching as em
import pandas as pd
import os,sys
import math


# In[76]:

A=em.read_csv_metadata('Data/csv/yelp_list.csv')
A['ID'] = range(0,len(A))
em.set_key(A,'ID')


B=em.read_csv_metadata('Data/csv/zomato_list.csv')
B['ID'] = range(0,len(B))
em.set_key(B,'ID')


# In[3]:

A


# In[4]:

B


# In[33]:

def clean_price_range( price_str ):

    avg_price = ''
    
    if not isinstance(price_str,basestring)  and  math.isnan(price_str):
        return price_str

    str2 = price_str.replace('$','')
        
    if '-' in str2:
        num_l = int(str2.split('-')[0])
        num_r = int(str2.split('-')[1])
        num_avg = (num_l+num_r)/2
        avg_price = '$' + str(num_avg)

    else:
        str_word = str2.split()[0].lower()
        num_price  = int(str2.split()[1])
        
        if str_word == 'above':
            num_avg = int(num_price + num_price/2)
            avg_price = '$' + str(num_avg)

        else:
            num_avg = num_price/2
            avg_price = '$' + str(num_avg)
            
    return avg_price


# In[6]:

def clean_num_reviews(review_string) :
     return review_string.split()[0]


# In[37]:

def clean_name( name_str):

	name_lower = name_str.lower()
	
	if "restaurant" not in name_lower and "restaurants" not in name_lower:
		name_lower = name_lower + " restaurant"

	return name_lower



# In[77]:

def clean_address( address ):
    addr_2 = address.replace('\"','')
    addr_3 = addr_2.replace(',','')
    if "Street" in addr_3:
        addr_3 = addr_3.replace('Street','St')
        
    return addr_3


# In[78]:

########## DATA CLEANING ################

##Converting A's price range to an absolute number
A['price_range'] = A['price_range'].apply( clean_price_range )

##Cleaning restaurant name of A
A['name'] = A['name'].apply( clean_name )

B['name'] = B['name'].apply( clean_name )
B['address'] = B['address'].apply( clean_address )
B['number_of_reviews'] = B['number_of_reviews'].apply( clean_num_reviews )



















# In[35]:

A['price_range']


# In[19]:

A.isnull().sum



# In[20]:

len(A.id) - A.count()


# In[21]:

len(A.ID) - A.count()


# In[22]:

len(B.ID) - B.count()


# In[41]:

A



# In[79]:

block_f = em.get_features_for_blocking(A,B)


# In[80]:

block_f




# In[81]:

rb1 = em.RuleBasedBlocker()
rule1 = 'name_name_lev_sim(ltuple,rtuple) < 0.8'
rb1.add_rule(rule1, block_f )

rb2 = em.RuleBasedBlocker()
rule2 = 'address_address_jac_qgm_3_qgm_3(ltuple,rtuple) < 0.9'
rb2.add_rule(rule2,block_f)


# In[63]:

C1 = rb1.block_tables(A,B,l_output_attrs=['ID','name','address','ratingValue','price_range','number_of_reviews'],r_output_attrs=['ID','name','address','ratingValue','price_range','number_of_reviews'])
C2 = rb2.block_tables(A,B,l_output_attrs=['ID','name','address','ratingValue','price_range','number_of_reviews'],r_output_attrs=['ID','name','address','ratingValue','price_range','number_of_reviews'])



# In[64]:

C2




# In[50]:

C


# In[56]:

dbg = em.debug_blocker(C,A,B,output_size=200)


# In[57]:

dbg


# In[ ]:



