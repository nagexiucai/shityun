#coding=utf8

try:
    import libvirt
except ImportError:
    print "please install libvirt"
import random
import uuid
import time

TEMPLATE = "/etc/shityun/default-vm.xml"

def macgen():
    return ":".join(["%02x" % int(random.uniform(0,256)) for _ in range(6)])

class Config(object):
    default = {"Name":None,
               "UUID":None,
               "Image":"/etc/shityun/default-image.qcow2",
               "MEM":262144,
               "MAC":None,
               "Net":"default",
               "VNCPORT":"-1",
               "VNCAUTO":"yes",
               "VNCPW":"shityun"}
    def verify(self):
        if self.UUID is None:
            self.UUID = str(uuid.uuid1())
        if self.Name is None:
            self.Name = self.UUID
        if self.MAC is None:
            self.MAC = macgen()
    def __init__(self, **kwargs):
        self.__dict__.update(Config.default)
        self.__dict__.update(kwargs)
        self.verify()

def xmlgen(config):
    with open(TEMPLATE) as t:
        return t.read() % config.__dict__

#libvirt-python-binding
class Domain(object):
    virt = None
    @staticmethod
    def initialize():
        if Domain.virt is None:
            Domain.virt = libvirt.open('qemu:///system')
    @staticmethod
    def clear():
        if Domain.virt is not None:
            Domain.virt.close()
            Domain.virt = None
    domain = None
    def __init__(self, config):
        self.config = config
        self.domain = self._find() or self._define()
    def __del__(self):pass
    def _find(self):
        return self.virt.lookupByName(self.config.Name)
    def _define(self):
        return self.virt.defineXML(xmlgen(self.config))
    def undefine(self): self.domain.undefine()
    def start(self): self.domain.create()
    def shutdown(self): self.domain.shutdown()
    def destroy(self): self.domain.destroy()
    def suspend(self):pass
    def reboot(self):pass

#virsh-command-pipe

if __name__ == "__main__":
    config = Config(Name="xiang")
    Domain.initialize()
    domain = Domain(config)
    domain.start()
    time.sleep(60*5)
    domain.destroy()
    Domain.clear()
