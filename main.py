from socketserver import TCPServer
from TCPHandler import Handler
from Setting import HOST, PORT


server = TCPServer((HOST, PORT), Handler)
server.serve_forever()
