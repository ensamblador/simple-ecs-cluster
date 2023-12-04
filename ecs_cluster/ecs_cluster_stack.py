from aws_cdk import Stack, aws_ssm as ssm, aws_ec2 as ec2, aws_ecs as ecs
from constructs import Construct


class EcsClusterStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

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