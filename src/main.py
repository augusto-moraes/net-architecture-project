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
    lab = api.create_lab("test_lab")  # Lab object
    print("Creating nodes")
    nodes = api.create_router(lab, conf_file)  # List of nodes (objects)
    print("Creating links")
    api.create_link_v2(lab, nodes, conf_file)  # Creates links
    print("Starting nodes")
    lab.start_nodes()
    #time.sleep(100)   #REPLACE BY WAIT FOR HOSTNAME PROMPT
    print("Configuring nodes")
    for node in nodes:
        if re.match("PE[0-9]", node.name):
            print("Configuring PEs")
            confPE.initial(node, conf_file)
            time.sleep(5)
            confPE.ospf(node, conf_file)
            time.sleep(5)
            confPE.ldp(node, conf_file)
            time.sleep(5)
            confPE.ibgp(node, conf_file)
            time.sleep(5)
            confPE.vrf(node, conf_file)
        if re.match("P[0-9]", node.name):
            print("Configuring Ps")
            confP.initial(node, conf_file)
            confP.ospf(node, conf_file)
            confP.ldp(node, conf_file)
        if re.match("CE[0-9]", node.name):
            print("Configuring CEs")
            confCE.initial(node, conf_file)
            confCE.ebgp(node, conf_file)

    # Add listener to listen if router is added in GNS3 to configure it


if __name__ == "__main__":
    main()
