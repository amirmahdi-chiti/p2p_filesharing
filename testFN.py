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

app = FastAPI()

@app.get("/file", response_class=FileResponse)
def getfile(file_name:str, parent:int):
    return FileResponse(path="NOT_FOUND.txt", media_type="text", status_code=200)

#@router.get("/file")
#def get_file(name_file: str):
#    return FileResponse(path=getcwd() + "/" + name_file)

def run_server():
    if __name__ == "__main__":
        uvicorn.run(app, host="localhost", port=8080, access_log=False)


def read_request():
        input()
        x = requests.get("http://localhost:8080/file",
                    params={"file_name":"fileRequested", "parent":12})
        print(x.content.decode('ascii'))


t1 = threading.Thread(target=run_server)
t2 = threading.Thread(target=read_request)

t1.start()
t2.start()

t1.join()
t2.join()




