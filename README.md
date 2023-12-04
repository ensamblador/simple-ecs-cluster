
# Simple ECS Cluster Stack

Este proyecto crea los siguientes recursos dentro de una región de AWS:

* 1 Cluster ECS


Parámetro en Parameter Store para guardar `cluster-name`.

![ecs cluster](/ecs-cluster.jpg)

el codigo es bastante simple de [`ecs_cluster_stack.py`](ecs_cluster/ecs_cluster_stack.py.py)


```python
from aws_cdk import Stack, aws_ssm as ssm, aws_ec2 as ec2, aws_ecs as ecs
from constructs import Construct


class EcsClusterStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #debe existir el parámetro vpc-id creado en parameter store
        vpc_id = ssm.StringParameter.value_from_lookup(self, parameter_name="/gen-ai-apps/vpc-id")
        vpc = ec2.Vpc.from_lookup(self, "V",vpc_id= vpc_id)

        ecs_cluster = ecs.Cluster(self, "C", cluster_name="genai-apps", vpc=vpc)

        ssm.StringParameter(
            self,
            "ssm-cluster",
            description="VPC Base para utilizar",
            parameter_name="/gen-ai-apps/ecs-cluster-name",
            string_value=ecs_cluster.cluster_name
        )
```




Realmente la creación del cluster ecs ocurre en la línea 
```python 
ecs_cluster = ecs.Cluster(self, "C", cluster_name="genai-apps", vpc=vpc)
```

Lo que nos muestra el nivel de abstracción que nos puede entregar CDK.

## Instrucciones para despliegue


Clonar y crear un ambiente virtual python para el proyecto

```zsh
git clone https://github.com/ensamblador/simple-ecs-cluster.git
cd simple-ecs-cluster
python3 -m venv .venv
```

En linux o macos el ambiente se activa así:

```zsh
source .venv/bin/activate
```

en windows

```cmd
% .venv\Scripts\activate.bat
```

Una vez activado instalamos las dependencias
```zsh
pip install -r requirements.txt
```

en este punto ya se puede desplegar:

```zsh
cdk deploy
```

y para eliminar:

```zsh
cdk destroy
```


## Otros comandos útiles

 * `cdk synth`       crea un template de cloudformation con los recursos de este proyecto
 * `cdk diff`        compara el stack desplegado con el nuevo estado local

Enjoy!
