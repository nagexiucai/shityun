#!/usr/bin/env sh

yum install -y epel-release
yum install -y qemu-kvm*
yum install -y libvirt
yum install -y virt-install
yum install -y git
yum install -y python-
pip install --upgrade pip
pip install cherrypy
pip install websockify

git clone http://github.com/nagexiucai/shityun.git

if [ ! -d "/etc/shityun" ]; then
  mkdir -p /etc/shityun
fi

if [ ! -d "/var/log/shityun" ]; then
  mkdir -p /var/log/shityun
fi

cp -f shityun/src/virt/default-image.txt /etc/shityun
cp -f shityun/src/virt/default-network.xml /etc/shityun
cp -f shityun/src/virt/default-vm.xml /etc/shityun
