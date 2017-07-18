import query_structure_identification as qsi

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
	noun_subject= qsi.extract_nouns(tagged_input_query)
	adjective_subject = qsi.noun_w_adj(tagged_input_query)

	#TODO
	#decide which is the main thing, which are the sub-parts
	#initilaize a structured_query object


if __name__ == "__main__":
	print("Hello and welcome to Robert and Anthony's plaintext-to-SQL query enhancer!")
	tagged_input_query = get_users_query()
	print(tagged_input_query)
	out_query = analyze(tagged_input_query)