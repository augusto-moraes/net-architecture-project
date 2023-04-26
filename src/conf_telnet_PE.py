import telnetlib
import GNS3_Server_API as api


def initial(node, conf_file):

    HOST = '192.168.33.128'
    PORT = api.get_node_console(node)
    # appel à l'API pour savoir sur quel port est chaque routeur
    tn = telnetlib.Telnet(HOST, PORT)  # PE1.console)

    name = node.name
    tn.read_until(name.encode('utf-8') + b"#")
    print("finished reading")
    tn.write(b"conf t\r\n")
    # Changes the IP for each int of the node
    for node in conf_file["PE_routers"]:
        if node["hostname"] == name:
            nb_of_interfaces = node["availableInt"]
            for i in range(1, nb_of_interfaces):
                tn.write(b"int " + node["int" + str(i)].encode('utf-8') + b"\r\n")
                tn.write(b"ip add " + node["IP" + node["int" + str(i)]].encode('utf-8') + b" " + node["netmaskCore"].encode('utf-8') + b"\r\n") #ADD when netmaskClient
                tn.write(b"no sh\r\n")
                tn.write(b"exit\r\n")

            tn.write(b"int Loopback0\r\n")
            tn.write(b"ip add " + node["loopback0"].encode('utf-8') + b" 255.255.255.255\r\n")
            tn.write(b"no sh\r\n")
            tn.write(b"exit\r\n")
        tn.write(b"end\r\n")
        # WRITE MEM
        break


def ospf(node, conf_file):

    HOST = '192.168.33.128'
    PORT = api.get_node_console(node)
    # appel à l'API pour savoir sur quel port est chaque routeur
    tn = telnetlib.Telnet(HOST, PORT)  # PE1.console)

    name = node.name
    tn.write(b"conf t\r\n")
    for node in conf_file["PE_routers"]:
        if node["hostname"] == name:
            nb_of_interfaces = node["availableInt"]
            for i in range(1, nb_of_interfaces):
                tn.write(b"int " + node["int" + str(i)].encode('utf-8') + b"\r\n")
                tn.write(b"ip osp f" + conf_file["OSPF_config"][0]["OSPFprocessId"].encode('utf-8') + b" area " + conf_file["OSPF_config"][0]["OSPFareaCore"].encode('utf-8') + b" secondaries none\r\n")
                tn.write(b"router ospf " + conf_file["OSPF_config"][0]["OSPFprocessId"].encode('utf-8') + b"\r\n")
                tn.write(b"mpls ldp autoconfig\r\n")
                tn.write(b"exit\r\n")
                tn.write(b"int Loopback0\r\n")
                tn.write(b"ip ospf " + conf_file["OSPF_config"][0]["OSPFprocessId"].encode('utf-8') + b" area " + conf_file["OSPF_config"][0]["OSPFareaCore"].encode('utf-8') + b" secondaries none\r\n")
                tn.write(b"exit\r\n")
        tn.write(b"end\r\n")
        break


def ldp(node, conf_file):

    HOST = '192.168.33.128'
    PORT = api.get_node_console(node)
    # appel à l'API pour savoir sur quel port est chaque routeur
    tn = telnetlib.Telnet(HOST, PORT)  # PE1.console)

    name = node.name
    tn.write(b"conf t\r\n")
    tn.write(b"mpls ip\r\n")
    tn.write(b"mpls label protocol ldp\r\n")
    for node in conf_file["PE_routers"]:
        if node["hostname"] == name:
            nb_of_interfaces = node["availableInt"]
            for i in range(1, nb_of_interfaces):
                tn.write(b"int " + node["int" + str(i)].encode('utf-8') + b"\r\n")
                tn.write(b"mpls ip\r\n")
                tn.write(b"exit\r\n")
        tn.write(b"end\r\n")
        break


def ibgp(node, conf_file):

    HOST = '192.168.33.128'
    PORT = api.get_node_console(node)
    # appel à l'API pour savoir sur quel port est chaque routeur
    tn = telnetlib.Telnet(HOST, PORT)  # PE1.console)

    name = node.name
    tn.write(b"conf t\r\n")
    for node in conf_file["PE_routers"]:
        if node["hostname"] == name:
            tn.write(b"router bgp " + conf_file["BGP_config"][0]["BGPCoreAS"].encode('utf-8') + b"\r\n")
            for router in conf_file["PE_routers"]:
                tn.write(b"neighbor " + router["loopback0"].encode('utf-8') + b" remote-as " + conf_file["BGP_config"][0]["BGPCoreAS"].encode('utf-8') + b"\r\n")
                tn.write(b"neighbor " + router["loopback0"].encode('utf-8') + b" update-source " + node["loopback0"].encode('utf-8') + b"\r\n")
            tn.write(b"address-family ipv4 unicast\r\n")
            for router in conf_file["PE_routers"]:
                tn.write(b"neighbor " + router["loopback0"].encode('utf-8') + b" activate\r\n")     # NEEDS CHECK
                tn.write(b"neighbor " + router["loopback0"].encode('utf-8') + b" next-hop-self\r\n")# NEEDS CHECK
                tn.write(b"exit\r\n")
            tn.write(b"address-family vpnv4 unicast\r\n")
            for router in conf_file["PE_routers"]:
                tn.write(b"neighbor " + router["loopback0"].encode('utf-8') + b" activate\r\n")                # NEEDS CHECK
                tn.write(b"neighbor " + router["loopback0"].encode('utf-8') + b" send-community extended\r\n") # NEEDS CHECK
        tn.write(b"end\r\n")
        break


def vrf(node, conf_file):

    HOST = '192.168.33.128'
    PORT = api.get_node_console(node)
    # appel à l'API pour savoir sur quel port est chaque routeur
    tn = telnetlib.Telnet(HOST, PORT)  # PE1.console)

    name = node.name
    tn.write(b"conf t\r\n")
    for node in conf_file["PE_routers"]:
        if node["hostname"] == name:
            tn.write(b"conf t\r\n")
            tn.write(b"ip vrf " + conf_file["VRF_config"][0]["vrfName"].encode('utf-8') + b"\r\n")
            tn.write(b"rd " + conf_file["VRF_config"][0]["RD"].encode('utf-8') + b"\r\n")
            tn.write(b"route-target export " + conf_file["VRF_config"][0]["RTexport"].encode('utf-8') + b"\r\n")
            tn.write(b"route-target import " + conf_file["VRF_config"][0]["RTimport"].encode('utf-8') + b"\r\n")
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
