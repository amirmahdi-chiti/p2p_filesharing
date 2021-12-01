import yaml

port_number: int

a_yaml_file = open("Config.yml")
parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
node_number = parsed_yaml_file["node_number"]
port_number = parsed_yaml_file["node_port"]
friend_nodes = parsed_yaml_file["friend_nodes"]
owned_files_dir = parsed_yaml_file["owned_files_dir"]
new_files_dir = parsed_yaml_file["new_files_dir"]
owned_files = parsed_yaml_file["owned_files"]

cp = []
for i in range(len(friend_nodes)):
    cp.append(friend_nodes[i].copy())


def rearrange(arr, n, x):
    m = {}

    # Store values in a map
    # with the difference
    # with X as key
    for i in range(n):
        m[arr[i]["node_name"]] = abs(x - arr[i]["node_name"])

    m = {k: v for k, v in sorted(m.items(),
                                 key=lambda item: item[1])}
    # print(m)
    # Update the values of array
    i = 0

    for it in m.keys():
        arr[i]["node_name"] = it
        i += 1


rearrange(friend_nodes, len(friend_nodes), node_number)

for f in friend_nodes:
    for f2 in cp:
        if f["node_name"] == f2["node_name"]:
            f["node_port"] = f2["node_port"]
            break
