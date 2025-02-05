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
    # Configurando o servidor HTTP
    server_address = ('localhost', 4443)
    httpd = http.server.HTTPServer(server_address, HTTPSRequestHandler)
    
    # Definindo o contexto SSL
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='server.pem', keyfile='server.key')

    # Ativando o modo de segurança
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    print("Servidor HTTPS rodando em https://localhost:4443")
    httpd.serve_forever()

def run_client():
    # Configurando o cliente HTTPS
    url = "https://localhost:4443"
    try:
        #response = requests.get(url, verify=False)  # Desativa a verificação SSL (somente para testes!)
        response = requests.get(url, verify="server.pem")
        print("Resposta do servidor:", response.text)
    # Tratamento de exceção para certificado inválido
    except SSLError:
        raise ValueError("Certificado inválido! Conexão rejeitada.")
        sys.exit(1)
    
# openssl req -x509 -newkey rsa:2048 -keyout server.key -out server.pem -days 365 -nodes

# Criando um certificado autoassinado
server_thread = threading.Thread(target=run_server)
server_thread.daemon = True
server_thread.start()
time.sleep(2)  # Espera o servidor iniciar
run_client()