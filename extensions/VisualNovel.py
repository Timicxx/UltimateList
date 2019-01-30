import ssl
import socket
import json

class VisualNovelList():
    def __init__(self, website, output_format='.json'):
        self.website = website
        self.output_format = output_format
        self.limit = 10
        
        self.ip = self.website.api_url.split(':')[0]
        self.port = int(self.website.api_url.split(':')[1])
        self.logged_in = False
        self.clientvars = {'protocol': 1, 'clientver': 0.1, 'client': 'UltimatList'}
        self.data_buffer = bytes(1024)
        self.sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.sslcontext.verify_mode = ssl.CERT_REQUIRED
        self.sslcontext.check_hostname = True
        self.sslcontext.load_default_certs()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sslwrap = self.sslcontext.wrap_socket(self.socket, server_hostname=self.ip)
        self.sslwrap.connect((self.ip, self.port))
        self._login()

    def getUserList(self, user_name):
        _user_id = self._send_command('get', "user basic (username~\"%s\")" % user_name)["items"][0]["id"]
        response = self._send_command('get', "vnlist basic (uid=%s)" % _user_id)["items"]
        return response

    def getEntry(self, entry_id):
        response = self._send_command('get', "vn basic,details (id=%d)" % entry_id)
        return response

    def searchEntry(self, search_input, page_number, parameters):
        response = self._send_command('get', "vn basic,details (title~\"%s\") {\"page\": %d}" % (search_input, page_number))
        return response

    def _send_command(self, command, args=None):
        if args:
            final_command = command + ' ' + args + '\x04'
        else:
            final_command = command + '\x04'
        self.sslwrap.sendall(final_command.encode('utf-8'))

        return self._recv_data()

    def _recv_data(self):
        temp = ""
        while True:
            self.data_buffer = self.sslwrap.recv(1024)

            if '\x04' in self.data_buffer.decode('utf-8', 'ignore'):
                temp += self.data_buffer.decode('utf-8', 'ignore')
                temp.replace("\\", '')
                break
            else:
                temp += self.data_buffer.decode('utf-8', 'ignore')
                self.data_buffer = bytes(1024)
        temp = temp.replace('\x04', '')
        if 'ok' in temp and not self.logged_in:
            self.logged_in = True
            return temp
        else:
            return json.loads(str(temp.split(' ', 1)[1]))

    def _login(self):
        self._send_command('login', json.dumps(self.clientvars))

