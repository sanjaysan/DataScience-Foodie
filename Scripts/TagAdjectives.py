import fileinput
import os
import re

import nltk

directory = "/home/sanjay/Documents/UW Madison/Semester II/Data Science/DataScience-Foodie/Data/Test Set"
fileCount = 0
for filename in os.listdir(directory):
    f = fileinput.input(os.path.join(directory, filename), inplace=True)

    # Marking up train set (200 files)
    fileCount += 1
    if fileCount > 200:
        f.close()
        break

    tagged = None
    for line in f:

        # Changing to lower case
        line = line.lower()

        # Removing the new line character at the end of the line
        line = line.rstrip('\n')

        # Removing special characters specific to regex matching
        # (*, +, [, ]) from line
        line = re.sub(r'\*', '', line)
        line = re.sub(r'\[', '(', line)
        line = re.sub(r'\]', ')', line)
        line = re.sub(r'\+', '-', line)

        # Splitting the words in the line into tokens
        tokens = nltk.word_tokenize(line)

        # POS Tagging the tokens
        tagged = nltk.pos_tag(tokens)

        # Keeping a list of already tagged adjectives so that duplicates don't get
        # tagged again
        tagged_adjectives = []
        text_to_replace = None
        for i in range(0, len(tagged)):

            if (tagged[i][0] not in tagged_adjectives) \
                    and (tagged[i][1] == 'JJ' or tagged[i][1] == 'JJR' or tagged[i][1] == 'JJS'):
                # Surrounding the identified adjective with <adj>...</adj> tags
                # original_text
                text_to_replace = "<adj> " + tagged[i][0] + " </adj>"

                # Marking up the adjective with <adj>...</adj> tags
                line = re.sub(r"\b%s\b" % tagged[i][0], text_to_replace, line)

                # Adding the word to the list of tagged adjectives
                tagged_adjectives.append(tagged[i][0])
        if line != '\n':
            # Writing back to the file
            print line
    f.close()
