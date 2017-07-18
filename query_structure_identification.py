#from nltk.tag.stanford import StanfordNERTagger

#st = StanfordNERTagger('../../nltk_data/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz', '../../nltk_data/stanford-ner/stanford-ner.jar')
#tokens = st.tag("Russell Westbrook, who plays for the Oklahoma City Thunder won the 2017 NBA MVP".split())

#print(tokens)

import nltk

# test sentences for verifying each tag interpreter module
sentence1 = "Russell Westbrook, who plays for the Oklahoma City Thunder won the 2017 NBA MVP"

sentence2 = "Russell Westbook is a talented basketball player and a fancy hombre"

sentence3 = "Russell Westbrook averaged over 30 points, 10 rebounds and 10 assists"

sentence4 = "Who was the 44th President of the United States"

sentence5 = "In what year did OutKast release their second album"

#we only need a small class to hold the main subject, any sub-topics, and the resulting SQL
class structured_query:
	_subject					#this is a string
	_sub_topics = []			#this is a list, although it will often be a single element
	_resulting_sql			#this is a string
	_related_sql = []		#this is a list

	def __init__(self, subject, sub_topics):
		self._subject = subject
		self._sub_topics = sub_topics

#self explanatory, saves a bit of writing
def is_noun(type):
	if(type[0:2] == 'NN'):
		return True
	else:
		return False

#returns a non-empty list of the original noun plus any possible multi word nouns
#from nouns that immediately follow the original noun
def multi_word_noun(token_list, i):
	more_words = []
	j = 1

	more_words.append(token_list[i][0])
	
	#if there are more nouns back to back, add that to the list
	while(i+j < len(token_list) and is_noun(token_list[i+j][1])):
		#we can simply concatenate the last element of the list 
		more_words.append(more_words[-1] + ' ' + token_list[i+j][0])
		j += 1

	return more_words


#this function makes the assumption that a number will precede a noun to identify it
#TO DO: make a general function for checking nouns, multiple word nouns, and adjective + noun combinations
def extract_numbers(token_list):

	numbers = []

	#iterate over all the words
	for i in range(len(token_list)):
		#check if that token is a number
		if(token_list[i][1] == 'CD'):
			#can easily add checks for multiple POS here
			if(i+1 < len(token_list) and is_noun(token_list[i+1][1])):
				numbers.append(token_list[i][0] + ' ' + token_list[i+1][0])
			else:
				#don't do anything for now, how should sole numbers be treated?
				continue

	return numbers


def noun_w_adj(token_list):
	noun_adj_pair= []

	for i in range(len(token_list)):
		if(token_list[i][1] == 'JJ'):
			if(i+1 < len(token_list) and is_noun(token_list[i+1][1])):
				possible_nouns = multi_word_noun(token_list, i+1)
				for j in range(len(possible_nouns)):
					noun_adj_pair.append(token_list[i][0] + ' ' + possible_nouns[j])

	return noun_adj_pair
				

def extract_nouns(token_list):

	nouns = []

	#iterate over all the words
	for i in range(len(token_list)):
		#check if that token is a token
		if(is_noun(token_list[i][1])):
			#add the noun to the noun list
			nouns += multi_word_noun(token_list, i)

	#return the list for further use
	return nouns

def handle_input(user_query):
	tokenized_query = nltk.word_tokenize(user_query)
	tagged_query = nltk.pos_tag(tokenized_query)

	return tagged_query

