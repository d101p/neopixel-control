#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import cgi
import time
import serial

PORT_NUMBER = 8000

class myHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path=="/":
            self.path="/index.html"
        try:
            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype='image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True

            if sendReply == True:
                #Open the static file requested and send it
                f = open(curdir + sep + self.path) 
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    def do_POST(self):
        if self.path=="/":
            content_len = int(self.headers.getheader('content-length', 0))
            colour = self.rfile.read(content_len)
            print 'Sending 0X{} to Arduino...'.format(colour)
            ser.write("0X" + colour)
            ser.write("\n")
            response = ser.readline()
            print response
            self.send_response(200)
            self.end_headers()
            return          

try:
        ser = serial.Serial("/dev/ttyAMA0", 9600, timeout=1)

	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print 'Shutting down the web server...'
	server.socket.close()
	print 'Closing serial port...'
        ser.close()
