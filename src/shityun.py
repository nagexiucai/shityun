#!/usr/bin/env python
#coding=utf-8

import db
import virt
import web
import atexit

atexit.register(web.HTTPServ.clear)
atexit.register(virt.Domain.clear)
atexit.register(db.Model.clear)
db.Model.initialize()
virt.Domain.initialize()
web.HTTPServ.initialize()
