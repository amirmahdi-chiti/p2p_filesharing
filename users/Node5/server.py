import uvicorn
from fastapi import FastAPI
import util
import threading
from fastapi.responses import FileResponse
import requests
from os import getcwd
from fastapi.responses import FileResponse

# for f in util.friend_nodes:
#     print(f)
import logging
logging.basicConfig(format='%(asctime)s %(message)s',filename='../Network.log', encoding='utf-8', level=logging.INFO)


app = FastAPI()


@app.get("/file", response_class=FileResponse)
def getfile(file_name: str):
    return FileResponse(path=f"./{util.owned_files_dir}/{file_name}",
                        media_type="text", status_code=200)

def checkSeen(node, seenNodes):
    for seen in seenNodes:
        if int(seen) == node:
            return True
    return False

@app.get("/port")
def getfile(file_name: str, seen: str, searchNode: int):
    friendNodes = []
    seenNodes = seen.split(",")
    fileFound = False

    for i in range(len(util.friend_nodes)):
        friendNodes.append(util.friend_nodes[i].copy())

    for friend in friendNodes:
        if friend['node_name'] == searchNode:
            # return FileResponse(path=f"./{util.owned_files_dir}/{file_name}",
            #                     media_type="text", status_code=200)
            seenNew = seen + "," + str(util.node_number)
            return (f'{str(friend["node_port"])}|{seenNew}')

    # if len(friendNodes) == 1 and friendNodes[0]["node_name"] == parent and not fileFound:
        # return FileResponse(path="NOT_FOUND.txt", media_type="text", status_code=200)
        # return -1
    cnt = len(friendNodes)
    for friend in friendNodes:
        if checkSeen(friend["node_name"], seenNodes):
            cnt -= 1
    if cnt == 0:
        seenNew = seen + "," + str(util.node_number)
        return (f'-1|{seenNew}')

    for ownFriend in friendNodes:

        if checkSeen(ownFriend["node_name"], seenNodes):
            continue

        seenNew = seen + "," + str(util.node_number)
        f = requests.get(f'http://localhost:{ownFriend["node_port"]}/port',
                         params={"file_name": file_name, "seen": seenNew})

        # if f.content.decode('ascii') != "-1":
        #     break
        f = f.text[1:(len(f.text) - 1)]
        if f.split("|")[0] != '-1':
            break

    return f


# @router.get("/file")
# def get_file(name_file: str):
#    return FileResponse(path=getcwd() + "/" + name_file)

def run_server():
    if __name__ == "__main__":
        print("Hi")
        uvicorn.run(app, host="localhost", port=util.port_number, access_log=False)#,log_level="critical")

def findNodeOfFile(file):
    for i in util.node_files:
        for f in i['node_files']:
            if f == file:
                return i['node_name']
    return -1

def read_request():
    while (True):
        input_str = input()
        x = input_str.split()

        if x[0] == "request":
            fileRequested = x[1]
            logging.info(f"{util.node_number} requested {fileRequested}")
        else:
            logging.warning(f"Node{util.node_number} wrong request")
            print("command not found")
            continue

        nodeSearchName = findNodeOfFile(fileRequested)

        if nodeSearchName == -1:
            print(f"couldn't get {fileRequested}")
            logging.warning(f"couldn't get {fileRequested}")
            continue

        fileFound = False
        if nodeSearchName == util.node_number:
            fileFound = True
            print(f"GET FILE FROM NODE {util.node_number}")
            logging.info(f" node {util.node_number} got {fileRequested} from port {util.port_number}")

        if not fileFound:
            portFound = False
            for friend in util.friend_nodes:
                if friend['node_name'] == nodeSearchName:
                    port = f"{friend['node_port']}|NOT"
                    portFound = True
            if not portFound:
                for ownFriends in util.friend_nodes:
                    port = requests.get(f"http://localhost:{ownFriends['node_port']}/port",
                                        params={"file_name": fileRequested,
                                        "parent": util.node_number, "seen":str(util.node_number), "searchNode": nodeSearchName})

                    # if f.content.decode('ascii') != "-1":
                    #     break
                    port = port.text[1:(len(port.text) - 1)]
                    if port.split("|")[0] != '-1':
                        portFound = True
                        break

            if port.split("|")[0] != '-1':
                f = requests.get(f"http://localhost:{port.split('|')[0]}/file",
                                 params={"file_name": fileRequested})
                fw = open(f"./{util.new_files_dir}/{fileRequested}", "wb")
                fw.write(f.content)
                fw.close()
                print(f"{util.node_number} got {fileRequested} from port {port.split('|')[0]}")
                logging.info(f"{util.node_number} got {fileRequested} from port {port.split('|')[0]}")
            else:
                print(f"couldn't get {fileRequested}")
                logging.warning(f"couldn't get {fileRequested}")

t1 = threading.Thread(target=run_server)
t2 = threading.Thread(target=read_request)

t1.start()
t2.start()

t1.join()
t2.join()