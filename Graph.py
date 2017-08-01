from py2neo import Graph
import re

#Link Graph Database
neograph = Graph(password="password")


#Given a Node, if exists returns label else returns false
def findlabel(node, ngraph):
	label = ngraph.data("MATCH (r) WHERE r.catName='"+node+"' RETURN labels(r)")
	if label:
		s = str(label[0])
		j = s.replace("'", "\"")
		d = json.loads(j)
		label = d['labels(r)'][0]
		return str(label)
	else:
		return False


#Given a word and a graph if node exists returns level, else returns false
def findnodelevel(word, ngraph):
	label = findlabel(word, ngraph)
	if not label:
		return False
	node = ngraph.data("Match(n:"+label+" {catName:'"+word+"'}) return n")
	s = str(node[0])
	j = re.findall(r'level:(.*?),',s)
	return j

#Given two nodes as strings and a graph, returns true if node1 is child of node2 else false
#Nodes must exist in graph	
def findpath(node1, node2, ngraph):
	label1 = findlabel(node1, ngraph)
	label2 = findlabel(node2, ngraph)
	path = ngraph.data("MATCH (f:"+label1+" {catName: '"+node1+"'}), (t:"+label2+" {catName: '"+node2+"'}), p = shortestPath((f)-[]-(t)) RETURN p")
	if path:
		return true
	else:
		return false
		
#Example findnode(17745, neograph)

#Deletes Knowledge Graph currently existing on your server where ngraph is that server info - see neograph var
def deletegraph(ngraph):
	ngraph.data("MATCH (n) DETACH DELETE n")


#Instantly creates a knowledge graph from wikipedia of the subject and depth you want :^) Robert original
#Subject = str, numoflevels = int, and numoflevels depth must exist in wikipedia, db = ur existing server - look at neograph var
def ngraphcreate(subject, numoflevels, db):
	db.data("CREATE INDEX ON :Category(catId)")
	db.data("CREATE INDEX ON :Category(catName)")
	db.data("CREATE INDEX ON :Category(catName)")
	db.data("CREATE (c:Category:RootCategory {catId: 0, catName: '"+subject+"', subcatsFetched : false, pagesFetched : false, level: 0 })")
	for i in range(numoflevels):
		db.data(":param level:"+(i+1)+"")
		db.data("MATCH (c:Category { fetched: false, level: $level - 1}) CALL apoc.load.json('https://en.wikipedia.org/w/api.php?format=json&action=query&list=categorymembers&cmtype=subcat&cmtitle=Category:' + apoc.text.urlencode(c.catName) + '&cmprop=ids%7Ctitle&cmlimit=500') YIELD value as results UNWIND results.query.categorymembers AS subcat MERGE (sc:Category {catId: subcat.pageid}) ON CREATE SET sc.catName = substring(subcat.title,9), sc.fetched = false, sc.level = $level WITH sc,c CALL apoc.create.addLabels(sc,['Level' +  $level + 'Category']) YIELD node MERGE (sc)-[:SUBCAT_OF]->(c) WITH DISTINCT c SET c.fetched = true")
