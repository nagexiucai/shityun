#coding=utf8

import cherrypy
from os import getcwd
from os.path import join
import pprint

class MyCloud():

    @cherrypy.expose
    def index(self):
        try:
            with open('./html/index.html') as html:
                return html.read()
        except:
            return '404'

    @cherrypy.expose
    def register(self, account, password):
        return None

    @cherrypy.expose
    def login(self, account, password):
        return "account: %s, password: %s" % (account, password)

    @cherrypy.expose
    def logout(self, account):
        return "account: %s" % account

    @cherrypy.expose
    def manager(self):
        return '404'

    @cherrypy.expose
    def courses(self, cid=None):
        pprint.pprint(cherrypy.request.params)
        return 'courses id: %s' % cid

    @cherrypy.expose
    def labscene(self, mode=None, vid=None):
        return '404'

conf = {
    "/": {
        "tools.sessions.on": True,
        "tools.staticdir.root": getcwd()
        },
    "/static": {
        "tools.staticdir.on": True,
        "tools.staticdir.dir": getcwd()
        },
    "/favicon.ico": {
        "tools.staticfile.on": True,
        "tools.staticfile.filename": join(getcwd(), "img", "favicon.ico")
        }
}

cherrypy.quickstart(MyCloud(), "/", conf)
