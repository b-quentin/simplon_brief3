import json
from lib2to3.pgen2 import driver
import subprocess
import shlex

group = {
    'name': 'groupe_5-1',
    'location': 'francecentral'
}


list_id = {}
ip_list={}


def exec(cmd, my_stdin=None):
    p = subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, err = p.communicate(my_stdin)
    return{'output': output.decode(), 'err': err.decode()}


def gest_output(cmd, a=None):
    global list_id
    if 'ERROR' in cmd['err']:

        ##########################################################
        # [TO DO ]à remplacer le print par la fonction de rollback
        ##########################################################
        error = cmd['err']
        print(error)
    elif cmd['output']:
        print('OK pour ', a)
        data = json.loads(cmd['output'])

        if 'id' in data:
            list_id[a] = data["id"]
            print(data)
        
        

           
    #########################################
    # [ TO DO] retire avant la mise en prod #
    #########################################
    #else:
        # print(data)


def rollback(group):
    cmd = exec(f"az group delete -n {group['name']} -y ")
    gest_output(cmd)

# base infra


def create_group(group):
    a = 'rg'
    cmd = exec(f"az group create -n {group['name']} -l {group['location']}")
    gest_output(cmd, a)


def nsg_create(group):
    a = 'nsg'
    cmd = exec(
        f"az network nsg create -n nsg-{group['name']} -g {group['name']}")
    gest_output(cmd, a)


def create_vnet(group):
    a = 'vnet'
    cmd = exec(
        f"az network vnet create -g  {group['name']} -n vnet-{group['name']} --address-prefix 10.0.1.0/24 --subnet-name subnet-{group['name']} --subnet-prefix 10.0.1.0/26")


###############################################################################

# vm jenkins

def create_data_disk():
    a = 'data-jenkins'
    cmd = exec(f"az disk create --name data-jenkins -g {group['name']} --size-gb 60 --sku Standard_LRS --encryption-type EncryptionAtRestWithPlatformKey")
    gest_output(cmd, a)


def create_vm(group):
    ############################################
    # [ TO DO ]ajout des utilisateurs et clé ssh
    ############################################
    a = 'vm'
    cmd = exec(f"az vm create -g {group['name']} -n vm-jenkins --image UbuntuLTS --size Standard_B2s --admin-username paul --ssh-key-values 'C:\Users\utilisateur\.ssh\id_rsa.pub'  --authentication-type ssh --public-ip-sku Standard --private-ip-address 10.0.1.10 --attach-data-disks data-jenkins")
    gest_output(cmd, a)

def nsg_rule_jenkins(group):
    a = 'nsg-rule'
    cmd = exec(f"az network nsg rule create -n nsg_rule-jenkins -g {group['name']} --nsg-name vm-jenkinsNSG --priority 200 --protocol Tcp --source-port-ranges * --destination-port-ranges 80")
    gest_output(cmd, a)


def fqdn(group):
    a='fqdn'
    cmd = exec(f"az network public-ip update -g {group['name']} --name vm-jenkinsPublicIP --dns-name jenkins51")
    gest_output(cmd, a)
####################################################################################

# creation element bastion


def create_bastionPublicIp(group):
    a = 'bastpubip'
    cmd = exec(f"az network public-ip create -g {group['name']} -n bastionPublicIp --version IPv4 --sku Standard")
    gest_output(cmd, a)


def create_bastion_subnet(group):
    a = 'bastsubnet'
    cmd = exec(f"az network vnet subnet create -g {group['name']} -n AzureBastionSubnet --address-prefixes 10.0.1.64/26 --vnet-name vnet-{group['name']}")
    gest_output(cmd, a)


def create_bastion(group):
    a = 'bastcreate'
    cmd = exec(f"az network bastion create -g {group['name']} -n bastion-{group['name']} -l {group['location']} --vnet-name vnet-{group['name']} --public-ip-address bastionPublicIp ")
    gest_output(cmd, a)


def create_bastion(group):
    a = 'bastcreate'
    cmd = exec(f"az network bastion create -g {group['name']} -n bastion-{group['name']} -l {group['location']} --vnet-name vnet-{group['name']} --public-ip-address bastionPublicIp ")
    gest_output(cmd, a)


def update_bastion():
    a = 'update bastion'
    bastid = list_id['bastcreate']
    cmd = exec(f"az resource update --ids {bastid} --set properties.enableTunneling=True ")
    gest_output(cmd, a)


def connect_bastion(group):
    a = 'bastssh'

    my_stdin = b"""
    sudo apt-get update -y
    sudo apt-get upgrade -y
    sudo apt-get autoremove -y
    sudo apt-get install nginx -y
    sudo apt-get update -y
    sudo apt-get install openjdk-11-jre --yes
    sudo curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo tee \
     /usr/share/keyrings/jenkins-keyring.asc > /dev/null
    sudo echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
    https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
    /etc/apt/sources.list.d/jenkins.list > /dev/null
    sudo apt-get update
    sudo apt-get install jenkins -y
    sudo apt-get update
    sudo systemctl stop nginx
    sudo cat /etc/nginx/sites-available/default | sudo sed -i '51d' /etc/nginx/sites-available/default
    sudo cat /etc/nginx/sites-available/default | sudo sed -i '51i\                #try_files $uri $uri/ =404;' /etc/nginx/sites-available/default
    sudo cat /etc/nginx/sites-available/default | sudo sed -i '52i\                proxy_pass http://127.0.0.1:8080;'  /etc/nginx/sites-available/default
    sudo service nginx restart
    sudo nginx -s reload
    sudo systemctl restart jenkins
    key=`sudo cat /var/lib/jenkins/secrets/initialAdminPassword`
    sudo java -jar /var/cache/jenkins/war/WEB-INF/jenkins-cli.jar -s http://jenkins51.francecentral.cloudapp.azure.com who-am-i --username #admin --password $key`    
    
                """
    vmid=list_id['vm']
    # bastid='/subscriptions/a1f74e2d-ec58-4f9a-a112-088e3469febb/resourceGroups/groupe_5-1/providers/Microsoft.Network/bastionHosts/bastion-groupe_5-1'
    #vmid = '/subscriptions/a1f74e2d-ec58-4f9a-a112-088e3469febb/resourceGroups/groupe_5/providers/Microsoft.Compute/virtualMachines/vm-jenkins'

    cmd = (f"az network bastion ssh -n bastion-{group['name']} -g {group['name']} --target-resource-id {vmid} --auth-type ssh-key --username paul --ssh-key 'C:\Users\utilisateur\.ssh\id_rsa' ")

    ssh_bastion = subprocess.Popen( cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = ssh_bastion.communicate(my_stdin)

    if out is not None:
        out = out.decode()
        print('retour : ', out)

        if err is not None:
            err = err.decode()
        print('erreur : ', err)



#'''
create_group(group)
create_vnet(group)
nsg_create(group)
create_data_disk()
create_vm(group)
fqdn(group)
nsg_rule_jenkins(group)
create_bastion_subnet(group)
create_bastionPublicIp(group)
create_bastion(group)
update_bastion()
with open("list_id.py", "a") as fichier:
    fichier.write(str(list_id))
print('voici la liste des id : ',list_id)
connect_bastion(group)
#'''


#rollback(group)





