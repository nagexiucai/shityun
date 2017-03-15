#coding=utf8

import sqlite3

class Model(object):
    connect = None #singleton
    @staticmethod
    def initialize():
        if Model.connect is None:
            print "open connect"
            Model.connect = sqlite3.connect(":memory:")
    @staticmethod
    def clear():
        if Model and Model.connect is not None:
            print "close connect"
            Model.connect.close()
            Model.connect = None
    cursor = None
    def __enter__(self):
        print self.__class__.__name__, "enter"
        if self.cursor is None:
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
        this = self.cursor.execute(sql)
        if sql.startswith("SELECT"):
            return this.fetchall()
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

class User(Model):
    Nickname = None
    PhoneNumber = None
    Realname = None
    Sex = None
    Birthday = None
    IDNumber = None
    Organization = None
    Major = None
    Key = None
    Role = None

class VM(Model):
    Name = None
    Timestamp = None #%Y-%m-%d %H:%M:%S, datetime.datetime, now.strftime, strptime
    Owner = None #User
    Status = None
    OS = None
    CPU = None
    Block = None #Image
    IFace = None #Net
    Graphic = None #VNC

if __name__ == "__main__":
    Model.initialize()
    print Model.listfileds()
    print User.listfileds()
    print VM.listfileds()
    with User() as user:
        print user.connect, user.cursor
        print user.create()
        print user.insert(('Birthday', 'IDNumber', 'Key', 'Major', 'Nickname', 'Organization', 'PhoneNumber', 'Realname', 'Role', 'Sex'))
        print user.select("Birthday='Birthday'")
    with VM() as vm:
        print vm.connect, vm.cursor
        print vm.create()
        print vm.insert(('Block', 'CPU', 'Graphic', 'IFace', 'Name', 'OS', 'Owner', 'Status', 'Timestamp'))
        print vm.select("Block='Block'")
    Model.clear()
