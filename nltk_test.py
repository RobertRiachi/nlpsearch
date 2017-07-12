#from nltk.tag.stanford import StanfordNERTagger

#st = StanfordNERTagger('../../nltk_data/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz', '../../nltk_data/stanford-ner/stanford-ner.jar')
#tokens = st.tag("Russell Westbrook, who plays for the Oklahoma City Thunder won the 2017 NBA MVP".split())

#print(tokens)

import nltk

#test for nouns
sentence1 = "Russell Westbrook, who plays for the Oklahoma City Thunder won the 2017 NBA MVP"
#test for adjective + noun(s)
sentence2 = "Russell Westbook is an amazing, talented basketball player"
#test for number + noun
sentence3 = "Russell Westbrook averaged over 30 points, 10 rebounds and 10 assists"


tokens = nltk.word_tokenize(sentence3)
tagged = nltk.pos_tag(tokens)

print(tagged)

#this function makes the assumption that a number will precede a noun to identify it
#TO DO: make a general function for checking nouns, multiple word nouns, and adjective + noun combinations
def extract_numbers(token_list):

	numbers = []

	#iterate over all the words
	for i in range(len(token_list)):
		#check if that token is a number
		if(token_list[i][1] == 'CD'):
			#can easily add checks for multiple POS here
			if(i+1 < len(token_list) and (token_list[i+1][1] == 'NNS' or token_list[i+1][1] == 'NN' or token_list[i+1][1] == 'NNP')):
				numbers.append(token_list[i][0] + ' ' + token_list[i+1][0])
			else:
				#don't do anything for now, how should sole numbers be treated?
				continue

	return numbers


def extract_nouns(token_list):

	nouns = []

	#iterate over all the words
	for i in range(len(token_list)):
		#check if that token is a token
		if(token_list[i][1] == 'NNP' or token_list[i][1] == 'NN'):
			#add the noun to the noun list
			nouns.append(token_list[i][0])
			j = 1
			#if there are more nouns back to back, add that to the list
			while(i+j < len(token_list) and (token_list[i+j][1] == 'NNP' or token_list[i+j][1] == 'NN' or token_list[i+1][1] == 'NNS')):
				#we can simply concatenate the last element of the list 
				nouns.append(nouns[-1] + ' ' + token_list[i+j][0])
				j += 1

	#return the list for further use
	return nouns

print(extract_numbers(tagged))