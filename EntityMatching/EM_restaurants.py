
# coding: utf-8

# <h1>Project Stage3 Entity Matching Workflow for Restaurant Data set

# **Introduction**
# 
# This IPython notebook explains a basic workflow two tables using py_entitymatching. 
# Our goal is to come up with a workflow to match restaurants from Yelp and Zomato sites.
# Specifically, we want to have precision of atleast 90 percent and as high recall as possible.
# 
# First, we need to import py_entitymatching package and other libraries as follows:

# In[76]:

import sys
sys.path.append('/usr/local/lib/python2.7/dist-packages/')

import py_entitymatching as em
import pandas as pd
import os,sys
import math


# In[77]:

##Display the versions
print('python version: ' + sys.version )
print('pandas version: ' + pd.__version__ )
print('magellan version: ' + em.__version__ )


# **Matching two tables typically consists of the following three steps**
# 
# 1. Reading the input tables
# 
# 2. Blocking the input tables to get a candidate set
# 
# 3. Matching the tuple pairs in the candidate set
# 

# <h1> Read the input tables </h1>
# 
# We begin by loading the input tables

# In[78]:

## Reading csv tables into pandas dataframe and set the key attribute in the dataframe

A=em.read_csv_metadata('../Data/csv/yelp_list.csv')
A['ID'] = range(0,len(A))
em.set_key(A,'ID')


B=em.read_csv_metadata('../Data/csv/zomato_list.csv')
B['ID'] = range(0,len(B))
em.set_key(B,'ID')


# In[79]:

print('Number of tuples in A: ' + str(len(A)))
print('Number of tuples in B: ' + str(len(B)))
print('Number of tuples in A X B (i.e the cartesian product): ' + str(len(A)*len(B)))


# In[80]:

## Sample tuples in A ( yelp_list )
A.head(2)


# In[81]:

## Sample tuples in B (zomato_list)
B.head(2)


# In[82]:

# Display the keys of the input tables
em.get_key(A), em.get_key(B)


# <h1> Data Cleaning 

# Some attributes of the table are cleaned for easier comparison. 
# Examples : 
#     * Price Range of yelp list is converted into a number (as it is in zomato)
#     * If the word "restaurant" appears as a last word in the restaurant name, it is removed.

# In[83]:

##Data Cleaning1: Converting  price range to an absolute number. Will be applied for yelp list 


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


# In[84]:

##Data Cleaning2: Removing "reviews" string from num_reviews column. Will be applied for zomato list


def clean_num_reviews(review_string) :
      return int(review_string.split()[0])


# In[85]:

##Data Cleaning3: Removing "restaurant" if it is the last word in restaurant name. to prevent inconsistentcy.
## Will be applied for both lists


def clean_name( name_str):

    name_lower = name_str.lower()

    name_2 = name_lower.split()[-1]
    
    if name_2 == 'restaurant':
        name_lower = name_lower.replace('restaurant','')
        
    return name_lower


# In[86]:

##Data Cleaning4: Removing quotes and shortening some words in address.Will be applied for zomato list 

def clean_address( address ):
    addr_2 = address.replace('\"','')
    addr_3 = addr_2.replace(',','')
    if "Street" in addr_3:
        addr_3 = addr_3.replace('Street','St')
    if "Boulevard" in addr_3:
        addr_3 = addr_3.replace('Boulevard','Blvd')
        
    return addr_3


# In[87]:

## Data Cleaning5: Convert rating value into string type
def clean_rating_value(ratingValue):
    return str(ratingValue)


# In[88]:

## Apply Data Cleaning to tables

A['price_range'] = A['price_range'].apply( clean_price_range )
A['name'] = A['name'].apply( clean_name )
A['ratingValue'] = A['ratingValue'].apply(clean_rating_value)



B['name'] = B['name'].apply( clean_name )
B['address'] = B['address'].apply( clean_address )
B['number_of_reviews'] = B['number_of_reviews'].apply( clean_num_reviews )
B['ratingValue'] = B['ratingValue'].apply(clean_rating_value)


# <h1> Block tables to get candidate set

# Before we do the matching, we would like to remove the obviously non-matching tuple pairs from the input tables. 
# This would reduce the number of tuple pairs considered for matching
# 
# We have first used a blackbox based blocker which looks at zipcode equivalence to obtain candidate sets.
# Further these candidate sets are pruned based on name similarity.
# 
# We use the entitymatching get_features routine to automatically generate features and choose the relevant ones 
# for blocking.
# 

# In[90]:

# Get features for blocking

block_f = em.get_features_for_blocking(A,B)


# In[91]:

# List the names of the features generated
block_f['feature_name']


