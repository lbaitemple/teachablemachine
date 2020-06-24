from http.server import BaseHTTPRequestHandler
import cgi, os, json, glob, os
from pred import classify
import base64

######
##   echo username:passwd | base64 >> passwd.txt
##   curl -u lbai:test -F "picture=@pic2.jpg" -F "model=@keras_model.h5" -F "class=@labels.txt" http://localhost:8080
######


class GetHandler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def check(self, auth):
        with open('passwd.txt') as f:
            if auth in f.read():
                return True
            else:
                return False



    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'})

#        response = get(self.address_string(), auth = ('user', 'pass'))
        bauth =self.headers['Authorization'].split(' ')[1]
        if (self.check(bauth)):
            auth=base64.b64decode(bauth.encode('ascii')).decode('ascii')
            user, passwd = auth.split(':')
            #auth=base64.b64encode(bauth.encode('utf-8')).decode()
            if not os.path.exists(user):
#                print('making dir')
                os.makedirs(user)


            try:
                for fi in form.keys():
                    upfilecontent = form[fi].value
                    filename = os.path.join(user, form[fi].filename)
#                    print(filename)

                    if upfilecontent:
                        fout = open(filename, 'wb')
                        fout.write(upfilecontent)
                        fout.close()
            except:
                pass


            files =['class', 'model', 'picture']
            data={}
            for fi in files:
                if fi not in form:
                    data[fi] = None
                else:
                    data[fi] = os.path.join(user, form[fi].filename)

            name = classify(folder=user, ifile=data['picture'], mfile=data['model'], lfile=data['class'])
            self.send_response(200)
            self.send_header("Content-type", 'application/json')
            self.end_headers()
            message=''+ name +'\n'
            self.wfile.write(message.encode(encoding='utf_8'))
        else:
            self.send_response(200)
            self.send_header("Content-type", 'application/json')
            self.end_headers()
            message='not authenticated \n'
            self.wfile.write(message.encode(encoding='utf_8'))


if __name__ == '__main__':
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    from http.server import HTTPServer
    server = HTTPServer(('', 8080), GetHandler)
    print('Starting server, use <Ctrl + F2> to stop')
    server.serve_forever()
