from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Responder con el código de estado 200 (OK)
        self.send_response(200)
        # Definir el tipo de contenido como texto HTML
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        # Obtener direcciones IP del cliente y del servidor
        ip_cliente = self.client_address[0]
        ip_servidor = self.server.server_address[0]

        # Crear el mensaje de respuesta
        mensaje = f"""
        <html>
        <body>
        <h1>Información de Conexión</h1>
        <p>Dirección IP del Cliente: {ip_cliente}</p>
        <p>Dirección IP del Servidor: {ip_servidor}</p>
        </body>
        </html>
        """

        # Enviar la respuesta
        self.wfile.write(mensaje.encode('utf-8'))

# Configuración del servidor seguro


def run(servidor_direccion, puerto, certfile, keyfile):
    # Crear servidor HTTP
    httpd = HTTPServer((servidor_direccion, puerto), RequestHandler)

    # Configurar SSL
    contexto_ssl = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    contexto_ssl.load_cert_chain(certfile=certfile, keyfile=keyfile)
    httpd.socket = contexto_ssl.wrap_socket(httpd.socket, server_side=True)

    print(f"Servidor HTTPS corriendo en https://{servidor_direccion}:{puerto}")

    # Ejecutar el servidor
    httpd.serve_forever()


if __name__ == '__main__':
    # Cambia '0.0.0.0' a la dirección IP de tu interfaz física si es necesario.
    servidor_direccion = '192.168.1.40'
    puerto = 443

    # Archivos de certificado y clave generados con OpenSSL
    certfile = 'cert.pem'
    keyfile = 'key.pem'

    run(servidor_direccion, puerto, certfile, keyfile)
