#coding=utf8

import sqlite3
from datetime import datetime

def timestamp():
    return datetime.now()

def time2text(time):
    return time.strftime("%Y-%m-%d %H:%M:%S")

def text2time(text):
    return datetime.strptime(text, "%Y-%m-%d %H:%M:%S")

def _row_factory(cursor, row):
    d = {}
    for i, col in enumerate(cursor.description):
        d[col[0]] = row[i]
    return d

class Model(object):
    connect = None #singleton
    @staticmethod
    def initialize():
        if Model.connect is None:
            print "open connect"
            Model.connect = sqlite3.connect(":memory:", check_same_thread=False)
            Model.connect.row_factory = _row_factory
            with User() as user: user.create(); user.insert(User.__Default__)
            with VM() as vm: vm.create(); vm.insert(VM.__Default__)
            with Course() as course: course.create(); course.insert(Course.__Default__)
    @staticmethod
    def clear():
        if Model and Model.connect is not None:
            print "close connect"
            Model.connect.close()
            Model.connect = None
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    cursor = None
    def __enter__(self):
        print self.__class__.__name__, "enter"
        if self.cursor is None and self.connect is not None:
            print "open cursor of", self.__class__.__name__
            self.cursor = self.connect.cursor()
        return self #must return a instance
    def __exit__(self, type_, value, traceback):
        print type_, value, traceback
        print self.__class__.__name__, "exit"
        if self.cursor is not None:
            print "close cursor of", self.__class__.__name__
            self.cursor.close()
            self.cursor = None
    __ = "RESERVED"
    @classmethod
    def listfileds(cls):
        attributes = dir(cls)
        return attributes[:attributes.index('__')]
    def execute(self, sql):
        if self.cursor is None:
            print "please initialize model"
            return
        this = self.cursor.execute(sql)
        if sql.startswith("SELECT"):
            result = []
            for record in this.fetchall():
                result.append(self.__class__(**record))
            return result
        elif sql.startswith("CREATE") or sql.startswith("INSERT") or sql.startswith("UPDATE") or sql.startswith("DELETE"):
            return Model.connect.commit()
        else:
            raise Exception("invalid sql")
    def create(self):
        return self.execute("CREATE TABLE %s (%s);" % (self.__class__.__name__, ", ".join(map(lambda f: "%s TEXT" % f, self.listfileds()))))
    def insert(self, values):
        return self.execute("INSERT INTO %s VALUES %s;" % (self.__class__.__name__, values))
    def update(self):pass
    def select(self, expression):
        return self.execute("SELECT * FROM %s WHERE %s" % (self.__class__.__name__, expression))
    def delete(self):pass
    Name = None
    UUID = None #TODO: repetition
    CreateTimestamp = None #%Y-%m-%d %H:%M:%S, datetime.datetime, now.strftime, strptime
    UpdateTimestamp = None
    DeleteTimestamp = None

class User(Model): #UUID IS PERSON'S IDNUMBER
    __Default__ = ('2017-03-15', '2017-03-15 00:00:00', 'NULL', 'wechat$nagexiucai', 'HASH-ShitYun', 'nagexiucai@qq.com', 'BioMedical-Engineering', 'ShitYun', '翔云', 'THISSTACK.COM', 'NULL', 'God', 'Unknown', '95279527-9527-9527-9527-952795279527', '2017-03-15 09:52:27')
    Nickname = None
    PhoneNumber = None
    Mailbox = None #nagexiucai@qq.com
    Sex = None
    Birthday = None #%Y-%m-%d
    Organization = None
    Major = None
    Key = None
    Role = None
    IM = None #vender$account, such as "wechat$nagexiucai"

class VM(Model): #UUID IS VM'S UUID
    __Default__ = ('default.img', '2', time2text(timestamp()), 'NULL', '-1|yes|shityun', 'default|NULL', 'shityun', 'win7x86-64', '95279527-9527-9527-9527-952795279527', 'closed', '95279527-9527-9527-9527-952795279527', time2text(timestamp()))
    Owner = None #User.UUID
    Status = None
    OS = None
    CPU = None
    Block = None #Image
    IFace = None #Net
    Graphic = None #VNC

class Course(Model): #UUID IS TEXTBOOK'S NUMBER
    __Default__ = ('95279527-9527-9527-9527-952795279527', time2text(timestamp()), 'NULL', '95279527-9527-9527-9527-952795279527', 'A', 'Linux Introduction', 'Linux', '95279527-9527-9527-9527-952795279527', time2text(timestamp()))
    Level = None
    Author = None #User.UUID
    Tag = None
    Environment = None #VM.UUIDs

if __name__ == "__main__":
    timestamp = timestamp()
    text = time2text(timestamp)
    time = text2time(text)
    print timestamp, text, time
    Model.initialize()
    print Model.listfileds()
    print User.listfileds()
    print VM.listfileds()
    print Course.listfileds()
    with User() as user:
        print user.connect, user.cursor
        print user.insert(('Birthday', 'CreateTimestamp', 'DeleteTimestamp', 'IM', 'Key', 'Mailbox', 'Major', 'Name', 'Nickname', 'Organization', 'PhoneNumber', 'Role', 'Sex', 'UUID', 'UpdateTimestamp'))
        print user.select("'DO'=='DO'")
    with VM() as vm:
        print vm.connect, vm.cursor
        print vm.insert(('Block', 'CPU', 'CreateTimestamp', 'DeleteTimestamp', 'Graphic', 'IFace', 'Name', 'OS', 'Owner', 'Status', 'UUID', 'UpdateTimestamp'))
        print vm.select("'DO'=='DO'")
    with Course() as course:
        print course.connect, course.cursor
        print course.insert(('Author', 'CreateTimestamp', 'DeleteTimestamp', 'Environment', 'Level', 'Name', 'Tag', 'UUID', 'UpdateTimestamp'))
        print course.select("'DO'=='DO'")
    Model.clear()
