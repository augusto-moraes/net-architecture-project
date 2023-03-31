import jinja2
import json
import os
import GNS3_Server_API

# cas particulier d'un reseau en ligne (  -- P -- ... -- P --  )
#   * nbRP : Nb de router provider (hors PEs, qui seront ajoutés apres)
def generateInfoPs(nbRP): 
    ip_base = "192.168.0."

    data = []
    for routerID in range(1,nbRP+1):
        template = {}
        at_reseau=(routerID-1)*4

        template['hostname'] = 'P'+str(routerID)
        template['loopbackAddress'] = str(routerID)+'.'+str(routerID)+'.'+str(routerID)+'.'+str(routerID)
        
        if routerID != 1:
            template['ipAddressG1'] = ip_base+str(at_reseau-2) #statique pour mask /30
        
        if routerID != nbRP:
            template['ipAddressG2'] = ip_base+str(at_reseau+1) #statique pour mask /30
        
        template['netmask'] = "255.255.255.252" #statique pour mask /30
        template['processId'] = "1"
        template['areaNumber'] = "0"
        
        data.append(template)

    with open("infoPRouterList.json", "w") as jsonFile:
        json.dump(data, jsonFile, indent=4)



# Methode de Boris
def createCfg(project_id, node_id):
    generateInfoPs(2)
    
    template_file_PE = "PE.j2"
    template_file_P = "P.j2"
    json_parameter_file_PE = "infoPE.json"
    json_parameter_file_P = "infoP.json"
    output_directory = "_output"

    # read the contents from the JSON files
    print("Read JSON parameter file...")
    config_parameters_PE = json.load(open(json_parameter_file_PE))
    config_parameters_P = json.load(open(json_parameter_file_P))


    # next we need to create the central Jinja2 environment and we will load
    # the Jinja2 template file (the two parameters ensure a clean output in the
    # configuration file)
    print("Create Jinja2 environment...")
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="."),
                             trim_blocks=True,
                             lstrip_blocks=True)
    template_PE = env.get_template(template_file_PE)
    template_P = env.get_template(template_file_P)

    # we will make sure that the output directory exists
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    # now create the templates
    #i = 0
    #for parameter in config_parameters_PE:
     #   result = template_PE.render(parameter)
      #  f = open(os.path.join("../projects", project_id, "project-files/dynamips", node_id[i], "configs", "i" + str(i) + "_startup-config.cfg"), "w")
       # f.write(result)
        #f.close()
        #i+=1
        #print("Configuration '%s' created..." % (parameter['hostname'] + ".config"))

    #for parameter in config_parameters_P:
        #result = template_P.render(parameter)
        #f = open(os.path.join("../projects", project_id, "project-files/dynamips",node_id[i], "configs", "i" + str(i) + "_startup-config.cfg"), "w")
        #f.write(result)
        #f.close()
        #i+=1
        #print("Configuration '%s' created..." % (parameter['hostname'] + ".config"))
    print("DONE")

#def change_router_config():
#    f = open("project_id.txt", "r")
#    project_id = f.read(-1)
#    f.close()
#    f = open(os.path.join("projects", project_id, "project-files/dynamips",
#                          project_id, "i2_startup-config.cfg"), "w")


def main():
    lab = GNS3_Server_API.create_lab()
    router_list = GNS3_Server_API.create_router(lab, ["PE1", "P1", "P2", "PE2"])
    GNS3_Server_API.create_link(lab, router_list)
    project_id = GNS3_Server_API.get_lab_id(lab)
    node_id = GNS3_Server_API.get_node_id(router_list)
    createCfg(project_id, node_id)

if __name__ == "__main__":
    main()

