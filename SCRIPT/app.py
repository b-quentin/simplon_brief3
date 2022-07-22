import json
import subprocess

with open("./init.json", "r") as file:
    data = json.load(file)

print(data["rg_name"])

def execute_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

    r = {"output_str": process.communicate()[0].decode(), "exit_code": process.returncode}
    
    print(r)

    return r

commands_list = [
    "az group create --name " + data["rg_name"] + " --location " + data["rg_location"],
    # "az vm create --name " + data["vm_name"] + " "
    #             + "--resource-group " + data["rg_name"] + " "
    #             + "--image Debian:debian-10:10:latest "
    #             + "--nic-delete-option delete "
    #             + "--os-disk-delete-option delete "
    #             + "--data-disk-delete-option delete "
    #             + "--generate-ssh-keys",
    # "az group delete --resource-group " + data["rg_name"] + " --yes"  

    #commandes pour créer le subnet du bastion
    "az network vnet create --resource-group " + data["rg_name"] + " "
            + "--name " + data["vnet_name"] + " "
            + "--address-prefix " + data["vnet_prefix"] + " " 
            + "--subnet-name " + data["subnet-name"] + " "
            + "--subnet-prefix " + data["bastion_subnet"] + " "
            + "--location " + data["rg_location"]
]
#cmd à ajouter :
#az network public-ip create --resource-group MyResourceGroup --name MyIp --sku Standard --location northeurope
#az network bastion create --name MyBastion --public-ip-address MyIp --resource-group MyResourceGroup --vnet-name MyVnet --location northeurope

for i in range(len(commands_list)):
    execute_command(commands_list[i])


# az network public-ip create --resource-group MyResourceGroup --name MyIp --sku Standard --location northeurope

# az network bastion create --name MyBastion --public-ip-address MyIp --resource-group MyResourceGroup --vnet-name MyVnet --location northeurope
    
