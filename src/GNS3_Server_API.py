from gns3fy import Gns3Connector, Project, Link, Node

# from tabulate import tabulate

# Script to communicate with the GNS3 server, create labs, routers, links

server = Gns3Connector(url="http://192.168.33.128:3080", user="admin", cred="1234")  # Connection to GNS3 server


def create_lab(project_name):  # create lab and GNS3 project

    lab = Project(name=project_name, connector=server)
    try:
        lab.create()  # Create lab													#OK
    except:
        lab.get()
        lab.open()  # Open existing lab if already exists

    print( "Project id:", lab.project_id)
    return lab


def create_router(lab, config_file):  # Create router (CE, PE, P)

    # server.create_template("test", "local", )
    # for template in server.get_templates():
    #	if "c7200" in template["name"]:
    #		print(f"Template: {template['name']} -- ID: {template['template_id']}")
    # server.get_template_by_name("c7200")
    # server.get_version()

    nodes = []
    router_hostnames = get_router_list(config_file)

    # Creates routers in GNS3 & adds the nodes to a list
    for r in router_hostnames:
        router = Node(
            project_id=lab.project_id,
            connector=server,
            name=r,
            template="c7200")
        router.create()
        nodes.append(router)
    print("Number of nodes:", len(nodes))
    return nodes


def create_matrix():
    matrix = [[0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0], #PE1
              [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0], #PE2
              [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0], #PE3
              [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0], #PE4
              [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0], #PE5
              [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0], #PE6
              [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1], #PE7
              [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1], #PE8
              [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], #P1
              [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0], #P2
              [0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0], #P3
              [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1], #P4
              [0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1], #P5
              [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1], #P6
              [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0]] #P7

    matrix_auto_gen = []
    # JE SAIS PAS COMMENT FAIRE ALED

    return matrix


def create_link(lab, matrix, routers, json_file):  # Create links between routers

    router_interfaces = {}
    for routerP in json_file["P_routers"]:
        router_interfaces[routerP["hostname"]] = routerP["availableInt"]

    for routerPE in json_file["PE_routers"]:
        router_interfaces[routerPE["hostname"]] = routerPE["availableInt"]
    print(router_interfaces)
    for i in range(len(matrix) - 1):
        print("i = ", i)
        ligne_ok = False
        for j in range(len(matrix[i])):
            print("j = ", j)
            if matrix[i][j] != 0:
                counter = 3
                for l in range(j + 1, len(matrix[i]) - 1):
                    print("l = ", l)
                    if matrix[i][l] != 0:
                        links = [
                            dict(node_id=routers["layer" + str(i)][j].node_id,
                                 adapter_number=router_interfaces[matrix[i][j]], port_number=0),
                            dict(node_id=routers["layer" + str(i)][l].node_id,
                                 adapter_number=router_interfaces[matrix[i][l]], port_number=0)
                        ]
                        extra_link = Link(project_id=lab.project_id, connector=server, nodes=links)
                        print(matrix[i][j], ":", router_interfaces[matrix[i][j]], matrix[i][l], ":",
                              router_interfaces[matrix[i][l]])
                        extra_link.create()
                        router_interfaces[matrix[i][j]] -= 1
                        router_interfaces[matrix[i][l]] -= 1
                        counter -= 1
                        break
                for k in range(len(matrix[i + 1])):
                    print("k = ", k)
                    if (matrix[i + 1][k] != 0) & (counter != 0):
                        links = [
                            dict(node_id=routers["layer" + str(i)][j].node_id,
                                 adapter_number=router_interfaces[matrix[i][j]], port_number=0),
                            dict(node_id=routers["layer" + str(i + 1)][k].node_id,
                                 adapter_number=router_interfaces[matrix[i + 1][k]], port_number=0)
                        ]
                        extra_link = Link(project_id=lab.project_id, connector=server, nodes=links)
                        print(matrix[i][j], ":", router_interfaces[matrix[i][j]], matrix[i + 1][k], ":",
                              router_interfaces[matrix[i + 1][k]])
                        extra_link.create()
                        router_interfaces[matrix[i][j]] -= 1
                        router_interfaces[matrix[i + 1][k]] -= 1
                        counter -= 1


def create_link_v2(lab, router_list, json_file):
    matrix = create_matrix()
    routers = []
    router_interfaces = {}

    #
    for router in router_list:
        routers.append(router.name)

    for routerPE in json_file["PE_routers"]:
        router_interfaces[routerPE["hostname"]] = routerPE["availableInt"]

    for routerP in json_file["P_routers"]:
        router_interfaces[routerP["hostname"]] = routerP["availableInt"]

    for i in range(len(matrix)):
        for j in range(i, len(matrix[i])):
            if matrix[i][j] == 1:
                print("links :", routers[i], "->", routers[j])
                links = [
                    dict(node_id=router_list[i].node_id,
                         adapter_number=router_interfaces[routers[i]], port_number=0),
                    dict(node_id=router_list[j].node_id,
                         adapter_number=router_interfaces[routers[j]], port_number=0)
                ]
                extra_link = Link(project_id=lab.project_id, connector=server, nodes=links)
                extra_link.create()
                router_interfaces[routers[i]] -= 1
                router_interfaces[routers[j]] -= 1


def add_router(lab):
    return


def get_lab_id(lab):
    return lab.project_id


def get_node_id(router_list):
    router_ids = []
    for router in router_list:
        router_ids.append(router.node_id)
    return router_ids


def get_node_console(node):
    return node.console


def get_router_list(config_file):
    router_names = []

    # Get all routers hostnames into a list
    for PE in config_file["PE_routers"]:
        router_names.append(PE["hostname"])
    for P in config_file["P_routers"]:
        router_names.append(P["hostname"])
    #for CE in config_file["CE_routers"]:
    #    router_names.append(CE["hostname"])
    print("Routers:", router_names)
    return router_names
