import json

import jsonpickle


def user_requirements():
    project_name = input("Project name? ")
    description = input("Description? ")
    CE_routers = input("How Many CE routers? ")
    PE_routers = input("How Many PE routers? ")
    P_routers = input("How Many P routers? ")
    OSPF_core_area = input("OSPF core area number? ")
    OSPF_client_area = input("OSPF client area number? ")
    BGP_core_AS = input("BGP core AS number? ")
    BGP_clientA_AS = input("BGP client A AS number? ")
    BGP_clientB_AS = input("BGP client B AS number? ")
    VRF_name = input("VRF name? ")
    RD = input("RD? ")
    RT_export = input("RT export? ")
    RT_import = input("RT import? ")

    project = [{project_name}, {description}]
    OSPF_config = [{'OSPF_core_area': OSPF_core_area, "OSPF_client_area": OSPF_client_area}]
    BGP_config = [{"BGP_core_AS": BGP_core_AS, "BGP_clientA_AS": BGP_clientA_AS, "BGP_clientB_AS": BGP_clientB_AS}]
    VRF_config = [{"VRF_name": VRF_name, "RD": RD, "RT_export": RT_export, "RT_import": RT_import}]
    CE_routers = []
    PE_routers = []
    P_routers = []

    params = {"project": project, "OSPF_config": OSPF_config, "BGP_config": BGP_config, "VRF_config": VRF_config}

    with open('config_file_usergen.json', 'w') as config_file:
        encoded_params = jsonpickle.encode(params)
        decoded = jsonpickle.decode(encoded_params)
        # json.dump(decoded, config_file)
        # pickle.dump(params, config_file, protocol=pickle.HIGHEST_PROTOCOL)


def main():
    user_requirements()


if __name__ == "__main__":
    main()
