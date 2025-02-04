import http.server
import ssl
import requests
import socket
from requests.exceptions import SSLError
import threading
import time

class HTTPSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Conexao segura estabelecida via HTTPS!')

def run_server():
    server_address = ('localhost', 4443)
    httpd = http.server.HTTPServer(server_address, HTTPSRequestHandler)
    
    # Usando SSLContext ao invés de wrap_socket
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='server.pem', keyfile='server.key')

    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    print("Servidor HTTPS rodando em https://localhost:4443")
    httpd.serve_forever()

def run_client():
    url = "https://localhost:4443"
    try:
        response = requests.get(url, verify="server.pem")
        print("Resposta do servidor:", response.text)
    except SSLError:
        raise ValueError("Certificado inválido! Conexão rejeitada.")
        sys.exit(1)
    #response = requests.get(url, verify=False)  # Desativa a verificação SSL (somente para testes!)

# openssl req -x509 -newkey rsa:2048 -keyout server.key -out server.pem -days 365 -nodes

server_thread = threading.Thread(target=run_server)
server_thread.daemon = True
server_thread.start()
time.sleep(2)  # Espera o servidor iniciar
run_client()