from gns3fy import Gns3Connector, Project, Link, Node
from tabulate import tabulate

server = Gns3Connector(url="http://localhost:3080", user="admin", cred="1234")

def create_lab() :
	lab = Project(name="test_lab10", connector=server)
	lab.create()
	return lab

def create_router(lab, routers):
	for template in server.get_templates():
		if "c7200" in template["name"]:
			print(f"Template: {template['name']} -- ID: {template['template_id']}")

	#server.get_template_by_name("c7200")
	#server.get_version()
	router_list = []
	for r in routers:
		router = Node(
			project_id=lab.project_id,
			connector=server,
			name=r,
			template="c7200")
		router.create()
		router_list.append(router)
	return router_list

def create_link(lab, router_list):
	links = []
	for i in range(len(router_list) - 1):
		links.append([
			dict(node_id=router_list[i].node_id, adapter_number=1, port_number=0),
			dict(node_id=router_list[i+1].node_id, adapter_number=2, port_number=0)
		])
	for link in links:
		extra_link = Link(project_id=lab.project_id, connector=server, nodes=link)
		extra_link.create()

def main():
	lab = create_lab()
	router_list = create_router(lab, ["PE1", "P1", "P2", "PE2"])
	create_link(lab, router_list)


if __name__ == "__main__":
	main()

