#! /usr/bin/env python
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink, Link, Intf
from mininet.log import setLogLevel
from subprocess import Popen, PIPE
import time
import os

if'__main__'==__name__:
	os.system('mn -c')
	setLogLevel('info')
	net = Mininet(link=TCLink)
	key = "net.mptcp.mptcp_enabled"
	value = 0
	p = Popen("sysctl -w %s=%s" %(key,value), shell=True, stdout=PIPE, stderr=PIPE)
	stdout, stderr = p.communicate()
	print("stdout=",stdout,"stderr=",stderr)

	## Add Host
	h1 = net.addHost('h1')
	h2 = net.addHost('h2')
	
	## Add Router
	r1 = net.addHost('r1')
	r2 = net.addHost('r2')
	r3 = net.addHost('r3')
	r4 = net.addHost('r4')

	## Configure Link
	net.addLink(h1,r1,max_queue=100,use_htb=True,intfName1='h1-eth0',intfName2='r1-eth0',cls = TCLink,bw=1)
	net.addLink(h1,r2,max_queue=100,use_htb=True,intfName1='h1-eth1',intfName2='r2-eth1',cls = TCLink,bw=1)
	net.addLink(h2,r3,max_queue=100,use_htb=True,intfName1='h2-eth0',intfName2='r3-eth0',cls = TCLink,bw=1)	
	net.addLink(h2,r4,max_queue=100,use_htb=True,intfName1='h2-eth1',intfName2='r4-eth1',cls = TCLink,bw=1)
	net.addLink(r1,r3,max_queue=100,use_htb=True,intfName1='r1-eth1',intfName2='r3-eth1',cls = TCLink,bw=0.5)
	net.addLink(r1,r4,max_queue=100,use_htb=True,intfName1='r1-eth2',intfName2='r4-eth2',cls = TCLink,bw=1)
	net.addLink(r2,r3,max_queue=100,use_htb=True,intfName1='r2-eth2',intfName2='r3-eth2',cls = TCLink,bw=1)
	net.addLink(r2,r4,max_queue=100,use_htb=True,intfName1='r2-eth0',intfName2='r4-eth0',cls = TCLink,bw=0.5)

	net.build()

	#h1, h2, r1, r2, r3, r4 = net.get('h1','h2','r1','r2','r3','r4')

	## Configure IP 

	##HostA
	h1.cmd("ifconfig h1-eth0 192.168.0.1/24 netmask 255.255.255.0")
	h1.cmd("ifconfig h1-eth1 192.168.5.2/24 netmask 255.255.255.0")

	##HostB
	h2.cmd("ifconfig h2-eth0 192.168.2.2/24 netmask 255.255.255.0")
	h2.cmd("ifconfig h2-eth1 192.168.3.1/24 netmask 255.255.255.0")

	##R1
	r1.cmd("ifconfig r1-eth0 192.168.0.2/24 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth1 192.168.1.1/24 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth2 192.168.7.1/24 netmask 255.255.255.0")
	r1.cmd("sysctl net.ipv4.ip_forward=1")

	##R2
	r2.cmd("ifconfig r2-eth0 192.168.4.2/24 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth1 192.168.5.1/24 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth2 192.168.6.2/24 netmask 255.255.255.0")
	r2.cmd("sysctl net.ipv4.ip_forward=1")
	##R3
	r3.cmd("ifconfig r3-eth0 192.168.2.1/24 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth1 192.168.1.2/24 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth2 192.168.6.1/24 netmask 255.255.255.0")
	r3.cmd("sysctl net.ipv4.ip_forward=1")
	
	##R4
	r4.cmd("ifconfig r4-eth0 192.168.4.1/24 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth1 192.168.3.2/24 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth2 192.168.7.2/24 netmask 255.255.255.0")
	r4.cmd("sysctl net.ipv4.ip_forward=1")
	
	## Configure Routing Table
	
	##HostA
	h1.cmd("ip rule add from 192.168.0.1 table 1")
	h1.cmd("ip rule add from 192.168.5.2 table 2")
	h1.cmd("ip route add 192.168.0.0/24 dev h1-eth0 link table 1")	
	h1.cmd("ip route add default via 192.168.0.2 dev h1-eth0 table 1")
	h1.cmd("ip route add 192.168.5.0/24 dev h1-eth1 table 2")
	h1.cmd("ip route add default via 192.168.5.1 dev h1-eth1 table 1")
	h1.cmd("ip route add default scope global nexthop via 192.168.0.2 dev h1-eth0")
	h1.cmd("ip route add default scope global nexthop via 192.168.5.1 dev h1-eth1")

	##HostB
	h2.cmd("ip rule add from 192.168.2.2 table 1")
	h2.cmd("ip rule add from 192.168.3.1 table 2")
	h2.cmd("ip route add 192.168.2.0/24 dev h2-eth0 link table 1")
	h2.cmd("ip route add default via 192.168.2.1 dev h2-eth0 table 1")
	h2.cmd("ip route add 192.168.3.0/24 dev h2-eth1 table 2")
	h2.cmd("ip route add default via 192.168.3.2 dev h2-eth1 table 1")
	h2.cmd("ip route add default scope global nexthop via 192.168.2.1 dev h1-eth0")
	h2.cmd("ip route add default scope global nexthop via 192.168.3.2 dev h1-eth1")

	##R1
	r1.cmd("route add -net 192.168.6.0/24 gw 192.168.1.2")
	r1.cmd("route add -net 192.168.4.0/24 gw 192.168.7.2")
	r1.cmd("route add -net 192.168.2.0/24 gw 192.168.1.2")
	r1.cmd("route add -net 192.168.3.0/24 gw 192.168.7.2")
	r1.cmd("route add -net 192.168.5.0/24 gw 192.168.7.2")
	r1.cmd("route add -net 192.168.5.0/24 gw 192.168.1.2")
	
	##R2
	r2.cmd("route add -net 192.168.1.0/24 gw 192.168.6.1")
	r2.cmd("route add -net 192.168.7.0/24 gw 192.168.4.1")
	r2.cmd("route add -net 192.168.3.0/24 gw 192.168.4.1")
	r2.cmd("route add -net 192.168.2.0/24 gw 192.168.6.1")
	r2.cmd("route add -net 192.168.0.0/24 gw 192.168.4.1")
	r2.cmd("route add -net 192.168.0.0/24 gw 192.168.6.1")

	##R3
	r3.cmd("route add -net 192.168.7.0/24 gw 192.168.1.1")
	r3.cmd("route add -net 192.168.4.0/24 gw 192.168.6.2")
	r3.cmd("route add -net 192.168.3.0/24 gw 192.168.6.2")
	r3.cmd("route add -net 192.168.3.0/24 gw 192.168.1.1")
	r3.cmd("route add -net 192.168.0.0/24 gw 192.168.1.1")
	r3.cmd("route add -net 192.168.5.0/24 gw 192.168.6.2")

	##R4
	r4.cmd("route add -net 192.168.1.0/24 gw 192.168.7.1")
	r4.cmd("route add -net 192.168.6.0/24 gw 192.168.4.2")
	r4.cmd("route add -net 192.168.2.0/24 gw 192.168.7.1")
	r4.cmd("route add -net 192.168.2.0/24 gw 192.168.7.2")
	r4.cmd("route add -net 192.168.0.0/24 gw 192.168.7.1")
	r4.cmd("route add -net 192.168.5.0/24 gw 192.168.4.2")

	time.sleep(2)

	## Run Traffic
	#h2.cmd("iperf -s &")
	h1.cmd("iperf -t 30 -c 192.168.2.2")
	
	CLI(net)
	
	net.stop()
