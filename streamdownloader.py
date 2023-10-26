import requests
import csv
import subprocess
from urllib3.exceptions import InsecureRequestWarning
from multiprocessing import Process
import time
from datetime import datetime
import logging

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
logging.basicConfig(filename='./output/log.txt', format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

def getStatusCode(url):
	try:
		r =requests.get(url,verify=False,timeout=5)
		return (r.status_code)
		
	except:
		return -1
        
def manageUrls(url, name):
    streamAvailable = True
    while True:
        if getStatusCode(url) == 200:
            streamAvailable = True
            logging.info(f"{name} Stream now downloading!")
            current_datetime = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
            outputfilename = f"{name}-{current_datetime}.ts"
            cmd = [
            'ffmpeg',
            '-i', url,
            '-c:v', 'libx264',
            '-preset', 'slow',
            '-crf', '15',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-y',
            '-strftime', '1',
            f"/output/{outputfilename}"
        ]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            logging.info(f"{name} Stopped!")
        else:
            if streamAvailable:
                logging.info(f"{name} Stream not available")
                streamAvailable = False
            
        time.sleep(30)		

if __name__ == "__main__": 
    with open("./config/urls.csv", newline="") as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            proc = Process(target=manageUrls, args=(row[0], row[1],))
            proc.start()

    print("started...")