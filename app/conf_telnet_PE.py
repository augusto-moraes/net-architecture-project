import telnetlib
import GNS3_Server_API as api



def initial(node, conf_file):

    HOST = '192.168.33.128'
    PORT = api.get_node_console(node)

    tn = telnetlib.Telnet(HOST, PORT)  # PE1.console)

    name = node.name

    for node in conf_file["PE_routers"]:
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
            tn.write(b"ip vrf " + conf_file["VRF_config"][0]["vrfName"].encode('utf-8') + b"\r\n")
            tn.write(b"rd " + conf_file["VRF_config"][0]["RD"].encode('utf-8') + b"\r\n")
            tn.write(b"route-target export " + conf_file["VRF_config"][0]["RTexport"].encode('utf-8') + b"\r\n")
            tn.write(b"route-target import " + conf_file["VRF_config"][0]["RTimport"].encode('utf-8') + b"\r\n")

            #CONF LOOPBACK
            tn.write(b"int Loopback0\r\n")
            tn.write(b"ip add " + node["loopback0"].encode('utf-8') + b" 255.255.255.255\r\n")
            tn.write(b"ip ospf " + conf_file["OSPF_config"][0]["processId"].encode('utf-8') + b" area " +
                     conf_file["OSPF_config"][0]["OSPFareaCore"].encode('utf-8') + b"\r\n")

            # Changes the IP for each int of the node
            for i in range(1, nb_of_interfaces + 1):
                tn.write(b"int " + node["int" + str(i)].encode('utf-8') + b"\r\n")
                for vrfInt in node["vrfInt"]:
                    if node["int" + str(i)] == vrfInt:
                        tn.write(b"ip vrf forwarding " + conf_file["VRF_config"][0]["vrfName"].encode('utf-8') + b"\r\n")
                        tn.write(b"ip add " + node["IP" + node["int" + str(i)]].encode('utf-8') + b" " + node[
                            "netmaskClient"].encode('utf-8') + b"\r\n")
                        tn.write(b"no sh\r\n")
                        break

                tn.write(b"ip add " + node["IP" + node["int" + str(i)]].encode('utf-8') + b" " + node["netmaskCore"].encode('utf-8') + b"\r\n")
                tn.write(b"no sh\r\n")
                tn.write(b"ip ospf network point-to-point\r\n")
                tn.write(b"ip ospf " + conf_file["OSPF_config"][0]["processId"].encode('utf-8') + b" area " +
                         conf_file["OSPF_config"][0]["OSPFareaCore"].encode('utf-8') + b"\r\n")

            tn.write(b"router ospf " + conf_file["OSPF_config"][0]["processId"].encode('utf-8') + b"\r\n")
            tn.write(b"router-id " + node["loopback0"].encode('utf-8') + b"\r\n")
            tn.write(b"network " + node["LinkNetwork"].encode('utf-8') + b" " + node["LinkNetworkNetmask"].encode('utf-8') + b" area " + conf_file["OSPF_config"][0]["OSPFareaCore"].encode('utf-8') + b"\r\n")
            tn.write(b"mpls ldp autoconfig\r\n")

            #BGP CONFIG
            tn.write(b"router bgp " + conf_file["BGP_config"][0]["BGPCoreAS"].encode('utf-8') + b"\r\n")
            tn.write(b"bgp log-neighbor-changes\r\n")
            tn.write(b"bgp"  + node["loopback0"].encode('utf-8') + b"\r\n")
            for router in conf_file["PE_routers"]:
                if router["hostname"] != name:
                    tn.write(b"neighbor " + router["loopback0"].encode('utf-8') + b" remote-as " + conf_file["BGP_config"][0]["BGPCoreAS"].encode('utf-8') + b"\r\n")
                    #tn.read_until(name.encode('utf-8') + b"(config-router)#")
                    tn.write(b"neighbor " + router["loopback0"].encode('utf-8') + b" update-source " + b"loopback0" + b"\r\n")

                    tn.write(b"address-family ipv4 unicast\r\n")
                    tn.write(b"neighbor " + router["loopback0"].encode('utf-8') + b" activate\r\n")
                    tn.write(b"exit-address-family\r\n")

                    tn.write(b"address-family vpnv4 unicast\r\n")
                    tn.write(b"neighbor " + router["loopback0"].encode('utf-8') + b" activate\r\n")
                    tn.write(b"neighbor " + router["loopback0"].encode('utf-8') + b" send-community extended\r\n")
                    tn.write(b"exit-address-family\r\n")

            for router in conf_file["CE_routers"]:
                if router["hostname"] == node["connectedTo"]:
                    tn.write(b"address-family ipv4 vrf " + conf_file["VRF_config"][0]["vrfName"].encode('utf-8') + b"\r\n")
                    tn.write(b"redistribute connected\r\n")
                    tn.write(b"neighbor " + router["IPg1/0"].encode('utf-8') + b" remote-as " + conf_file["BGP_config"][0]["BGPClientAAS"].encode('utf-8') + b"\r\n")
                    tn.write(b"neighbor " + router["IPg1/0"].encode('utf-8') + b"activate\r\n")
                    tn.write(b"neighbor " + router["IPg1/0"].encode('utf-8') + b"next-hop-self\r\n")
                    tn.write(b"neighbor " + router["IPg1/0"].encode('utf-8') + b"prefix-list " + conf_file["VRF_config"][0]["vrfName"].encode('utf-8') + b"-PREFIXES-IN in\r\n")
                    tn.write(b"neighbor " + router["IPg1/0"].encode('utf-8') + b"prefix-list " + conf_file["VRF_config"][0]["vrfName"].encode('utf-8') + b"-PREFIXES-OUT out\r\n")
                    tn.write(b"exit-address-family\r\n")

                    tn.write(b"ip prefix-list " + conf_file["VRF_config"][0]["vrfName"].encode('utf-8') + b"-PREFIXES-IN seq 5 permit " + router["LANNetwork"] + b"\r\n")
                tn.write(b"ip prefix-list " + conf_file["VRF_config"][0]["vrfName"].encode('utf-8') + b"-PREFIXES-OUT seq 5 permit " + router["LANNetwork"] + b"\r\n")


            tn.write(b"end\r\n")
            tn.write(b"write mem\r\n")
            tn.write(b"\r\n")
            break
    tn.read_until(name.encode('utf-8') + b"#")
    print("Configuration finished")
    return True

