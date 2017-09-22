#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Time    : 2017/9/22 17:11
# @Author  : Bob
# @Website : www.nagexiucai.com
# @E-Mail  : me@nagexiucai.com
# @Summary : 基于pyinotify和rsync命令的同步方案。
# pyinotify version: 0.9.6

# TODO: 针对文件更新频繁的仓库，可以把调用rsync命令的操作放入队列

cfg = {
    "slaves": ["192.168.1.2#ma"],
    "source": "/home/bob/*"
}
cmd = "rsync -av {source} simple@{ip}::{module} --password-file=/etc/rsync.secrets"

from pyinotify import WatchManager, Notifier, ProcessEvent
from pyinotify import IN_DELETE, IN_CLOSE_WRITE
import signal
import threading
import sys
import subprocess

class MyProcessEvent(ProcessEvent):
    def process_IN_DELETE(self, event):
        self.do(event)
    def process_IN_CLOSE_WRITE(self, event):
        self.do(event)
    def do(self, event):
        def invoke(cmd):
            subprocess.Popen(cmd, shell=True).communicate()
        source = cfg.get("source")
        for slaves in cfg.get("slaves"):
            ip, module = slaves.split("#")
            threading.Thread(target=invoke, args=(cmd.format(source=source, ip=ip, module=module),)).start()

class MyNotify(object):
    def __init__(self, path):
        self.wm = WatchManager()
        mask = IN_DELETE|IN_CLOSE_WRITE
        self.notifier = Notifier(self.wm, MyProcessEvent())
        self.wm.add_watch(path, mask, rec=True)
    def run(self):
        signal.signal(signal.SIGHUP, lambda: sys.exit(0))
        while True:
            try:
                self.notifier.process_events()
                if self.notifier.check_events():
                    self.notifier.read_events()
            except Exception:
                self.notifier.stop()
                break

m = MyNotify('/home/bob')
m.run()
