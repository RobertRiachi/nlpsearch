from py2neo import Graph

import query_structure_identification as qsi
from Graph import findnodelevel, findpath

def get_users_query():
	#get the users input
	user_query = input("Please enter your query: ")
	
	#current assumption: if query is invalid the graph search will return nothing
	#working under that assumption we can go ahead and tag the users query
	tagged_query = qsi.handle_input(user_query)
	
	#return the tagged list
	return tagged_query

def output_subject_analysis(out_query):
	print(out_query)

	while(True):
		user_reply = input("Is this what you meant? (y/n)")

		if(user_reply == 'y'):
			print("Yeehaw!")
			break
		elif(user_reply == 'n'):
			print("Whoopsie")
			break
		else:
			continue
	
def analyze(tagged_input_query):
	number_subject = qsi.extract_numbers(tagged_input_query)
	possible_subject_list = qsi.extract_nouns(tagged_input_query)
	adjective_subject = qsi.noun_w_adj(tagged_input_query)

	x = len(possible_subject_list)
	ichild_jparent = False
	#this function does not yet exist, but this is how it will be called
	if(x > 1):
		for i in range(x):
			if(findnodelevel(possible_subject_list[i], active_graph) == True ):
				for j in range(1,x):
					k = i+j % x;
					if(findnodelevel(possible_subject_list[k], active_graph) == True):
						ichild_kparent = findpath(possible_subject_list[i], possible_subject_list[k], active_graph)
						if(ichild_kparent == True):
							subtopic_list = possible_subject_list[0:k] + possible_subject_list[k+1:]
							new_query = structured_query(possible_subject_list[k], subtopic_list, )


if __name__ == "__main__":
	print("Hello and welcome to Robert and Anthony's plaintext-to-SQL query enhancer!")
	tagged_input_query = get_users_query()
	print(tagged_input_query)
	out_query = analyze(tagged_input_query)