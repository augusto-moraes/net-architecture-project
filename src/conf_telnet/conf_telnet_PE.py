import telnetlib
#from gns3fy import Gns3Connector

#server = Gns3Connector(url="http://localhost:3080", user="admin", cred="1234")


HOST = 'localhost'
#user = input("Enter your Username: ")
#password = getpass.getpass()
#enablepassword = getpass.getpass()

#appel à l4API pour savoir sur quel port est chaque routeur
tn = telnetlib.Telnet(HOST,5001)#PE1.console)

def initial(router_name, conf_file):
	#tn.read_until(b"P1>")
	#tn.write(b"enable\n")
	#tn.write(enablepassword.encode('ascii') + b"\n")

	tn.write(b"conf t\r\n")
	interfaces = []
	ips = []
	for int, ip in interfaces, ips:
		tn.write(b"int" + str(int) + "\r\n")
		tn.write(b"ip add" + str(ip) + "255.255.255.0\r\n")
		tn.write(b"no sh\r\n")
		tn.write(b"exit\r\n")
	tn.write(b"int Loopback0\r\n")
	tn.write(b"ip add 4.4.4.4 255.255.255.255\r\n")
	tn.write(b"no sh\r\n")
	tn.write(b"end\r\n")
	
def ospf(router_name, conf_file):
	tn.write(b"conf t\r\n")
	tn.write(b"int gigabitEthernet 1/0\r\n")
	tn.write(b"ip ospf 1 area 0 secondaries none\r\n")
	tn.write(b"router ospf 1\r\n")
	tn.write(b"mpls ldp autoconfig\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"int Loopback0\r\n")
	tn.write(b"ip ospf 1 area 0 secondaries none\r\n")
	tn.write(b"end\r\n")
	

def ldp(router_name, conf_file):
	tn.write(b"conf t\r\n")
	tn.write(b"mpls ip\r\n")
	tn.write(b"mpls label protocol ldp\r\n")
	tn.write(b"int gigabitEthernet 1/0\r\n")
	tn.write(b"mpls ip\r\n")
	tn.write(b"end\r\n")


def ibgp(router_name, conf_file):
	tn.write(b"conf t\r\n")
	tn.write(b"int gigabitEthernet 1/0\r\n")
	tn.write(b"router bgp 100\r\n")
	tn.write(b"neighbor 1.1.1.1 remote-as 100\r\n")
	tn.write(b"neighbor 1.1.1.1 update-source Loopback0\r\n")
	tn.write(b"address-family ipv4 unicast\r\n")
	tn.write(b"neighbor 1.1.1.1 activate\r\n")
	tn.write(b"neighbor 1.1.1.1 next-hop-self\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"address-family vpnv4 unicast\r\n")
	tn.write(b"neighbor 1.1.1.1 activate\r\n")
	tn.write(b"neighbor 1.1.1.1 send-community extended\r\n")
	tn.write(b"end\r\n")
	
def vrf(router_name, conf_file):
	tn.write(b"conf t\r\n")
	tn.write(b"ip vrf RED\r\n")
	tn.write(b"rd 4:4\r\n")
	tn.write(b"route-target export 4:4\r\n")
	tn.write(b"route-target import 4:4\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"ip vrf RED2\r\n")
	tn.write(b"rd 5:5\r\n")
	tn.write(b"route-target export 5:5\r\n")
	tn.write(b"route-target import 5:5\r\n")
	tn.write(b"exit\r\n")
	
	tn.write(b"int gigabitEthernet 2/0\r\n")
	tn.write(b"ip vrf forwarding RED\r\n")
	tn.write(b"ip add 192.168.101.1 255.255.255.0\r\n")
	tn.write(b"no sh\r\n")
	tn.write(b"router bgp 100\r\n")
	tn.write(b"address-family ipv4 vrf RED\r\n")
	tn.write(b"neighbor 192.168.101.2 remote-as 300\r\n")
	tn.write(b"neighbor 192.168.101.2 activate\r\n")
	tn.write(b"exit\r\n")
	
	tn.write(b"int gigabitEthernet 3/0\r\n")
	tn.write(b"ip vrf forwarding RED\r\n")
	tn.write(b"ip add 192.168.201.1 255.255.255.0\r\n")
	tn.write(b"no sh\r\n")
	tn.write(b"router bgp 100\r\n")
	tn.write(b"address-family ipv4 vrf RED2\r\n")
	tn.write(b"neighbor 192.168.201.2 remote-as 200\r\n")
	tn.write(b"neighbor 192.168.201.2 activate\r\n")
	tn.write(b"end\r\n")
