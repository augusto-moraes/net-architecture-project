from gns3fy import Gns3Connector, Project, Link, Node
from tabulate import tabulate

server = Gns3Connector(url="http://localhost:3080", user="admin", cred="1234")

#def create_lab() :
#	lab = Project(name="test_lab10", connector=server)
#	lab.create()
#	return lab

def create_router(routers):
	lab = Project(name="test_lab12", connector=server)
	lab.create()

	for template in server.get_templates():
		if "c7200" in template["name"]:
			print(f"Template: {template['name']} -- ID: {template['template_id']}")

	#server.get_template_by_name("c7200")
	#server.get_version()
	for r in routers:
		router = Node(
			project_id=lab.project_id,
			connector=server,
			name=r,
			template="c7200")
		router.create()

#def create_link():
	nodes = [
		dict(node_id=router.node_id, adapter_number=1, port_number=0),
		dict(node_id=router.node_id, adapter_number=0, port_number=0)
	]
	extra_link = Link(project_id=lab.project_id, connector=server, nodes=nodes)
	extra_link.create()
def main():
	#create_lab()
	create_router(["PE1", "P1", "P2", "PE2"])


if __name__ == "__main__":
	main()

