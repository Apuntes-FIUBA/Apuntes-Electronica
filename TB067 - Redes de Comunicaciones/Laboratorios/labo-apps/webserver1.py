from http.server import BaseHTTPRequestHandler, HTTPServer

# Definimos el manejador de solicitudes HTTP


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Responder con el código de estado 200 (OK)
        self.send_response(200)
        # Definir el tipo de contenido como texto
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        # Enviar la respuesta al cliente
        mensaje = "<html><body><h1>Hola, Laboratorio!!!</h1><p>¡Bienvenido al servidor web!</p></body></html>"
        self.wfile.write(mensaje.encode('utf-8'))

# Configuración del servidor


IP = '192.168.1.40'


def run():
    # Crear un servidor en todas las interfaces {IP} y el puerto 8000
    servidor_direccion = (IP, 8000)
    httpd = HTTPServer(servidor_direccion, RequestHandler)
    print(f"Servidor corriendo en http://{IP}:8000")

    # Ejecutar el servidor
    httpd.serve_forever()


if __name__ == '__main__':
    run()
