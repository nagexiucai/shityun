import db
import virt
import web

db.Model.initialize()
virt.Domain.initialize()
web.HTTPServ.initialize()
web.HTTPServ.clear()
virt.Domain.clear()
db.Model.clear()
