from py2neo import Graph
import re

#Link Graph Database
neograph = Graph(password="password")

#Wordpath: takes a word and a neo4j graph database, returns the cat nodes beloging to shortest path to the root node
def wordpath(word, ngraph):
	path = ngraph.data("MATCH path = shortestpath((x:Category {catName: '" + word + "'})-[:SUBCAT_OF*]->(root:RootCategory)) RETURN path")
	words = re.findall('"([^"]*)"', str(path))
	return words

	
def findnode(word, label, ngraph):
	node = ngraph.data("MATCH (n {"+label+": '"+word+"' }) return n")
	
	if node:
		return node
	else:
		print("Node does not exist")
		
#Example findnode('LOL', 'catName', neograph)
