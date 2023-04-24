import telnetlib
import GNS3_Server_API as api


def initial(node, conf_file):

    HOST = '192.168.33.128'
    PORT = api.get_node_console()
    # appel à l'API pour savoir sur quel port est chaque routeur
    tn = telnetlib.Telnet(HOST, PORT)  # PE1.console)

    name = node.name
    tn.write(b"conf t\r\n")
    # Changes the IP for each int of the node
    for node in conf_file["PE_routers"]:
        if node["hostname"] == name:
            nb_of_interfaces = node["availableInt"]
            for i in range(len(nb_of_interfaces)):
                tn.write(b"int" + bytes(node["int" + str(i)]) + b"\r\n")
                tn.write(b"ip add" + bytes(node["IP" + node["int" + str(i)]]) + bytes(node["netmask" + str(i)]) + b"\r\n")
                tn.write(b"no sh\r\n")
                tn.write(b"exit\r\n")

            tn.write(b"int Loopback0\r\n")
            tn.write(b"ip add" + bytes(node["loopback0"]) + b"255.255.255.255\r\n")
            tn.write(b"no sh\r\n")
            tn.write(b"exit\r\n")
        tn.write(b"end\r\n")
        break


def ospf(node, conf_file):

    HOST = '192.168.33.128'
    PORT = api.get_node_console()
    # appel à l'API pour savoir sur quel port est chaque routeur
    tn = telnetlib.Telnet(HOST, PORT)  # PE1.console)

    name = node.name
    tn.write(b"conf t\r\n")
    for node in conf_file["PE_routers"]:
        if node["hostname"] == name:
            nb_of_interfaces = node["availableInt"]
            for i in range(len(nb_of_interfaces)):
                tn.write(b"int" + bytes(node["int" + str(i)]) + b"\r\n")
                tn.write(b"ip ospf" + bytes(conf_file["OSPF_config"]["OSPFprocessId"]) + b"area" + bytes(conf_file["OSPF_config"]["OSPFareaCore"]) + b"secondaries none\r\n")
                tn.write(b"router ospf" + bytes(conf_file["OSPF_config"]["OSPFprocessId"]) + b"\r\n")
                tn.write(b"mpls ldp autoconfig\r\n")
                tn.write(b"exit\r\n")
                tn.write(b"int Loopback0\r\n")
                tn.write(b"ip ospf" + bytes(conf_file["OSPF_config"]["OSPFprocessId"]) + b"area" + bytes(conf_file["OSPF_config"]["OSPFareaCore"]) + b"secondaries none\r\n")
                tn.write(b"exit\r\n")
        tn.write(b"end\r\n")
        break


def ldp(node, conf_file):

    HOST = '192.168.33.128'
    PORT = api.get_node_console()
    # appel à l'API pour savoir sur quel port est chaque routeur
    tn = telnetlib.Telnet(HOST, PORT)  # PE1.console)

    name = node.name
    tn.write(b"conf t\r\n")
    tn.write(b"mpls ip\r\n")
    tn.write(b"mpls label protocol ldp\r\n")
    for node in conf_file["PE_routers"]:
        if node["hostname"] == name:
            nb_of_interfaces = node["availableInt"]
            for i in range(len(nb_of_interfaces)):
                tn.write(b"int" + bytes(node["int" + str(i)]) + b"\r\n")
                tn.write(b"mpls ip\r\n")
                tn.write(b"exit\r\n")
        tn.write(b"end\r\n")
        break


def ibgp(node, conf_file):

    HOST = '192.168.33.128'
    PORT = api.get_node_console()
    # appel à l'API pour savoir sur quel port est chaque routeur
    tn = telnetlib.Telnet(HOST, PORT)  # PE1.console)

    name = node.name
    tn.write(b"conf t\r\n")
    for node in conf_file["PE_routers"]:
        if node["hostname"] == name:
            tn.write(b"router bgp" + bytes(conf_file["BGP_config"]["BGPCoreAS"]) + b"\r\n")
            for router in conf_file["PE_routers"]:
                tn.write(b"neighbor" + bytes(router["loopback0"]) + b"remote-as" + bytes(conf_file["BGP_config"]["BGPCoreAS"]) + b"\r\n")
                tn.write(b"neighbor" + bytes(router["loopback0"]) + b"update-source" + bytes(node["loopback0"]) + b"\r\n")
            tn.write(b"address-family ipv4 unicast\r\n")
            for router in conf_file["PE_routers"]:
                tn.write(b"neighbor" + bytes(router["loopback0"]) + b"activate\r\n")     # NEEDS CHECK
                tn.write(b"neighbor" + bytes(router["loopback0"]) + b"next-hop-self\r\n")# NEEDS CHECK
                tn.write(b"exit\r\n")
            tn.write(b"address-family vpnv4 unicast\r\n")
            for router in conf_file["PE_routers"]:
                tn.write(b"neighbor" + bytes(router["loopback0"]) + b"activate\r\n")                # NEEDS CHECK
                tn.write(b"neighbor" + bytes(router["loopback0"]) + b"send-community extended\r\n") # NEEDS CHECK
        tn.write(b"end\r\n")
        break


def vrf(node, conf_file):

    HOST = '192.168.33.128'
    PORT = api.get_node_console()
    # appel à l'API pour savoir sur quel port est chaque routeur
    tn = telnetlib.Telnet(HOST, PORT)  # PE1.console)

    name = node.name
    tn.write(b"conf t\r\n")
    for node in conf_file["PE_routers"]:
        if node["hostname"] == name:
            tn.write(b"conf t\r\n")
            tn.write(b"ip vrf" + conf_file["VRF_config"]["vrfName"] + b"\r\n")
            tn.write(b"rd" + conf_file["VRF_config"]["RD"] + b"\r\n")
            tn.write(b"route-target export" + conf_file["VRF_config"]["RTexport"] + b"\r\n")
            tn.write(b"route-target import" + conf_file["VRF_config"]["RTimport"] + b"\r\n")
            tn.write(b"exit\r\n")
            #tn.write(b"ip vrf RED2\r\n")
            #tn.write(b"rd 5:5\r\n")
            #tn.write(b"route-target export 5:5\r\n")
            #tn.write(b"route-target import 5:5\r\n")
            #tn.write(b"exit\r\n")

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
