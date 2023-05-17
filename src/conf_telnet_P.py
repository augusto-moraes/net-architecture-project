import telnetlib
import GNS3_Server_API as api



def initial(node, conf_file):

    HOST = '192.168.33.128'
    PORT = api.get_node_console(node)

    tn = telnetlib.Telnet(HOST, PORT)  # PE1.console)

    name = node.name



    for node in conf_file["P_routers"]:
        if node["hostname"] == name:
            nb_of_interfaces = node["availableInt"]
            tn.write(b"\r\n")
            tn.write(b"\r\n")
            tn.read_until(name.encode('utf-8') + b"#")
            print("finished reading")
            # CONFIG VRF
            tn.write(b"conf t\r\n")
            tn.write(b"no logging monitor\r\n")
            tn.write(b"no logging console\r\n")
            tn.write(b"ip cef\r\n")

            #CONF LOOPBACK
            tn.write(b"int Loopback0\r\n")
            tn.write(b"ip add " + node["loopback0"].encode('utf-8') + b" 255.255.255.255\r\n")
            tn.write(b"ip ospf " + conf_file["OSPF_config"][0]["OSPFprocessId"].encode('utf-8') + b" area " +
                     conf_file["OSPF_config"][0]["OSPFareaCore"].encode('utf-8') + b" secondaries none\r\n")

            # Changes the IP for each int of the node
            for i in range(1, nb_of_interfaces + 1):
                tn.write(b"int " + node["int" + str(i)].encode('utf-8') + b"\r\n")
                tn.write(b"ip add " + node["IP" + node["int" + str(i)]].encode('utf-8') + b" " + node["netmaskCore"].encode('utf-8') + b"\r\n") #ADD when netmaskClient
                tn.write(b"no sh\r\n")
                tn.write(b"ip ospf " + conf_file["OSPF_config"][0]["OSPFprocessId"].encode('utf-8') + b" area " +
                         conf_file["OSPF_config"][0]["OSPFareaCore"].encode('utf-8') + b" secondaries none\r\n")
            tn.write(b"router ospf " + conf_file["OSPF_config"][0]["OSPFprocessId"].encode('utf-8') + b"\r\n")
            tn.write(b"mpls ldp autoconfig\r\n")

            tn.write(b"end\r\n")
            tn.write(b"write mem\r\n")
            tn.write(b"\r\n")
            break
    tn.read_until(name.encode('utf-8') + b"#")
    print("Configuration finished")
    return True

