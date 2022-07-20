## conception de l'infrastructure pour le déployement de "JENKINS"

## exigeance conformité AZURE
    * 1- installer un bastion azure
    * 2- créer les comptes utilisateurs et y televerser  
    les clés publiques de chaque utilisateur pour accéder  
    aux VM dès l'installation de ces dernières

## Azure cli

## topologie de l'infrastructure

:::mermaid
flowchart TB
 
  subgraph AZURE 
    A[ BASTION] --> B[VM JENKINS]
    A --ssh key --> C
   
    C[passerelle]
  end

  subgraph admin
    D[Laptop]
   
    D --ssh key--> C
  end
:::
## plan d'action
### descriptions des scripts