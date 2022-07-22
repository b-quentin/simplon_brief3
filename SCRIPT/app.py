import json
import subprocess

with open("./init.json", "r") as file:
    data = json.load(file)

def execute_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

    r = {"output_str": process.communicate()[0].decode(), "exit_code": process.returncode}
    
    print(r)

    return r

commands_list = [
    "az group create --name " + data["rg_name"] + " --location " + data["rg_location"],
    "az vm create --name " + data["vm_name"] + " "
                + "--resource-group " + data["rg_name"] + " "
                + "--image Debian:debian-10:10:latest "
                + "--nic-delete-option delete "
                + "--os-disk-delete-option delete "
                + "--data-disk-delete-option delete "
                + "--generate-ssh-keys",
    "az group delete --resource-group " + data["rg_name"] + " --yes"        
]

for i in range(len(commands_list)):
    execute_command(commands_list[i])