# In[92]:

## Routine to block based on zipcode equivalence

def zipcode_match(x, y):
    # x, y will be of type pandas series
    
    # get address attribute
    x_address = x['address']
    y_address = y['address']
    
    # get the zipcode
    x_split, y_split = x_address.split(), y_address.split()
    x_zipcode = x_split[len(x_split) - 1]
    y_zipcode = y_split[len(y_split) - 1]
    
    # check if the zipcode match
    if x_zipcode != y_zipcode:
        return True
    else:
        return False


# In[93]:

## Instantiate blackbox blocker
bb = em.BlackBoxBlocker()

## Set the black box function
bb.set_black_box_function(zipcode_match)


# In[94]:

##Rule based on restaurant name similarity
rb1 = em.RuleBasedBlocker()
rule1 = 'name_name_lev_sim(ltuple,rtuple) < 0.60'
rb1.add_rule(rule1, block_f )


# In[95]:

## Blocking Pipeline- First block based on zip code then block based on name similarity##

C1 = bb.block_tables(A,B,l_output_attrs=['ID','name','address','ratingValue','price_range','number_of_reviews'],r_output_attrs=['ID','name','address','ratingValue','price_range','number_of_reviews'],n_jobs=-1)

C2 = rb1.block_candset(C1,n_jobs=-1)


# In[96]:

## Number of tuple pairs in C2
len(C2)


# <h1> Debug Blocker Output
# 

# The number of tuple pairs considered for matching is reduced to  (from 10536512 to 953), 
# but we would want to make sure that the blocker did not drop any potential matches.
# We could debug the blocker output in py_entitymatching as follows:

# In[97]:

# Debug blocker output
dbg = em.debug_blocker(C2, A, B, output_size=200)


# In[98]:

# Display first few tuple pairs from the debug_blocker's output
dbg.head()


# From the debug blocker's output we observe that the current blocker drops quite a few potential matches. 
# We would want to update the blocking sequence to avoid dropping these potential matches.
# 
# For the considered dataset, we know that for the restaurants to match, the address should be similar.
# We could use rule based blocker with address similarity for this purpose.
# Finally, we would want to union the outputs from the name similarity blocker and the address blocker to get a consolidated candidate set.
# 

# In[99]:

##Rule based on address similarity
rb2 = em.RuleBasedBlocker()
rule2 = 'address_address_jac_qgm_3_qgm_3(ltuple,rtuple) < 0.8'
rb2.add_rule(rule2,block_f)


# In[100]:

###Address based blocker###
C3 = rb2.block_candset(C1,n_jobs=-1)

len(C3)


# In[71]:

## Display first two rows of C3
C3.head(2)


# In[101]:

## Combine blocker outputs
C4 = em.combine_blocker_outputs_via_union([C2, C3])


# In[102]:

len(C4)


# We observe that the number of tuple pairs considered for matching is increased to 2048 (from 953). 
# Now let us debug the blocker output again to check if the current blocker sequence is dropping any potential matches.

# In[103]:

# Debug again
dbg = em.debug_blocker(C4, A, B)


# In[104]:

# Display first few rows from the debugger output
dbg.head(3)


# We observe that the current blocker sequence does not drop obvious potential matches, and we can proceed with the matching step now. 

# <h1>  Matching tuple pairs in the candidate set

# 
# 
# In this step, we would want to match the tuple pairs in the candidate set. Specifically, we use learning-based method for matching purposes. This typically involves the following five steps:
# 
# * Sampling and labeling the candidate set
# * Splitting the labeled data into development and evaluation set
# * Selecting the best learning based matcher using the development set
# * Evaluating the selected matcher using the evaluation set
# 
# 

# <h1> Sampling and labeling the candidate set

# First, we randomly sample 350 tuple pairs for labeling purposes.

# In[105]:

##Sample candidate set
S = em.sample_table(C4, 350)


# In[23]:

##Label S 
G = em.label_table(S, 'gold_labels')


# Load labeled data fom previous session

# In[105]:

G = em.load_object('./GoldenData.pkl')
len(G)


# In[106]:

## Loading G into em catalog

em.set_fk_ltable(G, 'ltable_ID')
em.set_fk_rtable(G, 'rtable_ID')
em.set_key(G, '_id')
em.set_ltable(G, A)
em.set_rtable(G, B)


# In[107]:

## Find number of positive and negative examples 
G.groupby('gold_labels').count()


# <h1> Splitting the labeled data into development and evaluation set
# 
# 
# 

# In this step, we split the labeled data into two sets: development (I) and evaluation (J). Specifically, the development set is used to come up with the best learning-based matcher and the evaluation set used to evaluate the selected matcher on unseen data.

