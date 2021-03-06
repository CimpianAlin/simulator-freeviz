import db
import handler
#returns the list of the form 
#[({'identity':'dasdas','location':'0.31231'},{:,:}),...]
def get(trans):
	data=[]
	connections = list(db.NodePair.select(connection=trans))


	nodes = list(handler.get_activenodes(trans))
	lastgoodver = db.getLastGoodVer(trans)

	goodnodes=[]
	for node in nodes:
		if node.lastGoodVersion >= lastgoodver:
			goodnodes.append(node.id)
		else:
			print("%s is bad!" % node.name)

	#print "good nodes are:"
	#print goodnodes
	if not goodnodes:
		print "NO GOOD NODES!!!"

	for conn in connections:
		if conn.node1.id in goodnodes and conn.node2.id in goodnodes:

			left={}
			right={}
			left['identity'] = conn.node1.identity
			left['location'] = conn.node1.location
	
			right['identity'] = conn.node2.identity
			right['location'] = conn.node2.location
			data.append( (left, right) )

		else:
			print ('Droping conn: %s-%s' % (conn.node1.name,conn.node2.name) )
			
	return data
		


