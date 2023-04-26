import telnetlib
import GNS3_Server_API as api


def initial(node, conf_file):

    HOST = '192.168.33.128'
    PORT = api.get_node_console(node)
    # appel à l'API pour savoir sur quel port est chaque routeur
    tn = telnetlib.Telnet(HOST, PORT)  # PE1.console)

    name = node.name
    tn.write(b"conf t\r\n")
    # Changes the IP for each int of the node
    for node in conf_file["CE_routers"]:
        if node["hostname"] == name:
            nb_of_interfaces = node["availableInt"]
            for i in range(1, nb_of_interfaces):
                tn.write(b"int " + node["int" + str(i)].encode('utf-8') + b"\r\n")
                tn.write(b"ip add " + node["IP" + node["int" + str(i)]].encode('utf-8') + b" " + node["netmaskClient"].encode('utf-8') + b"\r\n")
                tn.write(b"no sh\r\n")
                tn.write(b"exit\r\n")

            tn.write(b"int Loopback0\r\n")
            tn.write(b"ip add " + node["loopback0"].encode('utf-8') + b" 255.255.255.255\r\n")
            tn.write(b"no sh\r\n")
            tn.write(b"exit\r\n")
        tn.write(b"end\r\n")
        break


def ebgp(node, conf_file):

    HOST = '192.168.33.128'
    PORT = api.get_node_console(node)
    # appel à l'API pour savoir sur quel port est chaque routeur
    tn = telnetlib.Telnet(HOST, PORT)  # PE1.console)

    name = node.name
    tn.write(b"conf t\r\n")
    # Changes the IP for each int of the node
    for node in conf_file["CE_routers"]:
        if node["hostname"] == name:
            tn.write(b"int" + node["int1"].encode('utf-8') + b"\r\n")       # g1/0 ARBITRAIRE
            tn.write(b"router bgp 200\r\n")
            tn.write(b"neighbor 192.168.201.1 remote-as 100\r\n")
            tn.write(b"address-family ipv4\r\n")
            tn.write(b"network " + node["loopback0"].encode('utf-8') + b" mask 255.255.255.255\r\n")
            tn.write(b"neighbor 192.168.201.1 activate\r\n")
            tn.write(b"end\r\n")
