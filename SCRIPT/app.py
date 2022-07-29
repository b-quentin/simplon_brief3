
import subprocess
import json
import time
import paramiko
import requests


group = {
    'name' : 'group5test',
    'location' : 'centralus'
}

nsg_app = {
    'name': 'nsg_app'
}

nsg_bastion = {
    'name' : 'nsg_bastion'
}

network = {
    'name' : 'network',
    'adress' : '10.0.1.0/24'
}

rule_app = {
    'name': 'https',
    'priority': '100',
    'description': 'https connexion on internet',
    'protocol': 'Tcp',
    'port' : '443'
}
rule_http_app = {
    'name': 'http',
    'priority': '110',
    'description': 'http connexion on internet',
    'protocol': 'Tcp',
    'port' : '80'
}
subnet_bastion = {
    'name' : 'AzureBastionSubnet',
    'adress' : '10.0.1.0/26'
}

subnet_app = {
    'name' : 'subnet_app',
    'adress': '10.0.1.64/26'
}
disk_app = {
    'name': 'disk_app'
}

disk_app_data = {
    'name' : 'disk_app_data'
}
nic = {
    'name' : 'nic_app'
}
vm = {
    'name' : 'vm_app',
    'admin' : 'quentin'
}
ip_bastion = {
    'name' : 'ip_bastion'
}
ip_app = {
    'name' : 'ip_app',
    'dns_name' : 'jenkinsapp'
}
bastion = {
    'name' : 'bastion'
}
nsg_bastion = {
    'name' : 'nsg_bastion'
}


def exec(cmd):
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(p.__str__())
        output, err = p.communicate()

        return {'output': output.decode(), 'error': err.decode()}

def exec_bg(cmd):
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(p.__str__())


def handle_text(text):
    return str(text).replace(r'\n', '\n').replace('b', '')

def create_group(group):
    group = exec(['az', 'group', 'create', '-n', group['name'], '-l', group['location']])

    if group['error'].__str__() != "b''":
        print(handle_text(group['error']))
    else:
        data = json.loads(group['output'])
        print(data)

def delete_group(group):
    print('Waiting delete group.')
    group = exec(['az', 'group', 'delete', '-n', group, '--yes'])
    print(group)
    print('Group delete.')

def create_network(group, network, subnet):
    #https://docs.microsoft.com/en-US/cli/azure/network/vnet?view=azure-cli-latest#az-network-vnet-create
    network = exec(['az', 'network', 'vnet', 'create',
        '-g', group,
        '--name', network['name'],
        '--address-prefix', network['adress'],
        '--subnet-name', subnet['name'],
        '--subnet-prefix', subnet['adress']
        ])

    if network['error'].__str__() != "b''":
        print(handle_text(network['error']))
        delete_group()
    else:
        data = json.loads(network['output'])
        print(data)

def create_nsg(nsg, group):
    nsg = exec(['az', 'network', 'nsg', 'create', '-n', nsg, '-g', group])

    if "ERROR" in nsg['error'].__str__():
        print(handle_text(nsg['error']))
        delete_group()
    else:
        data = json.loads(nsg['output'])
        print(data)

def create_subnet(group, network, nsg, subnet):
    subnet = exec(['az', 'network', 'vnet', 'subnet', 'create', '-n', subnet['name'],'-g', group, '--vnet-name', network, '--address-prefixes', subnet['adress'], '--network-security-group', nsg])

    if "ERROR" in subnet['error'].__str__():
        print(handle_text(subnet['error']))
        delete_group()
    else:
        data = json.loads(subnet['output'])
        print(data)

def create_public_adress():
    #https://docs.microsoft.com/fr-fr/cli/azure/network/public-ip?view=azure-cli-latest
    adress = exec(['az', 'network', 'public-ip', 'create', '-g', 'groupe5', '-n', "ip_bastion", '--sku', 'Standard'])

    if "ERROR" in adress['error'].__str__():
        print(handle_text(adress['error']))
        delete_group()
    else:
        data = json.loads(adress['output'])
        print(data)

def create_vm(vm, group, disk, nic, disk_data):
    vm = exec(['az', 'vm', 'create',
    '--name', vm['name'],
    '-g', group,
    '--image', 'UbuntuLTS',
    '--admin-username', vm['admin'],
    '--ssh-key-value','/home/nomad/.ssh/azure.pub',
    '--os-disk-name', disk,
    '--nics', nic,
    '--attach-data-disks', disk_data,
    '--authentication-type', 'ssh',
    '--size', 'Standard_D2as_v5'
    ])

    if "ERROR" in vm['error'].__str__():
        print(handle_text(vm['error']))
        delete_group()
    else:
        data = json.loads(vm['output'])
        print(data)

