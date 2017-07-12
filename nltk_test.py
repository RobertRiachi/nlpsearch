#from nltk.tag.stanford import StanfordNERTagger

#st = StanfordNERTagger('../../nltk_data/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz', '../../nltk_data/stanford-ner/stanford-ner.jar')
#tokens = st.tag("Russell Westbrook, who plays for the Oklahoma City Thunder won the 2017 NBA MVP".split())

#print(tokens)

import nltk

sentence = "Russell Westbrook, who plays for the Oklahoma City Thunder won the 2017 NBA MVP"

tokens = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokens)

print(tagged)


def extract_nouns(token_list):

	nouns = []

	#iterate over all the nouns
	for i in range(len(token_list)):
		#check if that token is a token
		if(token_list[i][1] == 'NNP' or token_list[i][1] == 'NN'):
			#add the noun to the noun list
			nouns.append(token_list[i][0])
			j = 1
			#if there are more nouns back to back, add that to the list
			while(i+j < len(token_list) and (token_list[i+j][1] == 'NNP' or token_list[i+j][1] == 'NN')):
				nouns.append(nouns[-1] + ' ' + token_list[i+j][0])
				j += 1


	return nouns

print(extract_nouns(tagged))