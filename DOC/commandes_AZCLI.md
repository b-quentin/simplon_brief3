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
az network public-ip create -g MyResourceGroup -n MyIp --dns-name MyLabel --allocation-method Static
```  

