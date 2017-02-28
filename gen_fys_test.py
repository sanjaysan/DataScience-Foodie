""" Take a text document 
1) look for words withing tag
2) extract features and populate vector for each adjective
"""

import os
import re
from collections import defaultdict
from sets import Set

import nltk
import numpy


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def GenNegFys(list_of_words, noun_set, adj_list):
    features = []
    negative_words = []

    tag1 = "<adj>"
    tag2 = "</adj>"
    tag_set = Set([tag1, tag2])

    for windx in range(len(list_of_words)):

        prev_word_indx = windx - 1

        if prev_word_indx >= 0 and list_of_words[windx] not in tag_set and tag1 not in list_of_words[
            windx] and tag2 not in list_of_words[windx]:

            """ Feature - len in chars """

            fys_list = []

            fys_list.append(len(list_of_words[windx]))

            """ Feature-Preceded by another adj """

            prev_word_indx_2 = prev_word_indx - 1
            prev_word_2 = ""

            if prev_word_indx_2 > 0:
                prev_word_2 = list_of_words[prev_word_indx_2]

            if prev_word_2 in adj_list:

                fys_list.append(int(1))
            else:
                fys_list.append(int(0))

            """ Feature- Rest of them """

            prev_word = list_of_words[prev_word_indx]

            if prev_word.lower() == "a" or prev_word.lower() == "an" or prev_word_2.lower() == "a" or prev_word_2.lower() == "an":

                fys_list.append(int(1))

            else:
                fys_list.append(int(0))

            if prev_word.lower() == "was" or prev_word.lower() == "is" or prev_word_2.lower() == "was" or prev_word_2.lower() == "is":

                fys_list.append(int(1))

            else:
                fys_list.append(int(0))

            if prev_word.lower() == "are" or prev_word.lower() == "were" or prev_word_2.lower() == "are" or prev_word_2.lower() == "were":

                fys_list.append(int(1))

            else:
                fys_list.append(int(0))

            if prev_word.lower() == "so" or prev_word_2.lower() == "so":

                fys_list.append(int(1))

            else:
                fys_list.append(int(0))

            if prev_word.lower() == "super" or prev_word_2.lower() == "super":

                fys_list.append(int(1))

            else:
                fys_list.append(int(0))

            if prev_word.lower() == "very" or prev_word_2.lower() == "very":

                fys_list.append(int(1))
            else:

                fys_list.append(int(0))

            suc_word_indx = windx + 1
            suc_word = ""

            if suc_word_indx < len(list_of_words):
                suc_word = list_of_words[suc_word_indx]

            if suc_word in noun_set:

                fys_list.append(int(1))
            else:

                fys_list.append(int(0))

            if sum(fys_list[1:8]) >= 1:
                features.append(fys_list)
                negative_words.append(list_of_words[windx])

    return features, negative_words


""" An adjective is only one word long """

p = re.compile("<adj> (\w+) </adj>")

testing_words = []
features = []
target_label = []

list_indx = 0

directory = "/home/sabareesh/DataScience/DataScience-Foodie/Data/Test_Set/"

file_count = 0

for filename in os.listdir(directory):

    filepath = directory + filename

    file_count += 1

    with open(filepath, 'r') as myFile:
        data = myFile.read().replace('\n', '')

    """ Same adjective may appear multiple times with
        different features thus a default dictionary
        is created with key=word and value=tuple consisting of
        (list_indx,visited_flag). Thus a key will point to a list
        if multiple occurences are present """

    tokens = nltk.word_tokenize(data)
    tagged = nltk.pos_tag(tokens)
    nouns = [word for word, pos in tagged if pos.startswith('N')]
    cleaned_nouns = [word for word in nouns if word != '>' and word != '<' and word != '/adj' and word != 'adj']
    noun_set = Set(cleaned_nouns)

    list_of_words = data.split()

    index_list = list(range(0, len(list_of_words)))
    flag_list = [0] * len(list_of_words)

    index_flag_list = zip(index_list, flag_list)

    word_dict = defaultdict(list)

    for i in range(len(list_of_words)):
        word_dict[list_of_words[i]].append(index_flag_list[i])

    adj_list = p.findall(data)

    positive_words = []

    for adj in adj_list:

        if len(adj) >= 4:

            positive_words.append(adj)

            """ Length """

            features.append([])

            features[list_indx].append(len(adj))

            """ Finding index,visited list from dictionary """

            cur_indx = list_of_words.index(adj)

            indx_visited_list = word_dict[adj]

            for i in range(len(indx_visited_list)):

                if indx_visited_list[i][1] == 0:
                    cur_indx = indx_visited_list[i][0]
                    indx_visited_list[i] = (cur_indx, 1)
                    break

            """ Updating word_dict with visited information """

            word_dict[adj] = indx_visited_list

            prev_word_indx = cur_indx - 2
            prev_word_indx_2 = prev_word_indx - 1

            suc_word_indx = cur_indx + 2
            prev_word = ""
            prev_word_2 = ""

            if prev_word_indx_2 >= 0:
                prev_word_2 = list_of_words[prev_word_indx_2]

            if prev_word_indx >= 0:
                prev_word = list_of_words[prev_word_indx]

            """ Preceded by another adjective """

            if prev_word_2 in adj_list:

                features[list_indx].append(int(1))

            else:
                features[list_indx].append(int(0))

            """ Preceded by was/a/.. """

            if prev_word.lower() == "a" or prev_word.lower() == "an" or prev_word_2.lower() == "a" or prev_word_2.lower() == "an":

                features[list_indx].append(int(1))

            else:
                features[list_indx].append(int(0))

            if prev_word.lower() == "was" or prev_word.lower() == "is" or prev_word_2.lower() == "was" or prev_word_2.lower() == "is":

                features[list_indx].append(int(1))

            else:
                features[list_indx].append(int(0))

            if prev_word.lower() == "are" or prev_word.lower() == "were" or prev_word_2.lower() == "are" or prev_word_2.lower() == "were":

                features[list_indx].append(int(1))

            else:
                features[list_indx].append(int(0))

            if prev_word.lower() == "so" or prev_word_2.lower() == "so":

                features[list_indx].append(int(1))

            else:
                features[list_indx].append(int(0))

            if prev_word.lower() == "super" or prev_word_2.lower() == "super":

                features[list_indx].append(int(1))

            else:
                features[list_indx].append(int(0))

            """ Preceded by very """

            if prev_word.lower() == "very" or prev_word_2.lower() == "very":

                features[list_indx].append(int(1))

            else:
                features[list_indx].append(int(0))

            """ Succeded by noun """

            if suc_word_indx < len(list_of_words):
                suc_word = list_of_words[suc_word_indx]

            if suc_word in noun_set:

                features[list_indx].append(int(1))
            else:

                features[list_indx].append(int(0))

            list_indx += 1

    [negative_fys, negative_words] = GenNegFys(list_of_words, noun_set, adj_list)
    features = features + negative_fys
    list_indx = list_indx + len(negative_fys)
    target_label = target_label + [1] * len(positive_words) + [0] * len(negative_words)
    testing_words = testing_words + positive_words + negative_words

    if file_count == 100:
        break

print target_label.count(1)
print target_label.count(0)

numpy.save('Data/Testing/test_features.npy', features)
numpy.savetxt('Data/Testing/test_features.txt', features)

numpy.save('Data/Testing/test_target_label.npy', target_label)
numpy.savetxt('Data/Testing/test_target_label.txt', target_label)

numpy.savetxt('Data/Testing/testing_words.txt', testing_words, fmt='%s')
numpy.save('Data/Testing/testing_words.npy', testing_words)
