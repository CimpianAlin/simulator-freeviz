import Image
import ImageDraw
import math
import handler
import db

class Dnode:
	def __init__(self,node):
		self.id = node.id

def idsin(idslist,dnodes):
	il = idslist
	dnpair = []
	for dn in dnodes:
		if dn.id in il:
			il.remove(dn.id)
			dnpair.append(dn)	

		if not (il):
			return dnpair


	return []	

def gen(con):
	nodes = handler.get_activenodes(con)
	node_pairs = list(db.NodePair.select())
	im = Image.new('P',(600,600))
	da = ImageDraw.Draw(im)
#	da.fill='red'


#big circle


#CENTER IS 220x220
#rad is 240
	da.rectangle((0,0,im.size[0],im.size[1]),fill='white')
#da.chord((20,20,460,460),0,360, outline='red'   )
	r = im.size[0]/2 - 20
	u = 10

	da.chord((20, 20, im.size[0] -20, im.size[1] - 20), 0, 360, outline='black')

#for i in nodes:

	dnodes = []
	for node in nodes:
		dnode = Dnode(node)
		j =  float(node.location)
		x = int(r * math.cos(j*2*math.pi))
		y = int(r * math.sin(j*2*math.pi))
		da.chord((x - 10 + im.size[0]/2, y-10 + im.size[1]/2,x+10+im.size[0]/2,y+10+im.size[1]/2),0,360,outline='green')
		dnode.x = int(x)
		dnode.y = int(y)
		dnodes.append(dnode)

	for node_pair in node_pairs:
		dnpair =  idsin([node_pair.node1.id, node_pair.node2.id], dnodes)
		if len(dnpair) == 2:
			da.line((dnpair[0].x + im.size[0]/2,dnpair[0].y+im.size[1]/2,
				dnpair[1].x + im.size[0]/2,dnpair[1].y + im.size[1]/2),fill='green')
			

	im.save('/tmp/outputc.png','PNG')