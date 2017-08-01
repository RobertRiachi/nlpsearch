from py2neo import Graph
import re

#Link Graph Database
neograph = Graph(password="password")
	
def findnode(idnum, ngraph):
	node = ngraph.data("MATCH (n {ID: "+str(idnum)+"}) return n")
	
	if node:
		return node
	else:
		print("Node does not exist")
		
def findlabel(node, ngraph):
	label = ngraph.data("MATCH (r) WHERE r.catName="+node+" RETURN labels(r)")
	label = str(label)
	return label
	
def findpath(node1, node2, ngraph):
	label1 = findlabel(node1, ngraph)
	label2 = findlabel(node2, ngraph)
	path = ngraph.data("MATCH (f:"+label1+" {catName: "+node1+"}), (t:"+label2+" {catName: "+node2+"}), p = shortestPath((f)-[]-(t)) RETURN p"
	
	return path
		
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
