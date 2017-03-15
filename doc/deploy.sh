mkdir -p /etc/shityun
cp ../src/virt/default-image.qcow2 /etc/shityun
cp ../src/virt/default-network.xml /etc/shityun
cp ../src/virt/default-vm.xml /etc/shityun

virsh net-define /etc/shityun/default-network.xml
virsh net-autostart default
virsh net-start default
