import telnetlib
import GNS3_Server_API as api


def initial(node, conf_file):

    HOST = '192.168.33.128'
    PORT = api.get_node_console(node)

    tn = telnetlib.Telnet(HOST, PORT)

    name = node.name

    # Changes the IP for each int of the node
    for node in conf_file["CE_routers"]:
        if node["hostname"] == name:
            nb_of_interfaces = node["availableInt"]
            tn.write(b"\r\n")
            tn.write(b"\r\n")
            tn.read_until(name.encode('utf-8') + b"#")
            print("finished reading")
            tn.write(b"conf t\r\n")
            tn.write(b"no logging monitor\r\n")
            tn.write(b"no logging console\r\n")
            tn.write(b"ip cef\r\n")

            # CONF LOOPBACK
            tn.write(b"int Loopback0\r\n")
            tn.write(b"ip add " + node["loopback0"].encode('utf-8') + b" 255.255.255.255\r\n")

            # Changes the IP for each int of the node
            for i in range(1, nb_of_interfaces + 1):
                tn.write(b"int " + node["int" + str(i)].encode('utf-8') + b"\r\n")
                tn.write(b"ip add " + node["IP" + node["int" + str(i)]].encode('utf-8') + b" " + node["netmaskClient"].encode('utf-8') + b"\r\n")  # ADD when netmaskClient
                tn.write(b"no sh\r\n")

            # CONF eBGP
            tn.write(b"router bgp " + conf_file["BGP_config"][0]["BGPClientAAS"].encode('utf-8') + b"\r\n")
            tn.write(b"bgp log-neighbor-changes\r\n")
            tn.write(b"neighbor " + node["IPg1/0"].encode('utf-8') + b" remote-as " + conf_file["BGP_config"][0][
                "BGPClientBAS"].encode('utf-8') + b"\r\n")

            tn.write(b"address-family ipv4 unicast\r\n")
            tn.write(b"network " + node["LANNetwork"].encode('utf-8') + b"\r\n")
            for router in conf_file["PE_routers"]:
                if node["hostname"] == router["connectedTo"]:
                    tn.write(b"neighbor " + router["IP" + router["VrfInt"]].encode('utf-8') + b" activate\r\n")
                    tn.write(b"neighbor " + router["IP" + router["VrfInt"]].encode('utf-8') + b" allow-as in 1\r\n")
                    tn.write(b"neighbor " + router["IP" + router["VrfInt"]].encode('utf-8') + b"prefix-list PREFIXES-IN in\r\n")
                    tn.write(b"neighbor " + router["IP" + router["VrfInt"]].encode('utf-8') + b"prefix-list PREFIXES-OUT out\r\n")
            tn.write(b"exit-address-family\r\n")

            for VRF in conf_file["VRF_config"]:
                for CE in conf_file["vrfMembers"]:
                    if VRF["vrfName"] == CE["vrfMember"]:
                        tn.write(b"ip prefix-list PREFIXES-IN seq 5 permit " + CE["LANNetwork"] + b"\r\n")
            tn.write(b"ip prefix-list PREFIXES-OUT seq 5 permit " + node["LANNetwork"] + b"\r\n")

            tn.write(b"end\r\n")
            tn.write(b"write mem\r\n")
            tn.write(b"\r\n")
            break
    tn.read_until(name.encode('utf-8') + b"#")
    print("Configuration finished")
    return True