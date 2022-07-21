[Création resource group](https://docs.microsoft.com/en-us/cli/azure/group?view=azure-cli-latest#az-group-create) :  

```console  
az group create \
    --name resGroupName \
    --location ... 
```

[Création Virtual Network](https://docs.microsoft.com/en-us/cli/azure/network/vnet?view=azure-cli-latest#az-network-vnet-create) :  
```console
az network vnet create \
  --name vNetName \
  --resource-group resGroupName \
  --subnet-name default
  ```

[Création IP Publique](https://docs.microsoft.com/en-us/cli/azure/network/public-ip?view=azure-cli-latest#az-network-public-ip-create) :  
```console
az network public-ip create -g resGroupName -n MyIp --dns-name MyLabel --allocation-method Static
```  

[Création Network Interface Card](https://docs.microsoft.com/en-us/cli/azure/network/nic?view=azure-cli-latest#az-network-nic-create)  
```console
az network nic create -g resGroupName --vnet-name MyVnet --subnet MySubnet -n MyNic \
    --ip-forwarding --network-security-group MyNsg
```

[Création VM](https://docs.microsoft.com/en-us/cli/azure/vm?view=azure-cli-latest#az-vm-create)  

```console
az vm create --name
             --resource-group
             [...]
```
