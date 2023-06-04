import json
import Gns3ServerApi as api
import conf_telnet_CE as confCE
import conf_telnet_PE as confPE
import conf_telnet_P as confP
import ihm as ihm
import re
import os
import time

def main():
    print("## Creating initial configs ##")
    ihm.createInitialConfigsJSON()
    ihm.createOrUpdateRoutersJSON()

    print("## Creating lab ##")
    lab = api.createLab()  # Lab object

    print("## Creating nodes ##")
    nodes = api.create_router()  # List of nodes (objects)

    print("Creating links")
    api.create_link_v2(lab, nodes, conf_file)  # Creates links
    print("Starting nodes")
    lab.start_nodes()
    print("Configuring nodes")
    for node in nodes:
        if re.match("PE[0-9]", node.name):
            print("Configuring " + node.name)
            confPE.initial(node, conf_file)
            #print("Error")

        if re.match("P[0-9]", node.name):
            print("Configuring " + node.name)
            try:
                confP.initial(node, conf_file)
            except:
                print("Error")
        if re.match("CE[0-9]", node.name):
            print("Configuring " + node.name)
            confCE.initial(node, conf_file)


    # Add listener to listen if router is added in GNS3 to configure it


if __name__ == "__main__":
    main()
