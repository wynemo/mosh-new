import json
import re
import base64
import subprocess
import StringIO
import sys
import web

CONFIG_FILE = 'config.json'

urls = (
    '/', 'Index',
    '/login', 'Login'
)

app = web.application(urls, globals())

allowed = ()

with open(CONFIG_FILE, 'rb') as f:
    o = json.load(f)
    for i in o['allowed']:
        allowed += ((i['user'], i['pwd']), )


def run_and_print_char(args, handler):
    pipe = subprocess.Popen(args, bufsize=0,
                            shell=False,
                            stdout=subprocess.PIPE,
                            stderr=sys.stderr)
    while 1:
        # use read(1), can get wget process bar like output
        s = pipe.stdout.read(1)
        if s:
            handler.write(s)
        if pipe.returncode is None:
            pipe.poll()
        else:
            s = pipe.stdout.read()
            if s:
                handler.write(s)
            break
    if not 0 == pipe.returncode:
        return False
    return True


def custom_redirect(url):
    if web.ctx.env.get('HTTP_X_FORWARDED_PROTO', 'http') == 'https':
        raise web.seeother('https://' + web.ctx.host + url)
    else:
        raise web.seeother(url) 


class Index:
    def GET(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            output = StringIO.StringIO()
            run_and_print_char('mosh-server', output)
            s = output.getvalue()
            output.close()
            return s
        else:
            custom_redirect('/login')


class Login:
    def GET(self):
        auth = web.ctx.env.get('HTTP_AUTHORIZATION')
        authreq = False
        if auth is None:
            authreq = True
        else:
            auth = re.sub('^Basic ', '', auth)
            username, password = base64.decodestring(auth).split(':')
            if (username, password) in allowed:
                custom_redirect('/')
            else:
                authreq = True
        if authreq:
            web.header('WWW-Authenticate', 'Basic realm="Auth example"')
            web.ctx.status = '401 Unauthorized'
            return

if __name__ == '__main__':
    app.run()
 
