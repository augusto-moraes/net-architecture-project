import telnetlib

# from gns3fy import Gns3Connector

# server = Gns3Connector(url="http://localhost:3080", user="admin", cred="1234")


HOST = 'localhost'
# user = input("Enter your Username: ")
# password = getpass.getpass()
# enablepassword = getpass.getpass()

# appel à l4API pour savoir sur quel port est chaque routeur
tn = telnetlib.Telnet(HOST, 5002)  # PE1.console)


def initial(router_name, conf_file):
    # tn.read_until(b"P1>")
    # tn.write(b"enable\n")
    # tn.write(enablepassword.encode('ascii') + b"\n")
    tn.write(b"conf t\r\n")
    tn.write(b"int gigabitEthernet 1/0\r\n")
    tn.write(b"ip add 192.168.1.2 255.255.255.0\r\n")
    tn.write(b"no sh\r\n")
    tn.write(b"exit\r\n")
    tn.write(b"conf t\r\n")
    tn.write(b"int gigabitEthernet 2/0\r\n")
    tn.write(b"ip add 192.168.2.1 255.255.255.0\r\n")
    tn.write(b"no sh\r\n")
    tn.write(b"exit\r\n")
    tn.write(b"int Loopback0\r\n")
    tn.write(b"ip add 2.2.2.2 255.255.255.255\r\n")
    tn.write(b"no sh\r\n")
    tn.write(b"end\r\n")


def ospf(router_name, conf_file):
    tn.write(b"conf t\r\n")
    tn.write(b"int gigabitEthernet 1/0\r\n")
    tn.write(b"ip ospf 1 area 0 secondaries none\r\n")
    tn.write(b"exit\r\n")
    tn.write(b"int gigabitEthernet 2/0\r\n")
    tn.write(b"ip ospf 1 area 0 secondaries none\r\n")
    tn.write(b"exit\r\n")
    tn.write(b"int Loopback0\r\n")
    tn.write(b"ip ospf 1 area 0 secondaries none\r\n")
    tn.write(b"router ospf 1\r\n")
    tn.write(b"mpls ldp autoconfig\r\n")
    tn.write(b"end\r\n")


def ldp(router_name, conf_file):
    tn.write(b"conf t\r\n")
    tn.write(b"mpls ip\r\n")
    tn.write(b"mpls label protocol ldp\r\n")
    tn.write(b"int gigabitEthernet 1/0\r\n")
    tn.write(b"mpls ip\r\n")
    tn.write(b"int gigabitEthernet 2/0\r\n")
    tn.write(b"mpls ip\r\n")
    tn.write(b"end\r\n")
