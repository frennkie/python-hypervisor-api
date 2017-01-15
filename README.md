# python-hypervisor-api
Here you can find some Python scripts and includes to interract with VMWare vCenter or ESX hosts and oVirt virtualization hosts.

## VMware Guest OS identifier

https://pubs.vmware.com/vsphere-60/index.jsp?topic=%2Fcom.vmware.wssdk.apiref.doc%2Fvim.vm.GuestOsDescriptor.GuestOsIdentifier.html

## Next Step -> Cobbler integration

https://dash1218.gitbooks.io/use-cobbler-and-ansible-for-deploying-cloudstack/content/chapter7/section7.1.html

* https://fedorahosted.org/cobbler/wiki/CobblerXmlrpc


import xmlrpclib



## Prerequisites
### to use the scripts for VMWare vCenter or ESX
- install python-pip: (`sudo yum -y install python-pip` or similar for your distro)
- pip install pysphere (`sudo pip install pysphere`)

more information on my blog: [Create a new virtual machine in Vsphere with Python, Pysphere and the VMWare API](http://jensd.be/?p=370)

## How to use:
- edit the defaults in deploy_vm.py
- create a textfile similar to example_ovirt.txt or example_vmware.txt
- execute `deploy_vm.py <name of the vm-definitions file>`

Multiple VM-definitions can be givin in one file.
The deploy_vm is rather quick/dirty, feel free to improve it :)