# In[109]:

# Split S into development set (I) and evaluation set (J)
train_test = em.split_train_test(G, train_proportion=0.7)
I = train_test['train']
J = train_test['test']


# <h1>  Selecting the best learning-based matcher

# Selecting the best learning-based matcher typically involves the following steps:
# 
# * Creating a set of learning-based matchers
# * Creating features
# * Converting the development set into feature vectors
# * Selecting the best learning-based matcher using k-fold cross validation
# 

# Creating a set of learning-based matchers
# ------------------

# In[111]:

## Create a set of ML Matchers
dt = em.DTMatcher()
rf = em.RFMatcher()
nb = em.NBMatcher()
logreg = em.LogRegMatcher()
linreg = em.LinRegMatcher()
svm = em.SVMMatcher()


# Creating features
# ------------------

# Next, we need to create a set of features for the development set. py_entitymatching provides a way to automatically generate features based on the attributes in the input tables. We drop the unwanted features from the feature table

# In[113]:

## Generate features
match_f = em.get_features_for_matching(A, B)
match_f.drop([13,14,15,16], inplace = True)


# In[114]:

# List the names of the features generated
match_f['feature_name']


# Converting the development set to feature vectors
# ------------------

# In[116]:

# Convert the I into a set of feature vectors using F

H = em.extract_feature_vecs(I, feature_table=match_f, attrs_after=['gold_labels'])


# In[117]:

## Display first three rows
H.head(3)


# Selecting the best matcher using cross-validation
# ------------------

# Now, we select the best matcher using k-fold cross-validation.
# For the purposes of this guide, we use ten fold cross validation and use 'precision' and 'recall' metric to select the best matcher

# In[120]:

## Select the best ML matcher using CV

result_precision = em.select_matcher(matchers=[dt, rf, nb, logreg, linreg, svm], table=H, exclude_attrs=[], target_attr='gold_labels', metric='precision', k=10)
result_precision['cv_stats']


# In[121]:

# Measuring recall
result_recall = em.select_matcher(matchers=[dt, rf, nb, logreg, linreg, svm], table=H, exclude_attrs=[], target_attr='gold_labels', metric='recall', k=10)
result_recall['cv_stats']


# Debugging Matcher
# ------------------

# We observe that the best matcher is either Linear Regression or Random Forest.
# We debug the RandomForest matcher to see what might be wrong( since it easier to debug). 
# To do this, first we split the feature vectors into train and test.

# In[126]:

## Split feature vectors (H) into train and test
rf = em.RFMatcher()
UV = em.split_train_test(H, train_proportion=0.5)
U = UV['train']
V = UV['test']


# Next, we debug the matcher using GUI. 

# In[85]:

# Debug random forest using GUI

em.vis_debug_rf(rf,U,V,
               exclude_attrs=['_id','ltable_ID','rtable_ID','gold_labels'],
               target_attr='gold_labels')


# From the debugger we notice there are many false negatives due to incorrect labeling

# In[106]:

## Relabel the sample
G2 = em.label_table(S, 'gold_labels')


# In[128]:

#load labeled data from previous session
G2 = em.load_object('./GoldenData2.pkl')
len(G2)


# In[129]:

## Load G2 into em catalog
em.set_fk_ltable(G2, 'ltable_ID')
em.set_fk_rtable(G2, 'rtable_ID')
em.set_key(G2, '_id')
em.set_ltable(G2, A)
em.set_rtable(G2, B)


# In[130]:

## Split into train and test set
train_test = em.split_train_test(G2, train_proportion=0.7)
I2 = train_test['train']
J2 = train_test['test']


# In[131]:

## Extract features
H2 = em.extract_feature_vecs(I2, feature_table=match_f, attrs_after=['gold_labels'])


# In[132]:

## Cross validation score
result = em.select_matcher(matchers=[dt, rf, nb, logreg, linreg, svm], table=H2, exclude_attrs=[], target_attr='gold_labels', metric='precision', k=10)
result['cv_stats']


# In[133]:

## Cross validation score for recall
result_recall_2 = em.select_matcher(matchers=[dt, rf, nb, logreg, linreg, svm], table=H, exclude_attrs=[], target_attr='gold_labels', metric='recall', k=10)
result_recall_2['cv_stats']


# We observe that due to relabeling both precision and recall have improved.Now we can further debug and look for improvements

# Debugging Matcher
# ------------------

# We debug the RandomForest matcher to see what might be wrong(since it easier to debug). To do this, first we split the feature vectors into train and test.

# In[135]:

