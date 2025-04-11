import subprocess
import os
import platform
import json


wifipass = "wifipass.json"
system_os = platform.platform().lower()
# RUN THIS SCRIPTAFTER RUNNING wifipass.py
# This script will connect to the wifi network using the ssid and password stored in wifipass.json
def get_available_networks():    
    try:
        if 'windows' in system_os:
            comm = subprocess.Popen('netsh wlan show network | findstr "SSID"',stderr=subprocess.PIPE,stdout=subprocess.PIPE,encoding="utf8",shell=True)
        elif 'linux' in system_os:
            comm = subprocess.Popen('nmcli -t -f active,ssid dev wifi | grep "^yes:"',stderr=subprocess.PIPE,stdout=subprocess.PIPE,encoding="utf8",shell=True)

        else:
            print("Your os doesn't support this script")    
        stdout,stderr = comm.communicate()

        if stderr:
            print(f"An error occurred: {stderr}")
        
        else:
            if os.path.exists(wifipass):
                with open("wifipass.json",'r') as f:
                    cont= f.read()
                    known_networks = json.loads(cont)
                available_networks = {i.split(":")[1].strip():known_networks.get(i.split(":")[1].strip()) for i in stdout.split("\n") if i and (i.split(":")[1].strip() in known_networks.keys() )}
                return available_networks
            else:
                print("No known networks found")
                quit()     
    except Exception as e:
        print(f"An error occured: {e.args}")

def connect_to_wifi(ssid, password):
    profile_name = ssid
    if "windows" in system_os:
        try:
            xml_content = f'''<?xml version="1.0"?>
            <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
            <name>{ssid}</name>
            <SSIDConfig>
                <SSID>
                <name>{ssid}</name>
                </SSID>
            </SSIDConfig>
            <connectionType>ESS</connectionType>
            <connectionMode>auto</connectionMode>
            <MSM>
                <security>
                <authEncryption>
                    <authentication>WPA2PSK</authentication>
                    <encryption>AES</encryption>
                    <useOneX>false</useOneX>
                </authEncryption>
                <sharedKey>
                    <keyType>passPhrase</keyType>
                    <protected>false</protected>
                    <keyMaterial>{password}</keyMaterial>
                </sharedKey>
                </security>
            </MSM>
            </WLANProfile>'''

        # Save the XML profile to a temp location
            xml_path = os.path.join(os.getcwd(), f"{ssid}.xml")
            with open(xml_path, 'w') as file:
                file.write(xml_content)
            subprocess.run(["netsh", "wlan", "add", "profile", f"filename={xml_path}"], check=True)
            # Connect to the network
            subprocess.run(["netsh", "wlan", "connect", f"name={profile_name}"], check=True)
            print(f"Successfully connected to {ssid}")    
        except subprocess.CalledProcessError as e:
            print(f"Failed to connect: {e}")   
    elif "linux" in system_os:
        try:
            subprocess.run("sudo su root",shell=True,check=True)
            subprocess.run([
                "nmcli",
                "connection",
                "add",
                "type",
                "wifi",
                "ifname",ssid,
                "con-name",ssid,
                "ssid",ssid,
            ],check=True,shell=True)
            subprocess.run([
                "nmcli",
                "connection",
                "modify",
                ssid,
                "wifi-sec.key-mgmt",
                "wpa-psk",
            ],check=True,shell=True)
            subprocess.run([
                "nmcli",
                "connection",
                "modify",
                ssid,
                "wifi-sec.psk",
                password,
            ],check=True,shell=True)
            subprocess.run([
                "nmcli",
                "connection",
                "up",
                ssid,
            ],check=True,shell=True)

            subprocess.run([
                "nmcli",
                "connection",
                "up",
                ssid,
            ],check=True,shell=True)
            print(f"Successfully connected to {ssid}")

        except subprocess.CalledProcessError as e:
            print(f"Failed to connect: {e}")
def main():
    available_networks = get_available_networks()
    ssid = input("Enter the SSID of the network you want to connect to: ").strip()

    if ssid and ssid in available_networks.keys():
        print(f"Connecting to {ssid}...")
        connect_to_wifi(ssid, available_networks[ssid])
    elif ssid and ssid not in available_networks.keys() and os.path.exists(wifipass):
        print(f"{ssid} is not in the list of known networks. Please check the SSID and try again.")
    else:
        ssid,password = [i for i in available_networks.items()][0]
        print(f"Connecting to {ssid}...")
        connect_to_wifi(ssid, password)
 
if __name__ == "__main__":
    main()