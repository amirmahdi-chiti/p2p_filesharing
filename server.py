import uvicorn
from fastapi import FastAPI
import util
import threading
from fastapi.responses import FileResponse
import requests


for f in util.friend_nodes:
    print(f)

app = FastAPI()
@app.get("/file")
async def getfile(filename: str):
    return FileResponse(path="test.txt")



def run_server():
    if __name__ == "__main__":
        uvicorn.run(app, host="localhost", port=util.port_number, access_log=False, log_level="critical")


def read_request():
    x = requests.get("http://localhost:4000/file")
    print(x)
    while (True):
        input_str = input()
        x = input_str.split()
        if x[0] == "request":
            print("request")
        else:
            print("command not found")


t1 = threading.Thread(target=run_server)
t2 = threading.Thread(target=read_request)

t1.start()
t2.start()

t1.join()
t2.join()




