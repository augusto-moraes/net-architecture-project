import json
import GNS3_Server_API as api
import conf_telnet_CE as confCE
import conf_telnet_PE as confPE
import conf_telnet_P as confP
import re
import os
import time

def main():
    router_constellation = ["PE1", "PE2", "PE3", "PE4", "PE5", "PE6", "PE7", "PE8", "P1", "P2", "P3", "P4", "P5", "P6",
                            "P7"]

    test_file = "test_config.json"
    conf_file = json.load(open(test_file))
    print("Creating lab")
    lab = api.create_lab("test_lab3")  # Lab object
    print("Creating nodes")
    nodes = api.create_router(lab, conf_file)  # List of nodes (objects)
    print("Creating links")
    api.create_link_v2(lab, nodes, conf_file)  # Creates links
    time.sleep(5)
    lab.start_nodes
    print("Starting nodes")
    time.sleep(100)
    print("Configuring nodes")
    for node in nodes:
        if re.match("PE\s[0-9]", node.name):
            print("Configuring PEs")
            confPE.initial(node, conf_file)
            confPE.ospf(node, conf_file)
            confPE.ldp(node, conf_file)
            confPE.ibgp(node, conf_file)
            confPE.vrf(node, conf_file)
        if re.match("P\s[0-9]", node.name):
            print("Configuring Ps")
            confP.initial(node, conf_file)
            confP.ospf(node, conf_file)
            confP.ldp(node, conf_file)
        if re.match("CE\s[0-9]", node.name):
            print("Configuring CEs")
            confCE.initial(node, conf_file)
            confCE.ebgp(node, conf_file)

    # Add listener to listen if router is added in GNS3 to configure it


if __name__ == "__main__":
    main()
