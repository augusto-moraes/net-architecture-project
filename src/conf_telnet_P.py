import telnetlib
import GNS3_Server_API as api


def initial(node, conf_file):

    HOST = '192.168.33.128'
    PORT = api.get_node_console(node)
    # appel à l'API pour savoir sur quel port est chaque routeur
    tn = telnetlib.Telnet(HOST, PORT)  # PE1.console)

    name = node.name
    tn.write(b"conf t\r\n")
    tn.write(b"ip cef\r\n")
    tn.write(b"mpls ip\r\n")
    tn.write(b"mpls label protocol ldp\r\n")

    # Changes the IP for each int of the node
    for node in conf_file["P_routers"]:
        if node["hostname"] == name:
            nb_of_interfaces = node["availableInt"]

            #CONF LOOPBACK
            tn.write(b"int Loopback0\r\n")
            tn.write(b"ip add " + node["loopback0"].encode('utf-8') + b" 255.255.255.255\r\n")
            tn.write(b"ip ospf " + conf_file["OSPF_config"][0]["OSPFprocessId"].encode('utf-8') + b" area " +
                     conf_file["OSPF_config"][0]["OSPFareaCore"].encode('utf-8') + b" secondaries none\r\n")
            tn.write(b"no sh\r\n")

            for i in range(1, nb_of_interfaces):
                tn.write(b"int " + node["int" + str(i)].encode('utf-8') + b"\r\n")
                tn.write(b"ip address " + node["IP" + node["int" + str(i)]].encode('utf-8') + b" " + node["netmaskCore"].encode('utf-8') + b"\r\n")
                tn.write(b"ip ospf " + conf_file["OSPF_config"][0]["OSPFprocessId"].encode('utf-8') + b" area " + conf_file["OSPF_config"][0]["OSPFareaCore"].encode('utf-8') + b" secondaries none\r\n")
                tn.write(b"no sh\r\n")

            tn.write(b"router ospf" + conf_file["OSPF_config"][0]["OSPFprocessId"].encode('utf-8') + b"\r\n")
            tn.write(b"mpls ldp autoconfig\r\n")



            tn.write(b"exit\r\n")
        tn.write(b"end\r\n")
        break


def ospf(node, conf_file):


    HOST = '192.168.33.128'
    PORT = api.get_node_console(node)
    # appel à l'API pour savoir sur quel port est chaque routeur
    tn = telnetlib.Telnet(HOST, PORT)  # PE1.console)

    name = node.name
    tn.write(b"conf t\r\n")
    for node in conf_file["P_routers"]:
        if node["hostname"] == name:
            nb_of_interfaces = node["availableInt"]
            for i in range(1, nb_of_interfaces):
                tn.write(b"int " + node["int" + str(i)].encode('utf-8') + b"\r\n")
                tn.write(b"ip ospf " + conf_file["OSPF_config"][0]["OSPFprocessId"].encode('utf-8') + b" area " + conf_file["OSPF_config"][0]["OSPFareaCore"].encode('utf-8') + b" secondaries none\r\n")
                tn.write(b"router ospf" + conf_file["OSPF_config"][0]["OSPFprocessId"].encode('utf-8') + b"\r\n")
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
    for node in conf_file["P_routers"]:
        if node["hostname"] == name:
            nb_of_interfaces = node["availableInt"]
            for i in range(1, nb_of_interfaces):
                tn.write(b"int " + node["int" + str(i)].encode('utf-8') + b"\r\n")
                tn.write(b"mpls ip\r\n")
                tn.write(b"exit\r\n")
        tn.write(b"end\r\n")
        break