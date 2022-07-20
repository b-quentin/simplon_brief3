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
  $$ classDef [nom of groupe 1] fill:#faa,stroke:#f66,stroke-width:4px,color:#fff,stroke-dasharray: 5 5;
$$ class [nom d'object à colorer], [nom d'object à colorer];
$$ classDef [nom de groupe 2] fill:#aff,stroke:#025,stroke-width:2px,color:#003;
$$ class [nom d'object à colorer], [nom d'object à colorer];
:::
## plan d'action
### descriptions des scripts