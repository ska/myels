import socket  
s=socket.socket( socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.1.35", 20000))

strr = s.recv(128)
print "Ack: " + strr

s.send("*#1*21##")
strr = s.recv(128)
print "stato: " + strr


if strr[3] != "0":
	print "acceso: " + strr[3]
	s.send("*1*0*21##")
else:
	print "spento: " + strr[3]
	s.send("*1*1*21##")
strr = s.recv(128)
print "Ack: " + strr

s.send("*#1*21##")
strr = s.recv(128)
print "stato: " + strr
