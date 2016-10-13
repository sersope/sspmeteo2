from bottle import route, run, template, static_file
import socket
import sys, getopt

data_server = 'localhost'
data_server_port = 1234
web_server_port = 8080

# Rutas del servidor
@route('/static/<filename>')
def send_static(filename):
    return static_file(filename, root='./static')

@route('/sspmeteo2')
def hello():
    datos = ['0' for i in range(16)]
    try:
        s = socket.socket()
        s.connect((data_server, data_server_port))
        s.send('GET_DATOS'.encode())
        datos = s.recv(256).decode().split(',')
        s.close()
    except:
        datos[0]= "ERROR en el acceso al servidor de datos."
    return template('sspmeteo2', datos=datos)
    
    
# Parse argumentos de linea de comandos
usage = 'Usage: -p <web server port> -S <data server> -P <data server port>'
try:
    opts, args = getopt.getopt(sys.argv[1:],"hp:S:P:")
except getopt.GetoptError:
    print(usage)
    sys.exit(2)
if  len(opts) == 0 and len(args) > 0:
    print(usage)
    sys.exit()
for opt, arg in opts:
    if opt == '-h':
        print(usage)
        sys.exit()
    elif opt == '-p':
        web_server_port = arg
    elif opt == '-S':
        data_server = arg
    elif opt == '-P':
        data_server_port = arg
    else:
        print(usage)
        sys.exit()
        
print('Data server: ', data_server + ':' + str(data_server_port))
# Lanza el servidor
run(host='', port=web_server_port)