def create_ip_public_app(ip, group):
    ip = exec(['az','network','public-ip', 'create',
    '-n', ip['name'],
    '-g', group,
    '--sku', 'Standard',
    '--dns-name', ip['dns_name']
    ])
    if "ERROR" in ip['error'].__str__():
        print(handle_text(ip['error']))
        delete_group()
    else:
        data = json.loads(ip['output'])
        print(data)

def create_ip_public(ip, group):
    ip = exec(['az','network','public-ip', 'create', '-n', ip['name'], '-g', group, '--sku', 'Standard'])
    if "ERROR" in ip['error'].__str__():
        print(handle_text(ip['error']))
        delete_group()
    else:
        data = json.loads(ip['output'])
        print(data)

def create_bastion(bastion, group, network, ip_bastion):
    #https://docs.microsoft.com/fr-fr/cli/azure/network/bastion?view=azure-cli-latest#az-network-bastion-create
    """
    az network bastion create --name
                          --public-ip-address
                          --resource-group
                          --vnet-name
    """

    bastion = exec(['az', 'network', 'bastion', 'create',
    '--name', bastion['name'],
    '--public-ip-address', ip_bastion,
    '-g', group,
    '--vnet-name', network])

    if "ERROR" in bastion['error'].__str__():
        print(handle_text(bastion['error']))
        delete_group()
    else:
        data = json.loads(bastion['output'])
        print(data)

def create_disk(disk, group):
    disk = exec(['az','disk', 'create',
    '--name', disk['name'],
    '-g', group,
    '--size-g', '1000'
    ])

    if "ERROR" in disk['error'].__str__():
        print(handle_text(disk['error']))
        delete_group()
    else:
        data = json.loads(disk['output'])
        print(data)

def create_nic(nic, group, subnet, network, ip):
    nic = exec(['az', 'network', 'nic', 'create',
    '--name', nic['name'],
    '-g', group,
    '--subnet', subnet,
    '--vnet-name', network,
    '--public-ip-address', ip
    ])

    if "ERROR" in nic['error'].__str__():
        print(handle_text(nic['error']))
        delete_group()
    else:
        data = json.loads(nic['output'])
        print(data)

def create_nsg_rule(rule, nsg, group):
    """

    az network nsg rule create --name
                           --nsg-name
                           --priority
                           --resource-group
                           [--access {Allow, Deny}]
                           [--description]
                           [--destination-address-prefixes]
                           [--destination-asgs]
                           [--destination-port-ranges]
                           [--direction {Inbound, Outbound}]
                           [--protocol {*, Ah, Esp, Icmp, Tcp, Udp}]
                           [--source-address-prefixes]
                           [--source-asgs]
                           [--source-port-ranges]
    """
    rule = exec(['az', 'network', 'nsg', 'rule', 'create',
    '--name', rule['name'],
    '--nsg', nsg,
    '--priority', rule['priority'],
    '-g', group,
    '--description', rule['description'],
    '--protocol', rule['protocol'],
    '--destination-port-ranges', rule['port']
    ])
    if "ERROR" in rule['error'].__str__():
        print(handle_text(rule['error']))
        delete_group()
    else:
        data = json.loads(rule['output'])
        print(data)

def get_bastion_id(group,bastion):
    id = exec(['az','network', 'bastion', 'show',
    '-g', group,
    '-n', bastion,
    '--query', '"id"'
    ])

    if "ERROR" in id['error'].__str__():
        print(id['error'])
        delete_group()
    else:
        return str(id['output']).replace('b\'', '').replace('\\n\'', '').replace('"', '')
# az resource update --ids <bastion resource ids> --set properties.enableTunneling=True

def set_tunnel(id):
    tunnel = exec(['az', 'resource', 'update',
    '--ids', id,
    '--set', 'properties.enableTunneling=True'
    ])

    if "ERROR" in tunnel['error'].__str__():
        print(tunnel['error'])
        delete_group()
    else:
        print(tunnel)
#https://docs.microsoft.com/fr-fr/cli/azure/vm/user?view=azure-cli-latest#az-vm-user-update
def create_user(group,username, key, vm):
    """
    az vm user update --username
                  [--ids]
                  [--name]
                  [--no-wait]
                  [--password]
                  [--resource-group]
                  [--ssh-key-value]
    """
    user = exec(['az', 'vm', 'user', 'update',
    '--username', username,
    '--ssh-key-value', key,
    '-n', vm,
    '-g', group
    ])

    if "ERROR" in user['error'].__str__():
        print(user['error'])
        delete_group()
    else:
        print(user)
