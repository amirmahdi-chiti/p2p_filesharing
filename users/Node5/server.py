import uvicorn
from fastapi import FastAPI
import util
import threading
from fastapi.responses import FileResponse
import requests
from os import getcwd
from fastapi.responses import FileResponse

for f in util.friend_nodes:
    print(f)

app = FastAPI()

@app.get("/file", response_class=FileResponse)
def getfile(file_name:str, parent:int):
    friendNodes = []

    for i in range(len(util.friend_nodes)):
        friendNodes.append(util.friend_nodes[i].copy())

    for ownedFile in util.owned_files:
        if ownedFile == file_name:
            return FileResponse(path=f"./{util.owned_files_dir}/{file_name}",
                media_type="text", status_code=200)

    if len(friendNodes) == 1 and friendNodes[0]["node_name"] == parent:
        return FileResponse(path="NOT_FOUND.txt", media_type="text", status_code=200)


    for ownFriend in friendNodes:
        if ownFriend['node_number'] == parent:
            continue

        f = requests.get(f"http://localhost:{ownFriend['node_port']}/file",
            params={"file_name":file_name, "parent":util.node_number})
        
        if f.content.decode('ascii') != "-1":
            break
    
    return f


    

    

#@router.get("/file")
#def get_file(name_file: str):
#    return FileResponse(path=getcwd() + "/" + name_file)

def run_server():
    if __name__ == "__main__":
        uvicorn.run(app, host="localhost", port=util.port_number, access_log=False, log_level="critical")


def read_request():
    
    while (True):
        input_str = input()
        x = input_str.split()

        if x[0] == "request":
            print("request")
            fileRequested = x[1]
        else:
            print("command not found")
            continue

        fileFound = False
        for ownFile in util.owned_files:
            if (ownFile == fileRequested):
                fileFound = True
                print("GET FILE FROM NODE" + util.node_number)

        if not fileFound:
            for ownFriends in util.friend_nodes:
                f = requests.get(f"http://localhost:{ownFriends['node_port']}/file",
                    params={"file_name":fileRequested, "parent":util.node_number})

                if f.content.decode('ascii') != "-1":
                    break

            fw = open(f"./{util.new_files_dir}/{fileRequested}", "wb")
            fw.write(f.content)
            fw.close()
        


t1 = threading.Thread(target=run_server)
t2 = threading.Thread(target=read_request)

t1.start()
t2.start()

t1.join()
t2.join()




