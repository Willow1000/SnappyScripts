import subprocess
import os
import json
file_name = 'wifipass.json'

def infoExtract(phrase,command):
    process = subprocess.Popen(f"{command}", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stdout:
        results = stdout.decode('utf8')
        cont = [i.strip().split(':')[1].strip() for i in results.split('\n') if f"{phrase}" in i]
        return cont
    else:
        print(f"An error occurred while fetching ssids: {stderr}")   
        return
def main():
    keyDict = {}
    ssid = infoExtract('All User Profile','netsh wlan show profile')
    for i in ssid:
        if infoExtract("Key Content",f'netsh wlan show profile name="{i}" key=clear'):
            key = infoExtract("Key Content",f'netsh wlan show profile name="{i}" key=clear')
            keyDict.update({i:key[0]})
    if os.path.exists(file_name):      
        with open(file_name,"r") as f:
            cont= f.read()
            known_networks = json.loads(cont)
        keyDict.update(known_networks) 
    with open(file_name,"w") as f:
        json.dump(keyDict,f)
if __name__ == "__main__":
    main()