# az network bastion tunnel --name "bastion" --resource-group "group5" --target-resource-id "/subscriptions/a1f74e2d-ec58-4f9a-a112-088e3469febb/resourceGroups/group5/providers/Microsoft.Compute/virtualMachines/vm_app" --resource-port "22" --port "2029"

def tunnel(bastion_name, id, group):
    tunnel = exec_bg(['az', 'network', 'bastion', 'tunnel',
    '-n', bastion_name,
    '-g', group,
    '--target-resource-id', id,
    '--resource-port', '22',
    '--port', '2023',
    ])

    return tunnel
def get_vm_id(group,vm):
    id = exec(['az','vm','show',
    '-g', group,
    '-n', vm,
    '--query', '"id"'
    ])
    if "ERROR" in id['error'].__str__():
        print(id['error'])
        delete_group()
    else:
        return str(id['output']).replace('b\'', '').replace('\\n\'', '').replace('"', '')

def ssh_vm():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname = "127.0.0.1", username = "quentin", key_filename='/home/nomad/.ssh/azure', port=2029)
    channel = ssh.invoke_shell()

    return channel
#az network public-ip show -g group5 -n ip_app --query "dnsSettings.fqdn"
def get_domaine_name(group,ip):
    name = exec(['az', 'network', 'public-ip', 'show',
    '-g', group,
    '-n', ip,
    '--query', 'dnsSettings.fqdn'
    ])

    if "ERROR" in name['error'].__str__():
        print(name['error'])
        delete_group()
    else:
        return str(name['output']).replace('"', '')

