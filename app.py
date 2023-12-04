#!/usr/bin/env python3
import os
import boto3
import aws_cdk as cdk

from ecs_cluster.ecs_cluster_stack import EcsClusterStack

TAGS = {"app": "generative ai business apps", "customer": "ecs-cluster"}


region = os.environ.get("AWS_DEFAULT_REGION")
if not region: region = "us-east-1"

caller = boto3.client('sts').get_caller_identity()
account_id = caller.get("Account")

app = cdk.App()
stk = EcsClusterStack(app, "ecs-cluster-stack", env=cdk.Environment(account=account_id, region=region))
if TAGS.keys():
    for k in TAGS.keys():
        cdk.Tags.of(stk).add(k, TAGS[k])
app.synth()
