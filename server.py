import socket
import threading
import handler
import db
import time

PORT=23415
NRCONS=100
HANDLER_DELAY=10
MAXCONNS=300


class Base(threading.Thread):
	vlock = threading.Lock()
	chunks=[]
	id=0
	conns = 0 

class Handler(Base):
	chunks = []	

	def run(self):
		con = db.get_con()		
		trans = con.transaction()
		while 1:
			Base.vlock.acquire()
			print "Hanlding harvested data"
			self.chunks = Base.chunks
			Base.chunks = []
			Base.vlock.release()
			for chunk in self.chunks:
				handler.handle(chunk,trans)
			if self.chunks: print "COMMITED"
			self.chunks=[]
			time.sleep(HANDLER_DELAY)			

class serv(Base):
	chunk=''
	def __init__(self,clnsock):
		threading.Thread.__init__(self)
		self.clnsock=clnsock
		self.myid=Base.id
		Base.id+=1


	def run(self):
		while 1:
			k = self.clnsock.recv(1024)
			if k == '': break
			self.chunk+=k
		self.clnsock.shutdown(socket.SHUT_RDWR)
		self.clnsock.close()
		Base.vlock.acquire()
		Base.chunks.append(self.chunk)
		Base.conns -= 1
		Base.vlock.release()	
		print "%s\n________\n" % self.chunk


lstn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lstn.bind(('',PORT))
lstn.listen(MAXCONNS)
h = Handler()
h.start()
conns=0
while 1:
	threading.Lock().acquire()
	conns = Base.conns
	threading.Lock().release
	print "conns running %d" % conns

	if conns < MAXCONNS:
		(clnt,ap) = lstn.accept()
		s = serv(clnt)
		threading.Lock().acquire()
		Base.conns += 1
		threading.Lock().release
		s.start()	
	else:
		print "DELAY!"
		time.sleep(HANDLER_DELAY)