def ssh_co(cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    barbare = True
    while barbare:
        time.sleep(60)
        try:
            client.connect(hostname = "127.0.0.1", username = "quentin", key_filename='/home/nomad/.ssh/azure', port=2023)
        except:
            print('error co ssh')
        else:
            barbare = False

    stdin, stdout, stderr = client.exec_command(cmd)
    if stdout.channel.recv_exit_status() != 0:
        print('error')
    for line in iter(stdout.readline, ""):
        print(line, end="")
    for line in iter(stderr.readline, ""):
        print(line, end="")
    print('finished.')
    client.close()

def ssh_certbot(cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(hostname = "127.0.0.1", username = "quentin", key_filename='/home/nomad/.ssh/azure', port=2023)

    stdin, stdout, stderr = client.exec_command(cmd)

    stdin.write("1\n")
    stdin.flush()
    stdin.write("2\n")
    stdin.flush()

    client.close()

def ssh_sftp_conf_nginx_certbot():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(hostname = "127.0.0.1", username = "quentin", key_filename='/home/nomad/.ssh/azure', port=2023)

    sftp = client.open_sftp()
    f_out = sftp.file('/etc/nginx/conf.d/install_tls.conf', "w")
    f_out.write('server {\n\tlocation / {\n\t\troot /var/www;\n\t}\n}')
    f_out.close()

    print('finished.')
    client.close()

def ssh_sftp_conf_certbot():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(hostname = "127.0.0.1", username = "quentin", key_filename='/home/nomad/.ssh/azure', port=2023)

    sftp = client.open_sftp()
    f_out = sftp.file('/etc/letsencrypt/cli.ini', "w")
    f_out.write('email = b.quentin@protonmail.com\nagree-tos = true')
    f_out.close()

    print('finished.')
    client.close()

def send_jenkins_config():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(hostname = "127.0.0.1", username = "quentin", key_filename='/home/nomad/.ssh/azure', port=2023)

    sftp = client.open_sftp()
    sftp.put('./jenkins.conf','/etc/nginx/conf.d/jenkins.conf')
    sftp.close()
    client.close()

def send_nginx_config():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(hostname = "127.0.0.1", username = "quentin", key_filename='/home/nomad/.ssh/azure', port=2023)

    sftp = client.open_sftp()
    sftp.put('./default.conf','/etc/nginx/sites-available/default')
    sftp.close()
    client.close()



delete_group(group['name'])

create_group(group)

create_nsg(nsg_app['name'], group['name'])

create_network(group['name'], network, subnet_bastion)
create_subnet(group['name'], network['name'], nsg_app['name'], subnet_app)

create_ip_public_app(ip_app, group['name'])

create_nic(nic, group['name'], subnet_app['name'], network['name'], ip_app['name'])
create_disk(disk_app_data, group['name'])

create_vm(vm, group['name'], disk_app['name'], nic['name'], disk_app_data['name'])

create_user(group['name'],'paul','ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDCWIWXMnQoBimi0uEDgNo+WY0oMzLIneka5OfvNtSA4zflxHYbv3wbYT0mLtDviolSXQAK26QlYBgaKd21men6S8SOxdLkrk24pqjT3dPk3CxNigaTqbx/AlAkClKxroT0kba8Pq6td/Z+FsIOI4CT1U/fBZ2BuQp5g5ghoi1PcoT339O8WQRCHX+vTRsGdZdJJCZPpRgNgu9Gh5O05/rnDgeDxFsjcsRBv91wCn0+PNIcqV9SEdppmeo6eAoSb00htk/0cY8e46dHlWvDMo3mKMNCJ1IocoJruQguIXebVwh9djhq/G9X0bG+v0JJ+F0hva19cE3gK/thwSUCyJ8JE5s0JrK0EO1iMUCLSjkKEZwEwPMFFuh+bItMAajFHBmY65kbmn1VE9CvYx6za9xv7G1b8kAHlD6+PRKOz08dxbUnnpS3X+oomPGZ4+hiZAEuwy2vKvYlvNZ3dTkK21VlVPZJFk7L/u5MnC3kiZBnRf6Ar2lNDUf57JwoKSgT0H0= utilisateur@UTILISA-RDIKR2H',vm['name'])

create_nsg_rule(rule_app,nsg_app['name'], group['name'])

create_nsg_rule(rule_http_app,nsg_app['name'], group['name'])
create_ip_public(ip_bastion, group['name'] )

create_bastion(bastion, group['name'], network['name'], ip_bastion['name'])

id_bastion = get_bastion_id(group['name'], bastion['name'])
set_tunnel(id_bastion)

app_id = get_vm_id(group['name'], vm['name'])
tunnel(bastion['name'], app_id, group['name'])

time.sleep(3)

ssh_co('sudo apt update')
ssh_co('sudo apt install openjdk-11-jre -y')


ssh_co('curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null')
ssh_co('echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null')
ssh_co('sudo apt update')
ssh_co('sudo apt install jenkins -y')
ssh_co('sudo apt install certbot -y')
ssh_co('sudo apt install nginx -y')

ssh_co('sudo apt install python3-certbot-nginx -y')

print('create file install_tls')
ssh_co('sudo touch /etc/nginx/conf.d/install_tls.conf')
print('chown intsall tls quentin')
ssh_co('sudo chown -R quentin:quentin /etc/nginx/conf.d/install_tls.conf')
print('send config certbot')
ssh_sftp_conf_nginx_certbot()
print('chown install_tls root')
ssh_co('sudo chown -R root:root /etc/nginx/conf.d/install_tls.conf')
print('start nginx')
ssh_co('sudo systemctl start nginx')

print('While wait fqdn:')
r = requests.head("http://jenkinsapp.centralus.cloudapp.azure.com/")

while r.status_code != 200:
    r = requests.head("http://jenkinsapp.centralus.cloudapp.azure.com/")
    print('Waiting fqdn: ' + str(r.status_code))

print('chown cli.ini quentin')
ssh_co('sudo chown quentin:quentin /etc/letsencrypt/cli.ini')
print('Send file conf certbot')
ssh_sftp_conf_certbot()
print('chown cli.ini root')
ssh_co('sudo chown root:root /etc/letsencrypt/cli.ini')
print('certbot certif')
ssh_certbot('sudo certbot --nginx --config /etc/letsencrypt/cli.ini -d jenkinsapp.centralus.cloudapp.azure.com')

print('chown conf.d quentin')
ssh_co('sudo chown -R quentin:quentin /etc/nginx/conf.d')
print('send jenkins conf')
send_jenkins_config()
print('chown conf.d root')
ssh_co('sudo chown -R root:root /etc/nginx/conf.d')
print('chown sites-available quentin')
ssh_co('sudo chown -R quentin:quentin /etc/nginx/sites-available')
print('send default nginx config')
send_nginx_config()
print('chown default root')
ssh_co('sudo chown -R root:root /etc/nginx/sites-available')
print('delete install_tls.conf')
ssh_co('sudo rm /etc/nginx/conf.d/install_tls.conf')
print('restart nginx')
ssh_co('sudo systemctl restart nginx')
print('start jenkins')
ssh_co('sudo systemctl start jenkins')




