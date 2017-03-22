#coding=utf8

import cherrypy
from os.path import abspath, dirname, join as pjoin
import pprint
import db

WEBROOT = abspath(dirname(__file__))

conf = {
    "global": {
        "server.socket_host": "0.0.0.0",
        "server.socket_port": 9527,
        "server.thread_pool": 8
    },
    "/": {
        "tools.sessions.on": True,
        "tools.staticdir.root": WEBROOT
        },
    "/static": {
        "tools.staticdir.on": True,
        "tools.staticdir.dir": WEBROOT
        },
    "/favicon.ico": {
        "tools.staticfile.on": True,
        "tools.staticfile.filename": pjoin(WEBROOT, "img", "favicon.ico")
        }
}

class HTTPServ(): #TODO: html cache

    @staticmethod
    def initialize():
        cherrypy.quickstart(HTTPServ(), "/", conf)

    @staticmethod
    def clear():
        print "shutdown http service"

    @cherrypy.expose
    def index(self):
        try:
            with open(pjoin(WEBROOT, "html/index.html")) as html:
                return html.read()
        except IOError:
            return "404"

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
        return "404"

    @cherrypy.expose
    def courses(self, cid=None):
        pprint.pprint(cherrypy.request.params)
        if cid is None:
            try:
                with open(pjoin(WEBROOT, "html/courses.html")) as html:
                    return html.read()
            except IOError:
                return "404"
        else:
            with db.Course() as course:
                result = course.select("UUID='%s'" % cid)
                if result:
                    return `[getattr(result[0], attrname) for attrname in db.Course.listfileds()]`

    @cherrypy.expose
    def labscene(self, mode=None, vid=None):
        try:
            with open(pjoin(WEBROOT, "html/labscene.html")) as html:
                return html.read()
        except IOError:
            return "404"

if __name__ == "__main__":
    HTTPServ.initialize()
    HTTPServ.clear()
