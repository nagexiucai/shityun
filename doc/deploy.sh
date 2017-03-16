if [ ! -d "/etc/shityun"]; then
  mkdir -p /etc/shityun
fi

cp -f ../src/virt/default-image.txt /etc/shityun
cp -f ../src/virt/default-network.xml /etc/shityun
cp -f ../src/virt/default-vm.xml /etc/shityun