## Split feature vectors (H) into train and test
UV2 = em.split_train_test(H, train_proportion=0.5)
U2 = UV2['train']
V2 = UV2['test']


# Next, we debug the matcher using GUI. 

# In[116]:

# Debug random forest using GUI

em.vis_debug_rf(rf,U2,V2,
               exclude_attrs=['_id','ltable_ID','rtable_ID','gold_labels'],
               target_attr='gold_labels')


# From the GUI, we observe that there are just few false positives and negatives. We can proceed for evaluation.
# 

# <h1> Evaluating the matching output

# Form feature vectors for the test set J

# In[136]:

L2 = em.extract_feature_vecs(J2, feature_table=match_f, attrs_after=['gold_labels'])


# Here we train the machine learning classifiers on the train set I

# In[147]:

# Train random forest using feature vectors from I
rf.fit(table = H2,
        exclude_attrs=['_id','ltable_ID','rtable_ID','gold_labels'],
        target_attr='gold_labels')


# In[146]:

# Train decision tree using feature vectors from I
dt.fit(table = H2,
        exclude_attrs=['_id','ltable_ID','rtable_ID','gold_labels'],
        target_attr='gold_labels')


# In[145]:

# Train Naive Bayesian
nb.fit(table = H2,
        exclude_attrs=['_id','ltable_ID','rtable_ID','gold_labels'],
        target_attr='gold_labels')


# In[149]:

# Train linear regression
linreg.fit(table = H2,
        exclude_attrs=['_id','ltable_ID','rtable_ID','gold_labels'],
        target_attr='gold_labels')


# In[150]:

# Train logistic regression
logreg.fit(table = H2,
        exclude_attrs=['_id','ltable_ID','rtable_ID','gold_labels'],
        target_attr='gold_labels')


# In[151]:

# Train SVM
svm.fit(table = H2,
        exclude_attrs=['_id','ltable_ID','rtable_ID','gold_labels'],
        target_attr='gold_labels')


# Here we use the above trained machine learning algorithms to predict the label for the test set J

# In[153]:

# Evaluate Random Forest
predictions_rf = rf.predict(table = L2,
                        exclude_attrs=['_id','ltable_ID','rtable_ID','gold_labels'],
                        append = True, target_attr='predicted', inplace=False)


# In[154]:

eval_result = em.eval_matches(predictions_rf, 'gold_labels', 'predicted')
em.print_eval_summary(eval_result)


# In[157]:

# Evaluate Linear Regression
predictions_linreg = linreg.predict(table = L2,
                        exclude_attrs=['_id','ltable_ID','rtable_ID','gold_labels'],
                        append = True, target_attr='predicted', inplace=False)


# In[158]:

eval_result = em.eval_matches(predictions_linreg, 'gold_labels', 'predicted')
em.print_eval_summary(eval_result)


# In[159]:

# Evaluate Logistic Regression
predictions_logreg = logreg.predict(table = L2,
                        exclude_attrs=['_id','ltable_ID','rtable_ID','gold_labels'],
                        append = True, target_attr='predicted', inplace=False)


# In[160]:

eval_result = em.eval_matches(predictions_logreg, 'gold_labels', 'predicted')
em.print_eval_summary(eval_result)


# In[161]:

# Evaluate Decision Tree
predictions_dt = dt.predict(table = L2,
                        exclude_attrs=['_id','ltable_ID','rtable_ID','gold_labels'],
                        append = True, target_attr='predicted', inplace=False)


# In[162]:

eval_result = em.eval_matches(predictions_dt, 'gold_labels', 'predicted')
em.print_eval_summary(eval_result)


# In[164]:

# Evaluate Naive Bayesian
predictions_nb = nb.predict(table = L2,
                        exclude_attrs=['_id','ltable_ID','rtable_ID','gold_labels'],
                        append = True, target_attr='predicted', inplace=False)


# In[165]:

eval_result = em.eval_matches(predictions_nb, 'gold_labels', 'predicted')
em.print_eval_summary(eval_result)


# In[166]:

# Evaluate SVM
predictions_svm = svm.predict(table = L2,
                        exclude_attrs=['_id','ltable_ID','rtable_ID','gold_labels'],
                        append = True, target_attr='predicted', inplace=False)


# In[169]:

eval_result = em.eval_matches(predictions_svm, 'gold_labels', 'predicted')
em.print_eval_summary(eval_result)


# From the results, we observe that Linear Regression is the best classifier. Below are the P, R, F1 scores for the same.

# In[170]:

## Thus the best matcher is linear regression based with precision,recall and F1 scores given below
eval_result = em.eval_matches(predictions_linreg, 'gold_labels', 'predicted')
em.print_eval_summary(eval_result)

