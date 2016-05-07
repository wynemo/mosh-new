My ISP ban SSH, but mosh will use SSH to start up mosh-server.

So I use a web server to start mosh-server, then use mosh-client to connect it, 

the whole process does not need SSH.

Web server use http basic authorization, you can edit password and username in 

config.json.

mosh.config is a nginx config example.

run 'python wsgi.py', it will listen 8080, then nginx will proxy it.



another approach:

run remote-cmd.py in server

run mosh.sh in command line

