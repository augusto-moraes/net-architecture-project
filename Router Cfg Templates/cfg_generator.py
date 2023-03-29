import jinja2
import json
import os


def createCfg():
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
    print("Create templates...")

    for parameter in config_parameters_PE:
        result = template_PE.render(parameter)
        f = open(os.path.join(output_directory, parameter['hostname'] + ".config"), "w")
        f.write(result)
        f.close()
        print("Configuration '%s' created..." % (parameter['hostname'] + ".config"))
    for parameter in config_parameters_P:
        result = template_P.render(parameter)
        f = open(os.path.join(output_directory, parameter['hostname'] + ".config"), "w")
        f.write(result)
        f.close()
        print("Configuration '%s' created..." % (parameter['hostname'] + ".config"))


    print("DONE")

def main():
    createCfg()

if __name__ == "__main__":
    main()

