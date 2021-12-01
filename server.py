import uvicorn
from fastapi import FastAPI
from file import file
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
def getfile(file_name:str):
    return FileResponse(path=f"./{file_name}", media_type="text", status_code=200)

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
        f = requests.get("http://localhost:4000/file",params={"file_name":"test.txt"})



        fw = open("new.txt", "wb")
        # print(f.text)
        fw.write(f.content)
        fw.close()

        fa = open("new.html", "rb")
        print(f.status_code)
        fa.close()
        # print(f.iter_content())
        # fNew = open("new.txt", "w")
        # f3:file = f
        # print(f.raise_for_status())
        # fNew.write(f.text)
        # fNew.close()
        # print(f.text)
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




